# ADR-001: 整体架构决策

> 状态: **已采纳**  
> 日期: 2025

---

## 背景

QWeb 是一个个人网站 / 基础设施门户 / 内容平台 / 工具中台。需要在单个项目中承载认证、权限、博客、存储、SSH 网关、MC 管理等 17 个业务模块。

## 决策

### 1. 前后端分离架构

采用 Django + DRF 提供 REST API，Vue 3 + TypeScript 作为纯前端 SPA。

**理由**：
- 前后端职责清晰，独立部署和迭代
- API 可同时服务 Web、移动端、CLI 等多端
- Django 生态成熟，DRF 序列化/权限/文档一体化

### 2. 领域模块化 Django Apps

将 17 个业务模块拆分为独立 Django App，按三层架构组织：

- **基础层**: core
- **平台层**: accounts, iam, audit, system_config, notifications, media_center
- **业务层**: blog, wiki, storage, temp_transfer, network_tools, frp_manager, ssh_gateway, mc_manager, mail_center, dev_workspace

**理由**：
- 每个模块有明确的职责边界
- 模块间通过 service 接口协作，禁止直接跨模块 import model
- 便于按需启用/禁用（system_config 模块开关）
- 支持渐进开发，不影响其他模块

### 3. 统一 API 风格

- 路径前缀 `/api/v1/`
- JWT Bearer 认证
- 统一响应格式 `{code, message, data}`
- drf-spectacular 自动生成 OpenAPI 文档

**理由**：
- 一致的接口风格降低前端对接成本
- 自动生成文档减少维护负担

### 4. Docker Compose 部署

生产环境使用 Docker Compose 编排所有服务。

**理由**：
- 个人项目规模，Kubernetes 过重
- Docker Compose 足以管理 Nginx + Django + Celery + Channels + PostgreSQL + Redis
- 部署和回滚简单

## 替代方案

| 方案 | 评估 | 否决原因 |
|------|------|----------|
| Django 模板渲染 | 简单但受限 | 不支持复杂交互，前后端耦合 |
| 微服务架构 | 灵活但复杂 | 个人项目运维成本过高 |
| FastAPI | 性能好 | Django 生态更全面（ORM、Admin、Auth） |
| Kubernetes | 生产级 | 规模不匹配，资源浪费 |

## 影响

- 所有模块必须遵循统一的 App 内部结构
- 前后端通过 API 契约协作
- 模块开关通过 system_config 而非代码层面删除
