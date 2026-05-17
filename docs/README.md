# QWeb 项目文档

> 文档索引 — 所有文档的入口

---

## 架构设计

| 文档 | 说明 |
|------|------|
| [总体架构](总体架构.md) | 完整架构设计原始文档 |
| [系统概览](architecture/system-overview.md) | 技术栈、模块清单、部署拓扑 |
| [IAM 设计](architecture/iam-design.md) | 三层权限模型、数据模型、判断流程 |
| [API 设计](architecture/api-design.md) | 接口规范、响应格式、端点参考 |
| [模块边界](architecture/module-boundaries.md) | 17 个模块职责与协作关系 |

## 后端开发

| 文档 | 说明 |
|------|------|
| [Django Apps](backend/django-apps.md) | App 结构、服务层模式、导入规则 |
| [用户模块表结构](backend/user-module-schema.md) | 用户核心表、扩展表、OAuth 绑定与登录日志设计 |

## 前端开发

| 文档 | 说明 |
|------|------|
| [路由设计](frontend/routing.md) | 路由分区、守卫、懒加载 |
| [设计系统](frontend/design-system.md) | Material 3、Material Web、Token 体系、主题 |

## 工作流

| 文档 | 说明 |
|------|------|
| [开发工作流](workflow/development-workflow.md) | 环境搭建、模块开发顺序、Git 规范、测试、CI/CD |
| [快速开始](workflow/getting-started.md) | 新开发者环境搭建速查 |
| [文档保存规则](workflow/documentation-rules.md) | docs 目录归档、命名、同步与索引规则 |

## 架构决策记录 (ADR)

| 文档 | 说明 |
|------|------|
| [ADR-001: 整体架构](decisions/ADR-001-architecture.md) | 前后端分离、领域模块化、Docker Compose |
| [ADR-002: IAM 模型](decisions/ADR-002-iam-model.md) | 三层权限模型选型 |
| [ADR-003: 存储策略](decisions/ADR-003-storage-strategy.md) | 分阶段存储方案 |

## 参考

| 文档 | 说明 |
|------|------|
| [端口说明](本地开发端口说明.md) | 本地开发端口分配 |
| [数据库初始化](postgresql-init.sql) | PostgreSQL 建库脚本 |
| [OpenAPI 契约](openapi/openapi.yaml) | 分文件维护的机器可读 API 契约入口 |
