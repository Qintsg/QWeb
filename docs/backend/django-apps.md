# Django Apps 结构与开发规范

> 后端 17 个 Django App 的内部组织模式与开发约定

---

## 1. App 内部推荐结构

每个 Django App 采用统一目录结构，避免大文件堆积：

```text
apps/{app_name}/
├─ apps.py              # App 配置
├─ admin.py             # Admin 注册（可选）
├─ urls.py              # URL 路由
├─ models/              # 模型定义
│  ├─ __init__.py       # 导出所有模型
│  └─ {model_name}.py   # 每个模型一个文件
├─ api/                 # API 层
│  ├─ serializers/      # 序列化器
│  ├─ views/            # ViewSet / APIView
│  └─ filters.py        # django-filter 过滤器
├─ services/            # 业务逻辑
├─ selectors/           # 查询逻辑
├─ permissions/         # 模块权限定义
├─ signals/             # 信号处理
├─ tasks/               # Celery 异步任务
├─ consumers/           # WebSocket Consumer（如有）
├─ integrations/        # 外部集成（如有）
├─ tests/               # 模块测试
└─ migrations/          # 数据库迁移
```

---

## 2. 各层职责

### 2.1 `models/` — 数据层

- 每个模型一个文件，通过 `__init__.py` 统一导出
- 所有业务模型继承 `core.BaseModel`（提供 `created_at`、`updated_at`、`is_deleted`、`created_by`、`updated_by`）
- 模型只定义字段、约束、`__str__`、`Meta`
- 不在模型中写业务逻辑

### 2.2 `api/` — 接口层

- `serializers/`：负责入参校验与输出格式化，不含业务逻辑
- `views/`：ViewSet 或 APIView，负责接收请求、调用 service、返回统一响应
- `filters.py`：基于 `django-filter` 的过滤器定义
- View 中不写复杂业务逻辑，委托给 `services/`

### 2.3 `services/` — 业务层

- 核心业务逻辑全部放在 service 函数/类中
- 接受已验证的数据，执行业务操作，返回结果
- 负责事务管理、权限检查调用、审计日志写入
- 对外是模块间调用的主要入口

### 2.4 `selectors/` — 查询层

- 复杂查询逻辑独立放置
- 提供带过滤、排序、分页的查询函数
- 与 service 分离，避免查询逻辑混入写操作

### 2.5 `permissions/` — 权限层

- 定义本模块的权限码常量
- 实现基于 IAM 的 DRF Permission Class
- 实现装饰器形式的权限检查（可选）

### 2.6 `tasks/` — 异步任务

- Celery 任务定义
- 长耗时操作（邮件发送、文件处理、定时清理等）
- 通过 `@shared_task` 注册

### 2.7 `consumers/` — WebSocket

- 仅 `ssh_gateway`、`mc_manager` 等需要实时通道的模块
- 基于 Django Channels 实现
- 统一走 `/ws/` 前缀路由

---

## 3. 开发规则

### 3.1 分层禁止规则

```
❌ View 中写业务逻辑
❌ Serializer 中调用数据库写操作
❌ Model 中写复杂业务判定
❌ Service 中直接操作 HTTP Request/Response
❌ 跨模块直接 import 对方的 models 内部实现
```

### 3.2 模块间调用

```python
# ✅ 正确：通过 service 调用
from apps.iam.services.permission_resolver import has_permission

# ❌ 错误：直接操作对方内部模型
from apps.iam.models.role import Role
Role.objects.filter(...)
```

### 3.3 数据库查询规范

- 禁止循环内查询（N+1）
- 使用 `select_related` / `prefetch_related` 优化关联查询
- 大结果集必须分页
- 聚合统计优先数据库层完成

### 3.4 API 同步规范

- 所有 API 都要注册到 `drf-spectacular` 生成 OpenAPI 文档
- 统一响应格式 `{code, message, data}`
- 统一分页格式 `{code, message, data: {count, next, previous, results}}`
- 错误响应统一 `{code, message, errors}`

---

## 4. Celery 与 Channels

### 4.1 Celery 异步任务

- Broker：Redis
- 后端：Redis
- 定时任务：Celery Beat
- 典型场景：
  - 邮件发送（`mail_center`）
  - 文件过期清理（`temp_transfer`）
  - MC 服务器备份（`mc_manager`）
  - 大文件处理（`storage`）

### 4.2 Django Channels WebSocket

- 仅用于需要实时双向通信的场景
- 当前规划：
  - `/ws/ssh/sessions/{session_id}` — SSH 终端
  - `/ws/mc/servers/{server_id}/console` — MC 控制台
- Channel Layer：Redis（`channels_redis`）

---

## 5. 测试规范

- 每个 App 独立 `tests/` 目录
- 单元测试覆盖 service 层
- API 测试使用 DRF `APITestCase`
- 权限测试覆盖各角色的允许/拒绝场景
- 测试数据不使用真实凭据
