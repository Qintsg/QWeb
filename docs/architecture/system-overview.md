# 系统总览

> QWeb — 个人基础设施门户 / 内容平台 / 工具中台

---

## 1. 定位

QWeb 是一个面向个人或小团队的综合型 Web 平台，核心目标：

- 统一管理个人基础设施（SSH、FRP、Minecraft、远程开发等）
- 提供内容创作与发布能力（博客、Wiki）
- 集成常用工具（云盘、临时传输、网络工具、邮件等）
- 通过统一 IAM 体系实现安全、可审计的权限管理

---

## 2. 技术栈

### 2.1 后端

| 层面     | 选型                                |
| -------- | ----------------------------------- |
| 语言     | Python 3.12                         |
| 框架     | Django 5.x + Django REST Framework  |
| 认证     | JWT（djangorestframework-simplejwt） |
| 异步任务 | Celery + Redis                      |
| 实时通信 | Django Channels + channels_redis    |
| 数据库   | PostgreSQL                          |
| 缓存     | Redis                               |
| API 文档 | drf-spectacular（OpenAPI 3）        |
| 过滤     | django-filter                       |

### 2.2 前端

| 层面     | 选型                          |
| -------- | ----------------------------- |
| 框架     | Vue 3 + TypeScript            |
| 构建     | Vite                          |
| 状态管理 | Pinia                         |
| 路由     | Vue Router                    |
| 设计系统 | Material 3 + Material Web      |
| HTTP     | Axios / ofetch                |
| 工具库   | VueUse                        |
| CSS      | UnoCSS / Tailwind（可选）     |

### 2.3 基础设施

| 层面     | 选型                           |
| -------- | ------------------------------ |
| 数据库   | PostgreSQL                     |
| 缓存     | Redis                          |
| 容器化   | Docker + Docker Compose        |
| 反向代理 | Nginx / Caddy                  |
| CI/CD    | GitHub Actions / Gitea Actions |
| 监控     | Sentry + Prometheus + Grafana  |

---

## 3. 架构模式

```
[浏览器]
   │
   ├── HTTPS ──▶ [Nginx/Caddy]
   │                │
   │                ├── /api/v1/*   ──▶ [Django + DRF]  ──▶ [PostgreSQL]
   │                ├── /ws/*       ──▶ [Channels/ASGI] ──▶ [Redis PubSub]
   │                └── /*          ──▶ [Vue SPA 静态]
   │
   └── 异步任务 ──▶ [Celery Worker] ──▶ [Redis Queue]
```

- **前后端分离**：前端 Vue SPA，后端纯 API
- **领域模块化**：每个业务域是独立 Django app
- **统一 IAM**：所有权限校验走 `iam` 模块，不各自为政
- **统一审计**：高危操作统一记录到 `audit` 模块
- **统一配置**：模块开关、站点配置走 `system_config`

---

## 4. 分层架构

### 4.1 三层划分

```
基础层（core / common / config）
    └── 提供基础模型、通用工具、响应格式、中间件

平台层（audit / notifications / system_config / media_center）
    └── 横切关注点，供所有业务模块调用

领域层（accounts / iam / blog / wiki / storage / ssh_gateway / ...）
    └── 各业务域独立实现，仅通过 service 接口互调
```

### 4.2 Django App 内部分层

```
app/
├─ models/        # 数据模型定义
├─ api/
│  ├─ serializers/  # 序列化与校验
│  ├─ views/        # API 视图
│  └─ filters.py    # 过滤器
├─ services/      # 业务逻辑（写操作编排）
├─ selectors/     # 查询逻辑（读操作聚合）
├─ permissions/   # 权限判定
├─ tasks/         # Celery 异步任务
├─ consumers/     # WebSocket 消费者
├─ signals/       # Django 信号
├─ tests/         # 模块内测试
└─ migrations/    # 数据库迁移
```

---

## 5. 模块总览

| 分类   | 模块             | 职责                   |
| ------ | ---------------- | ---------------------- |
| 基础   | core             | 健康检查、基础模型     |
| 基础   | accounts         | 注册、登录、资料       |
| 基础   | iam              | 角色、权限、覆盖、策略 |
| 平台   | audit            | 操作日志、登录审计     |
| 平台   | system_config    | 站点配置、模块开关     |
| 平台   | notifications    | 站内通知               |
| 内容   | blog             | 博客文章               |
| 内容   | wiki             | 知识库                 |
| 内容   | media_center     | 媒体资源管理           |
| 工具   | storage          | 云盘                   |
| 工具   | temp_transfer    | 临时传输               |
| 工具   | network_tools    | 测速、Ping、端口检测   |
| 工具   | frp_manager      | FRP 隧道管理           |
| 工具   | ssh_gateway      | SSH 网关               |
| 工具   | mc_manager       | Minecraft 服务管理     |
| 工具   | mail_center      | 邮件发送               |
| 工具   | dev_workspace    | 远程开发工作区         |

---

## 6. 数据存储职责

| 存储         | 适用内容                                                 |
| ------------ | -------------------------------------------------------- |
| PostgreSQL   | 用户、角色、权限、审计、内容、元数据、配置、任务记录     |
| Redis        | 缓存、队列、节流、锁、短期状态、WebSocket 辅助           |
| 文件系统     | 上传文件、媒体资源、临时传输、备份产物、缩略图           |
| .env / Secret| 凭据、令牌、SMTP、SSH 密钥、第三方密钥                  |

---

## 7. 开发端口

| 服务   | 端口 | 地址                           |
| ------ | ---- | ------------------------------ |
| 后端   | 8000 | http://127.0.0.1:8000          |
| 前端   | 5173 | http://127.0.0.1:5173          |
| API    | 8000 | http://127.0.0.1:8000/api/v1/  |
| Swagger| 8000 | http://127.0.0.1:8000/api/docs/|
| 健康   | 8000 | http://127.0.0.1:8000/api/health/|
