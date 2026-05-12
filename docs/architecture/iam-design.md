# IAM 设计文档

> 权限模型：角色 + 用户覆盖 + 资源级策略

---

## 1. 设计目标

- 比 Django 内置 Group/Permission 更灵活
- 支持角色模板可编辑
- 支持用户级 allow/deny 覆盖
- 支持资源级策略扩展
- 可审计、可调试

---

## 2. 三层权限模型

```
第一层：权限定义（Permission）
    └── 描述"谁可以对什么做什么"的元数据

第二层：角色与用户组（Role）
    └── 权限的集合，按职责分配

第三层：用户覆盖（User Override）
    └── 对个别用户做 allow/deny 级别的精确控制
```

### 2.1 权限定义

权限码格式：`{module}.{resource}.{action}`

示例：
- `blog.post.create`
- `blog.post.publish`
- `ssh.host.connect`
- `iam.role.assign`
- `system.config.update`

### 2.2 预置角色

| 角色    | 定位                             |
| ------- | -------------------------------- |
| owner   | 站点所有者，拥有一切权限         |
| admin   | 管理员，管理用户和大部分配置     |
| trusted | 受信用户，可使用高级功能         |
| user    | 普通注册用户                     |
| guest   | 访客，仅可访问公开内容           |

角色可自定义编辑，预置角色可覆盖权限配置。

### 2.3 用户覆盖

- 对某个用户，在角色基础上额外 `allow` 或 `deny` 特定权限
- `deny` 优先于 `allow`（黑名单优先）

### 2.4 第三方登录身份

- 账号认证中心支持 provider 化 OAuth 登录，当前已接线 GitHub。
- GitHub OAuth 回调由前端接收 `code/state` 后提交给后端完成换取 token，GitHub `client_secret` 只保存在后端环境变量中。
- 后端保存 `user_oauth_accounts` 绑定关系：`provider`、`provider_account_id`、第三方用户名、昵称、邮箱、头像和原始资料快照。
- 第三方账号首次登录时，如果未找到 `UNIQUE(provider, provider_account_id)` 对应绑定，后端返回待选择状态，前端让用户选择绑定已有账号或创建新账号。
- 不能仅凭第三方邮箱相同自动绑定已有账号；邮箱相同只能作为提示，绑定前必须登录已有账号确认控制权。
- 登录成功后仍签发项目自己的 JWT，并继续使用 IAM 解析最终权限。

---

## 3. 权限检查流程

```
请求到达
  │
  ▼
① owner 角色？ ──▶ 是 ──▶ 放行
  │
  ▼
② 用户已禁用？ ──▶ 是 ──▶ 拒绝
  │
  ▼
③ 用户 deny 覆盖命中？ ──▶ 是 ──▶ 拒绝
  │
  ▼
④ 用户 allow 覆盖命中？ ──▶ 是 ──▶ 放行
  │
  ▼
⑤ 角色权限包含？ ──▶ 是 ──▶ 放行
  │
  ▼
⑥ 资源级策略命中？ ──▶ 是 ──▶ 按策略决定
  │
  ▼
⑦ 默认拒绝
```

---

## 4. 数据模型

### 4.1 permissions（权限定义）

| 字段        | 类型     | 说明              |
| ----------- | -------- | ----------------- |
| id          | UUID     | 主键              |
| code        | VARCHAR  | 权限码（唯一）    |
| name        | VARCHAR  | 显示名称          |
| module      | VARCHAR  | 所属模块          |
| resource    | VARCHAR  | 资源类型          |
| action      | VARCHAR  | 操作类型          |
| description | TEXT     | 描述              |
| is_active   | BOOLEAN  | 是否启用          |

### 4.2 roles（角色）

| 字段        | 类型     | 说明              |
| ----------- | -------- | ----------------- |
| id          | UUID     | 主键              |
| name        | VARCHAR  | 角色名（唯一）    |
| display_name| VARCHAR  | 显示名称          |
| description | TEXT     | 描述              |
| is_system   | BOOLEAN  | 是否系统预置      |
| level       | INTEGER  | 权限等级          |

### 4.3 role_permissions（角色-权限关联）

| 字段          | 类型 | 说明     |
| ------------- | ---- | -------- |
| id            | UUID | 主键     |
| role_id       | FK   | 角色     |
| permission_id | FK   | 权限     |

### 4.4 user_roles（用户-角色关联）

| 字段    | 类型 | 说明     |
| ------- | ---- | -------- |
| id      | UUID | 主键     |
| user_id | FK   | 用户 `uid` |
| role_id | FK   | 角色     |

### 4.5 user_permission_overrides（用户权限覆盖）

| 字段          | 类型    | 说明                    |
| ------------- | ------- | ----------------------- |
| id            | UUID    | 主键                    |
| user_id       | FK      | 用户 `uid`              |
| permission_id | FK      | 权限                    |
| effect        | VARCHAR | `allow` 或 `deny`       |
| reason        | TEXT    | 覆盖原因                |

### 4.6 resource_policies（资源级策略）

| 字段          | 类型    | 说明                       |
| ------------- | ------- | -------------------------- |
| id            | UUID    | 主键                       |
| resource_type | VARCHAR | 资源类型（如 blog_post）   |
| resource_id   | UUID    | 资源 ID                    |
| subject_type  | VARCHAR | 主体类型（user / role）    |
| subject_id    | VARCHAR | 主体 ID，用户为 `uid`，角色为 UUID |
| permission_id | FK      | 权限                       |
| effect        | VARCHAR | `allow` 或 `deny`          |

### 4.7 audit_logs（审计日志）

| 字段        | 类型      | 说明             |
| ----------- | --------- | ---------------- |
| id          | UUID      | 主键             |
| user_id     | FK        | 操作人 `uid`     |
| action      | VARCHAR   | 操作类型         |
| module      | VARCHAR   | 模块             |
| resource    | VARCHAR   | 资源描述         |
| detail      | JSON      | 操作详情         |
| ip_address  | INET      | IP 地址          |
| user_agent  | TEXT      | UA               |
| created_at  | TIMESTAMP | 创建时间         |

---

## 5. 后端实现建议

### 5.1 DRF Permission Class

```python
class RequirePermission(BasePermission):
    """通用权限类，子类设置 required_permission"""
    required_permission: str = ""

    def has_permission(self, request, view):
        if not self.required_permission:
            return True
        return PermissionResolver.has_permission(
            user=request.user,
            permission_code=self.required_permission,
        )
```

### 5.2 装饰器

```python
@require_permission("blog.post.publish")
def publish_post(request, post_id):
    ...
```

### 5.3 PermissionResolver

```python
class PermissionResolver:
    @staticmethod
    def resolve_user_permissions(user, resource=None) -> set[str]:
        """解析用户最终权限集"""
        ...

    @staticmethod
    def has_permission(user, permission_code, resource=None) -> bool:
        """检查用户是否拥有某权限"""
        ...
```

---

## 6. 前端权限控制

前端**不负责安全**，只负责体验优化：

1. 登录后拉取 `GET /api/v1/iam/me/permissions/` 获取角色与权限列表
2. 前端路由、菜单和按钮使用与后端一致的 `{module}.{resource}.{action}` 权限码，例如 `accounts.user.view`、`iam.role.view`、`audit.log.view`
3. 根据权限列表控制：
   - 菜单显示/隐藏
   - 按钮启用/禁用
   - 路由守卫体验优化
4. 403 状态必须有明确的提示页面
5. 真正的安全校验以后端为准

---

## 7. 必须审计的操作

| 操作类型               | 说明                     |
| ---------------------- | ------------------------ |
| 角色创建/编辑/删除     | IAM 变更                 |
| 权限分配/撤销          | IAM 变更                 |
| 用户覆盖创建/修改/删除 | IAM 变更                 |
| 用户封禁/解封          | 账户管理                 |
| 文件上传/删除/分享     | 存储操作                 |
| SSH 会话创建/关闭      | 高风险基础设施           |
| FRP 隧道启停           | 高风险基础设施           |
| MC 服务启停/备份       | 高风险基础设施           |
| 邮件发送配置变更       | 高风险通信               |
| 系统配置变更           | 全局影响                 |
| 模块开关变更           | 全局影响                 |
