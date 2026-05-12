# docs 文档保存规则

> 本规则定义 QWeb 仓库内 `docs/` 的文档归档位置、维护方式和同步要求。

## 1. 总原则

- `docs/` 是项目设计、接口、模型、流程和决策的唯一长期文档目录。
- 后端、前端目录下默认不新增说明型文档；必要的配置模板和工具链标准文件除外。
- 文档更新应跟随代码变更一起提交。凡影响 API、数据库、权限、审计、配置、部署、路由或关键交互，都必须同步更新对应文档。
- 不把真实密钥、真实令牌、生产账号、内网敏感地址写入文档。
- 生成型文档应标明生成命令和事实来源，避免手写内容与生成内容长期分叉。

## 2. 目录归档规则

|目录|保存内容|示例|
|---|---|---|
|`docs/architecture/`|跨模块架构、权限模型、API 规范、模块边界|`system-overview.md`、`iam-design.md`、`api-design.md`|
|`docs/backend/`|Django app 结构、数据模型、服务边界、后端实现约束|`django-apps.md`、`user-module-schema.md`|
|`docs/frontend/`|路由、布局、设计系统、前端交互约定|`routing.md`、`design-system.md`|
|`docs/api/`|OpenAPI、接口生成物和机器可读契约|`openapi.yaml`|
|`docs/decisions/`|ADR 架构决策记录|`ADR-001-architecture.md`|
|`docs/workflow/`|开发、协作、文档、发布、验证流程|`development-workflow.md`、`documentation-rules.md`|
|`docs/` 根目录|项目入口索引、总体架构原始稿、少量全局参考文件|`README.md`、`总体架构.md`、`postgresql-init.sql`|

## 3. 命名规则

- Markdown 文件使用小写英文和短横线，例如 `user-module-schema.md`。
- ADR 使用 `ADR-序号-英文短名.md`，序号递增且不复用。
- 不新增与现有文档职责重复的文件；优先更新已有文档相关章节。
- 中文标题可以保留在文件内容中，文件名优先保持英文稳定路径。

## 4. API 文档规则

- `docs/architecture/api-design.md` 保存人工维护的接口设计和语义说明。
- `docs/api/openapi.yaml` 保存 drf-spectacular 生成的机器可读契约。
- `openapi.yaml` 不手写维护；使用后端命令生成或刷新。
- 接口字段、路径、认证方式变更时，必须同时检查人工 API 文档和 OpenAPI 生成物。

## 5. 后端文档规则

- 数据模型、表结构、迁移策略和服务边界放入 `docs/backend/`。
- 涉及权限解析、角色、覆盖、资源策略时，同步更新 `docs/architecture/iam-design.md`。
- 涉及数据库结构变化时，文档必须说明主键、外键、唯一约束、软删除、审计影响和旧数据兼容策略。
- 高风险模块文档必须说明权限、审计、回滚或失败处理边界。

## 6. 前端文档规则

- 路由、新页面、布局切换、权限展示入口更新 `docs/frontend/routing.md`。
- 设计系统、Fluent 2 组件使用方式、交互状态和响应式规则更新 `docs/frontend/design-system.md`。
- 前端只做权限体验优化，不把隐藏按钮描述成安全边界。

## 7. 工作流文档规则

- 开发环境、命令、迁移、测试、构建、发布、PR 流程放入 `docs/workflow/`。
- 命令示例必须与仓库当前工具链一致，例如后端使用 `uv run python manage.py ...`。
- 当工具链变化时，更新工作流文档而不是只修改 README。

## 8. 文档索引规则

- 新增文档后必须更新 `docs/README.md`。
- 索引说明应短而明确，避免复制文档正文。
- 删除或重命名文档时，必须同步修正所有引用链接。

## 9. 提交前检查

- 新增文档是否放在正确目录。
- 是否存在重复职责文档。
- 相关 API、模型、权限、前端路由文档是否同步。
- 文档中是否包含真实密钥或不可公开信息。
- 文档中的命令是否能在当前仓库执行。
