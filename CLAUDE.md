# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库定位

QWeb 是一个个人基础设施门户 / 内容平台 / 工具中台。当前仓库采用前后端分离：`backend/` 是 Django + DRF API，`frontend/` 是 Vue 3 + TypeScript + Vite SPA，`docs/` 保存架构、工作流与 OpenAPI 契约。

进入本仓库工作时必须同时遵守根目录 `AGENTS.md`；修改 `backend/` 或 `frontend/` 时还必须遵守对应子目录的 `AGENTS.md`。

## 常用命令

### 环境初始化

```bash
# 数据库初始化脚本在仓库根目录执行
psql -U postgres -f docs/postgresql-init.sql

# 后端依赖与环境
cd backend
uv sync
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py init_permissions
uv run python manage.py seed_admin
uv run python manage.py runserver 0.0.0.0:8000

# 前端依赖与环境
cd ../frontend
npm install
cp .env.example .env
npm run dev
```

本地默认端口：后端 `http://127.0.0.1:8000`，前端 `http://127.0.0.1:3000`，PostgreSQL `5432`，Redis `6379`。

GitHub OAuth 本地回调地址是 `http://127.0.0.1:3000/auth/github/callback`，后端读取 `GITHUB_OAUTH_CLIENT_ID`、`GITHUB_OAUTH_CLIENT_SECRET`、`GITHUB_OAUTH_CALLBACK_URL`、`GITHUB_OAUTH_STATE_MAX_AGE`。

### 后端

```bash
cd backend

# 开发服务器
uv run python manage.py runserver 0.0.0.0:8000

# 数据库迁移
uv run python manage.py makemigrations <app_name>
uv run python manage.py migrate

# 初始化 IAM 预置角色与权限；需要重建关联时加 --reset
uv run python manage.py init_permissions
uv run python manage.py init_permissions --reset

# 创建初始管理员并分配 owner 角色（幂等）
uv run python manage.py seed_admin

# Django shell
uv run python manage.py shell

# 全量测试
uv run python manage.py test

# 单 app / 单类 / 单测试方法
uv run python manage.py test apps.accounts
uv run python manage.py test apps.accounts.tests.UsernamePolicyTests
uv run python manage.py test apps.accounts.tests.UsernamePolicyTests.test_accepts_valid_usernames
```

后端健康检查与文档入口：`/api/health/`、`/api/schema/`、`/api/docs/`。

### 前端

```bash
cd frontend

# Vite 开发服务器
npm run dev

# 类型检查 + 生产构建
npm run build

# 预览构建产物
npm run preview

# 只做类型检查
npx vue-tsc --noEmit
```

当前 `frontend/package.json` 只定义了 `dev`、`build`、`preview`；不要在未添加脚本前假设存在 `npm run lint` 或 `npm run test`。

### OpenAPI 契约

```bash
# 仓库根目录执行
npx @redocly/cli lint docs/openapi/openapi.yaml
```

`docs/openapi/openapi.yaml` 是分文件 OpenAPI 契约入口，`redocly.yaml` 继承 recommended 规则并关闭 `no-path-trailing-slash`。

## 当前代码架构

### 后端入口与已接线模块

- Django 配置入口：`backend/config/settings.py`。
- URL 入口：`backend/config/urls.py`。
- 当前 `INSTALLED_APPS` 已接线本地 app：`apps.core`、`apps.accounts`、`apps.iam`、`apps.audit`、`apps.homepage`。
- 当前 API 路由接入：accounts、iam、audit、homepage，统一挂在 `/api/v1/` 下；健康检查和 schema 分别在 `/api/health/`、`/api/schema/`。
- 自定义用户模型是 `accounts.User`，SimpleJWT 使用 `uid` 作为用户 ID 字段与 JWT claim。
- DRF 默认使用 `apps.core.exception_handler.unified_exception_handler`、`apps.core.pagination.StandardPagination`，响应约定是 `{code, message, data}`，错误响应是 `{code, message, errors}`。

### Django app 内部分层

后端模块按职责分层，新增或修改功能时保持既有形状：

```text
apps/{module}/
├─ models/          # 数据模型；每个模型一个文件，通过 __init__.py 导出
├─ api/
│  ├─ serializers/  # 入参校验与输出格式化
│  └─ views/        # 请求接入、权限检查、响应组织
├─ services/        # 写操作与业务流程编排
├─ selectors/       # 读路径查询与聚合
├─ permissions/     # 权限码与 DRF permission
├─ management/      # 管理命令
└─ migrations/      # 数据库迁移
```

View 不承载完整业务流程，Serializer 不做复杂查询或副作用，Service 负责事务边界、权限调用和审计写入，Selector 负责列表/聚合读路径。

### IAM 与审计边界

权限码格式为 `{module}.{resource}.{action}`。预置角色为 `owner`、`admin`、`trusted`、`user`、`guest`；角色权限可编辑，用户权限覆盖支持 `allow` / `deny`，且 `deny` 优先。

不要在业务代码中散落 `if is_admin` 式硬编码；敏感操作必须以后端 IAM 校验为准，前端权限展示只用于体验优化。涉及角色、权限、用户封禁/启用、文件删除、SSH/FRP/MC/邮件/工作区、系统配置等高风险动作时，要同步考虑审计。

### 规划模块与当前实现的区别

文档中规划了 `system_config`、`notifications`、`media_center`、`blog`、`wiki`、`storage`、`temp_transfer`、`network_tools`、`frp_manager`、`ssh_gateway`、`mc_manager`、`mail_center`、`dev_workspace` 等模块，但当前代码只接线了基础账号、IAM、审计和首页服务链接相关模块。引用规划模块前先确认代码是否已实际存在。

## 前端架构

- Vite 配置入口：`frontend/vite.config.ts`，`@` 指向 `frontend/src`，开发端口固定为 `3000`，并将 `md-*` 声明为 Vue custom elements。
- 应用入口：`frontend/src/main.ts`，初始化 Pinia、Vue Router、vue-i18n 与 Material Web Components，并加载 `src/styles/tokens.css` 和 `src/style.css`。
- 根组件：`frontend/src/App.vue` 提供 skip link 并渲染 `RouterView`。
- API 客户端：`frontend/src/api/client.ts` 使用 Axios，`VITE_API_BASE_URL` 默认 `http://127.0.0.1:8000`，baseURL 为 `${VITE_API_BASE_URL}/api/v1`；请求自动附加 Bearer token，401 时尝试 refresh token 续签。
- 路由入口：`frontend/src/router/index.ts`，公开页走 `PublicLayout`，认证页走 `DashboardLayout`，路由 `meta.permission` 与后端 IAM 权限码保持一致。
- 状态管理：`src/stores/auth.ts` 管认证状态，`src/stores/permission.ts` 管权限缓存，`src/stores/app.ts` 管全局应用状态。
- 设计系统：Material 3 基线，设计 token 在 `src/styles/tokens.css`，Material Web custom elements 注册在 `src/styles/material-setup.ts`；根目录 `DESIGN.md` 是当前 UI 规范源。

## API 与文档同步规则

长期文档统一在 `docs/`。影响 API、数据库、权限、审计、配置、部署、路由或关键交互时，同步更新相关文档：

- API 语义：`docs/architecture/api-design.md`
- OpenAPI 契约：`docs/openapi/openapi.yaml`、`docs/openapi/paths/*.yaml`、`docs/openapi/components/**/*.yaml`
- IAM / 权限：`docs/architecture/iam-design.md`
- 模块边界：`docs/architecture/module-boundaries.md`
- Django app 结构：`docs/backend/django-apps.md`
- 用户表结构：`docs/backend/user-module-schema.md`
- 前端路由：`docs/frontend/routing.md`
- 前端设计系统：`docs/frontend/design-system.md`
- 工作流命令变化：`docs/workflow/development-workflow.md` 或 `docs/workflow/getting-started.md`

OpenAPI 运行时 schema 由 drf-spectacular 暴露在 `/api/schema/`，但仓库维护的契约源是 `docs/openapi/` 分文件 YAML。

## 代码与提交约束

- Python、Vue、TypeScript 等代码文件应保留仓库现有文件头注释风格；Python 函数需要类型标注和 reStructuredText 风格文档注释。
- 命名必须有业务语义，避免 `tmp`、`data`、`obj`、`res` 等弱语义名称。
- 单文件过长时优先拆分；不要继续在超过 500 行的文件里堆积实现，除非本次任务范围已有明确限制。
- 默认不主动执行 `git push`、切换分支、新建分支、提交 PR 或改写远端历史。
- commit 格式使用 `type(scope): 中文摘要`，例如 `feat(accounts): 接入 GitHub OAuth 登录`。
- 用户全局规则要求 git commit message 末尾包含 `Qintsg`；如果需要提交，遵守该要求。

## 已知仓库状态提示

根目录 `README.md` 与 `backend/README.md` 当前几乎为空，开发事实主要来自 `AGENTS.md`、`docs/`、`pyproject.toml`、`package.json` 和实际源码。若文档与代码冲突，以当前源码和可执行验证结果为准，并在必要时更新文档。
