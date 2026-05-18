# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库定位

QWeb 是一个个人基础设施门户 / 内容平台 / 工具中台。当前仓库采用前后端分离：`backend/` 是 Django + DRF API，`frontend/` 是 Vue 3 + TypeScript + Vite SPA，`docs/` 保存架构、工作流与 OpenAPI 契约。

本文件是仓库内 Claude Code 的唯一协作指引；原 `AGENTS.md` 中的通用、后端和前端规则已收敛到本文，不再维护单独的 `AGENTS.md` 文件。

## 工作原则与规则优先级

规则冲突按以下顺序处理：用户当前明确要求、`CLAUDE.md`、仓库既有约定、官方标准与通用工程约定。

开始修改前先理解相邻文件、模块分层、API 契约、权限与审计边界、测试和文档；只实现用户明确要求、完成任务必要配套修改、代码上下文可直接推断的内容，不擅自新增业务模块、空壳服务、无落地场景的抽象层或无依据预留字段。

默认交付可运行、可验证、可审查的完整实现；除非确有必要，不保留空函数、`pass`、假成功返回、未接线按钮、未接线 API、未接线权限码或未接线审计逻辑。确需保留未完成项时，使用 `TODO:` / `FIXME:` 写明原因、影响范围、后续动作和风险说明。

最终代码、注释、文档和提交说明只保留稳定、正向、面向结果的内容，不保留过程性残留表达。

## 常用命令

### 环境初始化

```bash
# 数据库初始化脚本在仓库根目录执行
psql -U postgres -v qweb_db=qweb -v qweb_user=qweb_app -v qweb_password='replace-with-local-password' -f docs/postgresql-init.sql

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

本地默认端口：后端 `http://127.0.0.1:8000`，前端 `http://127.0.0.1:5173`，PostgreSQL `5432`，Redis `6379`。

GitHub OAuth 本地回调地址是 `http://127.0.0.1:5173/auth/github/callback`，后端读取 `GITHUB_OAUTH_CLIENT_ID`、`GITHUB_OAUTH_CLIENT_SECRET`、`GITHUB_OAUTH_CALLBACK_URL`、`GITHUB_OAUTH_STATE_MAX_AGE`。

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

# 首次部署时通过前端引导页或交互式参数创建站长账号
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

## 后端专项规则

后端技术栈为 Python、Django、Django REST Framework、PostgreSQL、Redis、Celery、Django Channels。后端承载用户与认证、IAM 权限体系、审计与系统配置、博客与 Wiki 内容、文件与临时传输、FRP、SSH、邮件、远程开发、Minecraft 等服务管理、异步任务、实时状态与终端通道。

后端模块按职责分层，新增或修改功能时保持既有形状：

```text
apps/{module}/
├─ models/          # 事务结构与数据约束；每个模型一个文件，通过 __init__.py 导出
├─ api/
│  ├─ serializers/  # 输入输出校验与转换
│  └─ views/        # 请求接入、权限检查、响应组织
├─ services/        # 写操作与业务流程编排
├─ selectors/       # 读路径查询与聚合
├─ permissions/     # 权限码校验、角色解析、覆盖解析
├─ tasks/           # 异步任务
├─ consumers/       # WebSocket / 实时通道
├─ integrations/    # SSH、FRP、SMTP、工作区等外部系统交互
├─ management/      # 管理命令
└─ migrations/      # 数据库迁移
```

View 不承载完整业务流程，Serializer 不做复杂查询或副作用，Service 负责事务边界、权限调用和审计写入，Selector 负责列表与聚合读路径。不要在 Model `save()` 中触发高风险外部动作，不要把长耗时任务直接塞进同步请求，不要把外部网络调用包进长事务。

列表接口优先分页，热路径关注索引，避免 N+1 查询，不在循环中隐式访问数据库。凭据只从配置读取，不写死在代码里，不回显到日志、异常或 API 响应；修改配置相关逻辑时检查 `.env.example` 与文档是否需要同步。

Python 代码遵循 PEP 8 注释要求，所有 `.py` 文件保留文件头注释，所有函数和类需要文档注释；函数参数与返回值必须显式类型标注，`-> None` 必须显式写出。

完成后端任务时说明改了哪些 Model、Serializer、View、Service、Selector、Task、Consumer、Permission 模块，是否影响 API 契约、PostgreSQL、Redis、文件存储、角色权限覆盖、审计、高权限动作，更新了哪些 `docs/`，做了哪些验证以及剩余风险。

### IAM 与审计边界

权限码格式为 `{module}.{resource}.{action}`。预置角色为 `owner`、`admin`、`trusted`、`user`、`guest`；角色权限可编辑，用户权限覆盖支持 `allow` / `deny`，且 `deny` 优先。

不要在业务代码中散落 `if is_admin` 式硬编码；敏感操作必须以后端 IAM 校验为准，前端权限展示只用于体验优化。涉及角色、权限、用户封禁/启用、文件删除、SSH/FRP/MC/邮件/工作区、系统配置等高风险动作时，要同步考虑审计。

### 规划模块与当前实现的区别

文档中规划了 `system_config`、`notifications`、`media_center`、`blog`、`wiki`、`storage`、`temp_transfer`、`network_tools`、`frp_manager`、`ssh_gateway`、`mc_manager`、`mail_center`、`dev_workspace` 等模块，但当前代码只接线了基础账号、IAM、审计和首页服务链接相关模块。引用规划模块前先确认代码是否已实际存在。

## 前端架构与专项规则

前端技术栈为 Vue 3、TypeScript、Vite、Vue Router、Pinia、Material 3 Design System 和 `@material/web` custom elements。

- Vite 配置入口：`frontend/vite.config.ts`，`@` 指向 `frontend/src`，开发端口固定为 `5173`，并将 `md-*` 声明为 Vue custom elements。
- 应用入口：`frontend/src/main.ts`，初始化 Pinia、Vue Router、vue-i18n 与 Material Web Components，并加载 `src/styles/tokens.css` 和 `src/style.css`。
- 根组件：`frontend/src/App.vue` 提供 skip link 并渲染 `RouterView`。
- API 客户端：`frontend/src/api/client.ts` 使用 Axios，`VITE_API_BASE_URL` 默认 `http://127.0.0.1:8000`，baseURL 为 `${VITE_API_BASE_URL}/api/v1`；请求自动附加 Bearer token，401 时尝试 refresh token 续签。
- 路由入口：`frontend/src/router/index.ts`，公开页走 `PublicLayout`，认证页走 `DashboardLayout`，路由 `meta.permission` 与后端 IAM 权限码保持一致。
- 状态管理：`src/stores/auth.ts` 管认证状态，`src/stores/permission.ts` 管权限缓存，`src/stores/app.ts` 管全局应用状态。
- 设计系统：Material 3 基线，设计 token 在 `src/styles/tokens.css`，Material Web custom elements 注册在 `src/styles/material-setup.ts`；根目录 `DESIGN.md` 是当前 UI 规范源。

前端优先沿用仓库既有组件组织、API 封装、路由组织、状态管理、主题与 token 约定；无明确约定时优先保持 Composition API、强类型、明确分层、强语义命名和可测试的组件结构。

禁止 `var`，尽量不使用 `any`，优先 `const` / `let`，类型定义要有业务语义。组件名、store 名、API 名必须体现职责，避免 `tmp`、`data`、`obj`、`res` 等弱语义命名。

共享视觉元素优先沉淀为设计系统组件；页面层不要反复硬编码颜色、间距、圆角、阴影、状态色；导航、表单、反馈、卡片、表格、列表保持 Material 3 风格一致，不同模块不要出现多套视觉语言。

展示组件与业务组件分离，布局组件与页面组件分离，表单状态与展示分离，风险确认组件与实际业务请求分离，文件展示组件与文件权限逻辑分离。

默认不保留空页面、假按钮、未接线弹窗、假数据成功态、未处理错误态、无权限却仍可点击的危险操作。Vue、TypeScript、HTML、CSS、JavaScript 代码使用 reStructuredText 风格注释并保留文件头注释。

完成前端任务时说明改了哪些页面、组件、store、composable、API 调用，是否影响权限展示、高风险操作交互和 API 依赖，更新了哪些 `docs/`，做了哪些验证以及剩余风险。

## API 与文档同步规则

长期文档统一在 `docs/`。影响 API、数据库、权限、审计、配置、部署、路由或关键交互时，同步更新相关文档；更新文档时保留原有总体结构，只在相关章节增补或修订，保持标题层级与既有风格，不随意重写整份文档。除非用户明确要求或任务本身就是发版，不修改版本号。

`frontend/` 与 `backend/` 下默认不新增说明型文档；允许新增的必要文件仅限 `.env.example`、依赖或工具链必须存在的标准文件、构建运行部署测试所需配置模板。

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

## 工具、代码与提交约束

优先读取本地代码与 `docs/`，再查官方文档，再使用最合适的工具做验证，结果必须回到仓库实际代码与验证结论；同类能力避免重复调用。涉及 Material 3 布局、导航、表单、排版、状态、Token、可访问性、反馈组件或密集型后台界面规范时，优先查阅 Material Design 3 与 Material Web 官方文档。涉及 Django、DRF、Vue、Pinia、Vue Router、Celery、Channels 的框架行为、最佳实践或升级兼容性时，优先查阅官方文档。

- Python、Vue、TypeScript 等代码文件应保留仓库现有文件头注释风格；Python 函数需要类型标注和 reStructuredText 风格文档注释。
- 命名必须有业务语义，避免 `tmp`、`foo`、`bar`、`data`、`obj`、`res` 等弱语义名称，禁止用注释弥补糟糕命名。
- 禁止在代码、日志、截图、测试数据或文档中泄露真实密钥；禁止把敏感配置写死在源码中；禁止在高风险模块中默认放开权限、删除或绕过审计、为了调试永久关闭安全检查。
- 单文件过长时优先拆分；不要继续在超过 500 行的文件里堆积实现，除非本次任务范围已有明确限制。
- 完成一个独立、可审查且可验证的变更块后，根据原有 commit 规范自动执行本地 commit，无需用户再次确认；若测试失败、验证未执行或工作区包含与当前任务无关的改动，必须先向用户说明并等待指示。
- 默认不主动执行 `git push`、切换分支、新建分支、提交 PR 或改写远端历史。
- commit 格式使用 `type(scope): 中文摘要`，例如 `feat(accounts): 接入 GitHub OAuth 登录`。
- commit message 末尾必须包含单独一行 `Qintsg`。
- 仓库提供 `.gitmessage` 作为提交消息模板；需要启用时执行 `git config commit.template .gitmessage`。

## 已知仓库状态提示

根目录 `README.md` 与 `backend/README.md` 当前几乎为空，开发事实主要来自 `CLAUDE.md`、`docs/`、`pyproject.toml`、`package.json` 和实际源码。若文档与代码冲突，以当前源码和可执行验证结果为准，并在必要时更新文档。
