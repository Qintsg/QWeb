# backend/AGENTS.md

## 1. 适用范围

本文件适用于 `backend/` 目录。  
在本目录工作时，必须同时遵守：

- `/AGENTS.md`
- `/backend/AGENTS.md`

权限等级只引用根目录字段：

**AI_PERMISSION_LEVEL**

---

## 2. 后端技术事实

技术栈：

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Django Channels

后端承载：

- 用户与认证
- IAM 权限体系
- 审计与系统配置
- 博客与 Wiki 内容
- 文件与临时传输
- FRP、SSH、邮件、远程开发、Minecraft 等服务管理
- 异步任务
- 实时状态与终端通道

---

## 3. 后端核心规则

### 3.1 分层
推荐职责边界：

- `models`：事务结构与数据约束
- `serializers`：输入输出校验与转换
- `views` / `viewsets`：请求接入、权限检查、响应组织
- `services`：业务流程编排
- `selectors`：读路径查询与聚合
- `permissions`：权限码校验、角色解析、覆盖解析
- `tasks`：异步任务
- `consumers`：WebSocket / 实时通道
- `integrations`：与 SSH、FRP、SMTP、工作区等外部系统交互

### 3.2 禁止职责混乱
禁止将以下逻辑胡乱混在一起：

- 在 View 中堆积完整业务流程
- 在 Serializer 中做复杂查询与副作用操作
- 在 Model `save()` 中触发高风险外部动作
- 绕过 IAM 直接放行敏感操作
- 在高风险模块中省略审计
- 把长耗时任务直接塞进同步请求
- 把配置解析散落在多个模块中

### 3.3 模块边界基线
默认按以下模块边界实现：

- `core`
- `accounts`
- `iam`
- `audit`
- `system_config`
- `notifications`
- `media_center`
- `blog`
- `wiki`
- `storage`
- `temp_transfer`
- `network_tools`
- `frp_manager`
- `ssh_gateway`
- `mc_manager`
- `mail_center`
- `dev_workspace`

未经明确要求，不跨模块直接侵入对方内部实现。

### 3.4 IAM 专项约束
权限模型基线：

- 角色：`owner`、`admin`、`trusted`、`user`、`guest`
- 角色权限可修改
- 用户权限覆盖角色权限
- 覆盖支持 `allow` / `deny`
- 后续允许扩展资源级策略

禁止：

- 在业务代码中散落 `if is_admin` 式硬编码
- 前端放行而后端不校验
- 通过隐藏按钮代替后端权限控制
- 绕过权限解析器直接访问敏感服务

### 3.5 审计专项约束
以下动作必须可审计：

- 角色与权限变更
- 用户封禁、启用、提权
- 文件删除、恢复、分享
- SSH 会话创建与关闭
- FRP 配置变更
- 邮件账号与模板变更
- 工作区启动、停止、销毁
- Minecraft 实例控制
- 系统配置修改

### 3.6 高风险模块默认原则
涉及以下模块时：

- `ssh_gateway`
- `frp_manager`
- `mail_center`
- `dev_workspace`
- `mc_manager`
- `network_tools`
- `system_config`
- `iam`

必须优先：

- 参数校验
- 权限校验
- 审计记录
- 幂等处理
- 超时控制
- 明确错误返回
- 尽量可回滚

---

## 4. Python 与 Django 代码规范

### 4.1 规范来源
优先遵循：

- PEP 8
- Django / DRF 官方实践
- Celery / Channels 官方实践
- 仓库既有约定

### 4.2 类型要求
要求：

- 公共函数参数必须有类型注解
- 公共函数返回值必须有类型注解
- Serializer 输入输出要清晰
- Service 输入输出要清晰
- 避免使用 `Any`
- 确有必要使用宽泛类型时，必须说明原因

### 4.3 命名要求
禁止无语义命名：

- `var`
- `tmp`
- `temp`
- `foo`
- `bar`
- `data`
- `obj`
- `res`
- `ret`

名称必须体现职责，例如：

- `UserPermissionResolver`
- `CreateSshSessionService`
- `StorageShareSelector`
- `UpdateRolePermissionsService`

### 4.4 未完成实现
默认不保留：

- `pass`
- 空 service
- 空 selector
- 未接线 permission class
- 未接线 task
- 假成功返回
- 高风险动作的占位实现

若确有必要，使用 `TODO:` / `FIXME:` 并说明原因与影响。

---

## 5. 数据与服务专项规则

### 5.1 PostgreSQL
适合放：

- 用户、资料、角色、权限、覆盖、策略
- 审计日志
- 系统配置
- 博客、Wiki、评论、附件元数据
- 文件与分享元数据
- 主机、隧道、实例、工作区元数据
- 邮件账号与发件记录
- 任务记录与状态

### 5.2 Redis
适合放：

- 缓存
- Celery 队列
- 节流
- 锁
- 短期状态
- WebSocket 辅助状态

### 5.3 文件存储
适合放：

- 上传文件
- 媒体资源
- 临时传输对象
- 备份产物
- 缩略图或派生文件

文件二进制不要直接塞进 PostgreSQL，除非任务明确要求。

### 5.4 长耗时动作
以下动作优先走异步任务：

- 文件扫描
- 缩略图生成
- 大文件处理
- 邮件批量发送
- 备份
- 服务状态轮询
- 日志整理
- 远程操作后的状态同步

### 5.5 实时通道
以下能力优先走 Channels / WebSocket：

- SSH 终端输出
- Minecraft 控制台输出
- 长任务进度
- 服务状态流式刷新

---

## 6. 查询与性能规则

### 6.1 查询
- 列表接口优先分页
- 热路径关注索引
- 避免 N+1 查询
- 不在循环中隐式访问数据库
- Selector 负责读聚合，Service 负责写编排

### 6.2 事务
- 事务边界必须清晰
- 不把外部网络调用包进长事务
- 需要一致性的写操作用受控事务
- 高风险动作失败时必须明确返回部分成功或回滚结果

### 6.3 配置与密钥
- 凭据只从配置读取
- 不写死在代码里
- 不回显到日志、异常、API 响应
- 修改配置相关逻辑时检查 `.env.example` 与文档是否需要同步

---

## 7. API 与文档同步检查

提交前自查：

- 是否影响 `/api/v1/` 契约
- 是否需要更新 `docs/api/openapi.yaml`
- 是否需要更新 `docs/architecture/api-design.md`
- 是否需要更新 `docs/architecture/iam-design.md`
- 是否需要更新 `docs/backend/django-apps.md`
- 是否需要更新 `docs/backend/models.md`

---

## 8. 测试与验证

后端改动优先验证：

- 单元测试
- 关键接口测试
- 权限测试
- 审计写入测试
- 高风险模块的失败路径测试
- 序列化与校验测试
- 异步任务触发与状态测试

涉及迁移时，还必须验证：

- 迁移可执行
- 回滚路径清楚
- 旧数据兼容性明确

---

## 9. 结果说明要求

完成后端任务后必须说明：

- 改了哪些 Model、Serializer、View、Service、Selector、Task、Consumer、Permission 模块
- 是否影响 API 契约
- 是否影响 PostgreSQL、Redis、文件存储
- 是否影响角色、权限、覆盖、审计
- 是否影响高风险服务模块
- 是否使用了外部工具
- 当前 `AI_PERMISSION_LEVEL`
- 是否执行高权限动作
- 本次 commit 列表
- 更新了哪些 `docs/`
- 做了哪些验证
- 风险项

---

## 10. 完成定义

后端任务完成时必须满足：

- 分层清晰
- IAM 边界未被破坏
- 审计未被绕过
- API 契约未被意外破坏
- 数据职责未被混淆
- 高风险模块具备必要保护
- 类型、命名、错误处理达标
- 当前块内容已 commit
- 相关 `docs/` 已更新
- 最终内容无过程性残留表达