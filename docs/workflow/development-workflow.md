# 开发工作流

> QWeb 项目的完整开发流程、模块开发顺序与协作规范

---

## 1. 开发环境准备

### 1.1 系统要求

- Python 3.12+
- Node.js 20+（LTS）
- PostgreSQL 16+
- Redis 7+
- Git

### 1.2 初始化步骤

```bash
# 1. 克隆仓库
git clone <repo_url>
cd QWeb

# 2. 初始化数据库
psql -U postgres -f docs/postgresql-init.sql

# 3. 后端环境
cd backend
uv sync
cp .env.example .env           # 修改 .env 中的数据库与 Redis 配置
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 0.0.0.0:8000

# 4. 前端环境
cd ../frontend
npm install
cp .env.example .env           # 修改 API 代理地址
npm run dev                    # 启动在 http://localhost:3000
```

### 1.3 端口规划

| 服务 | 端口 | 说明 |
|------|------|------|
| Django 后端 | 8000 | API 服务 |
| Vite 前端 | 3000 | 开发服务器 |
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 缓存/队列 |

### 1.4 GitHub OAuth 登录

本地 GitHub OAuth App 的回调地址应配置为：

```text
http://127.0.0.1:3000/auth/github/callback
```

后端使用以下环境变量读取 GitHub OAuth 配置：

```env
GITHUB_OAUTH_CLIENT_ID=your-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-client-secret
GITHUB_OAUTH_CALLBACK_URL=http://127.0.0.1:3000/auth/github/callback
GITHUB_OAUTH_STATE_MAX_AGE=600
```

GitHub `client_secret` 只允许配置在后端 `.env`，前端通过 `/api/v1/auth/oauth/github/authorize/` 获取授权地址，不直接持有密钥。旧 `/api/v1/auth/github/authorize/` 保留为兼容入口，新代码默认使用 provider 化接口。

首次 GitHub 登录未命中既有关联时，前端回调页会进入“绑定已有账号 / 创建新账号”选择流程。即使第三方邮箱与本地邮箱相同，也只作为提示，不自动绑定。

---

## 2. 模块开发顺序

采用自底向上、先基础后业务的策略：

### 阶段 1：基础设施层

```text
core → accounts → iam → audit → system_config
```

| 步骤 | 模块 | 产出 | 依赖 |
|------|------|------|------|
| 1 | `core` | BaseModel、统一响应、通用工具 | 无 |
| 2 | `accounts` | 用户注册/登录/JWT/资料管理 | core |
| 3 | `iam` | 角色/权限/覆盖/策略 | core, accounts |
| 4 | `audit` | 登录日志/操作日志/高危审计 | core, accounts, iam |
| 5 | `system_config` | 站点配置/模块开关/策略配置 | core, accounts, iam |

### 阶段 2：平台服务层

```text
notifications → media_center
```

| 步骤 | 模块 | 产出 | 依赖 |
|------|------|------|------|
| 6 | `notifications` | 通知引擎 | 阶段 1 全部 |
| 7 | `media_center` | 图片/文件统一管理 | 阶段 1 全部 |

### 阶段 3：内容模块

```text
blog → wiki
```

| 步骤 | 模块 | 产出 | 依赖 |
|------|------|------|------|
| 8 | `blog` | 文章 CRUD/分类/标签/评论 | 阶段 1-2 |
| 9 | `wiki` | 文档页面 CRUD/版本/权限 | 阶段 1-2 |

### 阶段 4：存储模块

```text
storage → temp_transfer
```

| 步骤 | 模块 | 产出 | 依赖 |
|------|------|------|------|
| 10 | `storage` | 文件上传/管理/分享 | 阶段 1-2 |
| 11 | `temp_transfer` | 临时传输/二维码取件 | 阶段 1-2 |

### 阶段 5：工具与基础设施模块

```text
network_tools → frp_manager → ssh_gateway → mc_manager → mail_center → dev_workspace
```

| 步骤 | 模块 | 产出 | 依赖 |
|------|------|------|------|
| 12 | `network_tools` | 测速/Ping/路由追踪 | 阶段 1 |
| 13 | `frp_manager` | FRP 隧道配置/状态 | 阶段 1 |
| 14 | `ssh_gateway` | 主机/会话/终端/命令审计 | 阶段 1, Channels |
| 15 | `mc_manager` | MC 服务器管理 | 阶段 1, Channels |
| 16 | `mail_center` | 邮件账号/模板/发件 | 阶段 1, Celery |
| 17 | `dev_workspace` | 远程开发工作区信息 | 阶段 1 |

---

## 3. 单模块开发流程

每个模块按以下步骤开发：

```text
┌──────────────────────────────────────────────────────────────┐
│  1. Models        定义数据模型、字段、约束                      │
│         ↓                                                    │
│  2. Migrations    生成并检查数据库迁移                          │
│         ↓                                                    │
│  3. Services      实现核心业务逻辑                              │
│         ↓                                                    │
│  4. Selectors     实现查询逻辑                                 │
│         ↓                                                    │
│  5. Serializers   入参校验 + 输出格式化                         │
│         ↓                                                    │
│  6. Views         ViewSet/APIView，调用 service               │
│         ↓                                                    │
│  7. URLs          注册路由                                     │
│         ↓                                                    │
│  8. Permissions   定义权限码 + DRF Permission Class            │
│         ↓                                                    │
│  9. Audit         在 service 中接入审计日志                     │
│         ↓                                                    │
│ 10. Tasks         异步任务（如需要）                            │
│         ↓                                                    │
│ 11. Consumers     WebSocket（如需要）                          │
│         ↓                                                    │
│ 12. Tests         单元测试 + API 测试 + 权限测试               │
│         ↓                                                    │
│ 13. Docs          API 文档更新 + docs/ 同步                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. 前端开发流程

### 4.1 全局基础搭建（一次性）

```text
1. 安装 Fluent 2 Token / 组件库
2. 创建 Layout 组件（PublicLayout、DashboardLayout、AdminLayout）
3. 配置路由结构与守卫
4. 实现 Auth Store + API Client（JWT 注入、拦截器）
5. 实现权限 Store + 权限指令
6. 实现全局通知/Toast 组件
```

### 4.2 单模块前端开发

```text
1. API 层     — 在 src/api/{module}.ts 中定义接口调用
2. Types     — 在 src/types/{module}.ts 中定义 TypeScript 类型
3. Store     — 如需全局状态，在 src/stores/ 中创建
4. Pages     — 在 src/pages/{module}/ 下创建页面组件
5. Components — 模块业务组件放 src/components/business/
6. Routes    — 在 src/router/routes/{module}.ts 中注册路由
7. Permission — 使用 v-permission 指令控制 UI 元素
```

---

## 5. 前后端联调流程

```text
1. 后端完成 API → 在 /api/docs/ (Swagger) 中验证
2. 前端根据 Swagger 文档编写 API 层
3. Vite 开发服务器代理 /api/* → localhost:8000
4. 联调验证：
   a. 正常流程测试
   b. 权限拒绝场景
   c. 错误处理验证
   d. 分页/筛选验证
5. 联调完成后：
   a. 后端提交 commit
   b. 前端提交 commit
   c. 更新 docs/ 中相关文档
```

---

## 6. IAM 集成工作流

每个业务模块接入 IAM 的标准流程：

### 6.1 后端

```text
1. 在 apps/{module}/permissions/ 中定义权限码常量
   例: BLOG_POST_CREATE = "blog.post.create"

2. 在初始迁移或 seed 数据中注册权限到 IAM

3. 在 apps/{module}/api/views/ 中引用 IAM Permission Class
   permission_classes = [IsAuthenticated, HasPermission("blog.post.create")]

4. 在 apps/{module}/services/ 的关键操作处调用审计记录
   audit_log(user, "blog.post.create", target=post)

5. 在角色种子数据中配置默认角色-权限映射
```

### 6.2 前端

```text
1. 登录后拉取用户权限列表 → 存入 permission store

2. 路由 meta 中声明所需权限
   { path: '/blog/editor', meta: { requiredPermission: 'blog.post.create' } }

3. 页面按钮/操作使用 v-permission 指令
   <button v-permission="'blog.post.create'">新建文章</button>

4. 菜单项根据权限列表过滤显示
```

---

## 7. Git 工作流

### 7.1 分支策略

```text
main             ← 稳定发布分支
  └─ develop     ← 开发集成分支
      ├─ feat/accounts-auth     ← 功能分支
      ├─ feat/iam-rbac
      ├─ fix/blog-pagination
      └─ refactor/api-response
```

### 7.2 开发节奏

```text
1. 从 develop 创建功能分支
2. 按模块开发流程完成功能
3. 每完成一个独立可审查块 → commit
4. 功能完成 → 自测 → 更新文档 → PR 到 develop
5. Code Review → 合并
6. 定期从 develop 合并到 main 发布
```

### 7.3 Commit 规范

```text
type(scope): 中文摘要

类型: feat / fix / refactor / docs / style / test / perf / build / ci / chore / revert
范围: 模块名（accounts / iam / blog / frontend 等）

示例:
feat(accounts): 实现用户注册与 JWT 认证
fix(iam): 修复权限覆盖优先级判断
docs(architecture): 更新 IAM 设计文档
test(blog): 补充文章发布权限测试
```

---

## 8. 测试策略

### 8.1 后端测试

| 层级 | 目标 | 工具 |
|------|------|------|
| 单元测试 | services / selectors / permissions | pytest + Django TestCase |
| API 测试 | 接口路由 + 响应格式 + 权限 | DRF APITestCase |
| 集成测试 | 跨模块流程 | pytest |

### 8.2 前端测试

| 层级 | 目标 | 工具 |
|------|------|------|
| 组件测试 | UI 组件渲染与交互 | Vitest + Vue Test Utils |
| E2E 测试 | 关键用户流程 | Playwright |

### 8.3 何时写测试

- Service 层核心逻辑：必须
- 权限检查逻辑：必须
- API 关键路由：必须
- 工具函数：必须
- UI 组件：关键交互测试
- E2E：登录流程、核心业务流程

---

## 9. 发布与部署

### 9.1 部署架构

```text
Docker Compose:
  ├─ nginx        — 反向代理 + 静态文件
  ├─ django       — Gunicorn/Uvicorn
  ├─ celery       — 异步任务 Worker
  ├─ celery-beat  — 定时任务调度
  ├─ channels     — WebSocket (Daphne/Uvicorn)
  ├─ postgres     — 数据库
  └─ redis        — 缓存 + 队列
```

### 9.2 CI/CD 流程

```text
Push → GitHub/Gitea Actions:
  1. Lint（后端 ruff/flake8 + 前端 eslint）
  2. 类型检查（mypy + vue-tsc）
  3. 测试（pytest + vitest）
  4. 构建（前端 vite build）
  5. Docker 镜像构建
  6. 部署到目标环境
```

---

## 10. 日常开发检查清单

开发每个功能前确认：

- [ ] 了解目标模块的职责边界
- [ ] 了解依赖的上游模块是否已就绪
- [ ] 创建功能分支

开发过程中：

- [ ] Models: 字段定义、约束、索引
- [ ] Services: 业务逻辑实现
- [ ] API: 序列化器、视图、路由
- [ ] Permissions: 权限码定义、IAM 集成
- [ ] Audit: 关键操作审计日志
- [ ] Tests: 测试覆盖
- [ ] Frontend: 页面、Store、API 层

完成后确认：

- [ ] 所有测试通过
- [ ] API 文档自动更新（drf-spectacular）
- [ ] docs/ 相关文档同步
- [ ] Commit 规范
- [ ] 无敏感信息泄露
