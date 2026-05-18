# API 设计规范

> RESTful + JWT + 统一响应 + WebSocket

---

## 1. 基本约定

| 项目       | 规范                              |
| ---------- | --------------------------------- |
| 前缀       | `/api/v1/`                        |
| 认证       | JWT Bearer Token                  |
| 格式       | JSON                              |
| 风格       | RESTful                           |
| 实时       | WebSocket（`/ws/`）               |
| 文档       | `docs/openapi/openapi.yaml` 分文件维护，运行时 `/api/schema/` 由 drf-spectacular 提供 |

---

## 2. 统一响应格式

### 成功

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

### 失败

```json
{
  "code": 4001,
  "message": "permission denied",
  "errors": {
    "permission": ["blog.post.publish"]
  }
}
```

### 分页列表

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "results": [],
    "count": 100,
    "next": "...",
    "previous": "..."
  }
}
```

---

## 3. HTTP 方法约定

| 方法   | 用途               | 幂等 |
| ------ | ------------------ | ---- |
| GET    | 获取资源           | 是   |
| POST   | 创建资源 / 触发动作| 否   |
| PATCH  | 部分更新资源       | 是   |
| PUT    | 全量替换关联       | 是   |
| DELETE | 删除资源           | 是   |

---

## 4. 状态码约定

| 状态码 | 含义               |
| ------ | ------------------ |
| 200    | 成功               |
| 201    | 创建成功           |
| 204    | 删除成功           |
| 400    | 请求参数错误       |
| 401    | 未认证             |
| 403    | 权限不足           |
| 404    | 资源不存在         |
| 409    | 资源冲突           |
| 422    | 数据校验失败       |
| 429    | 请求过于频繁       |
| 500    | 服务端错误         |

---

## 5. 接口总览

### 5.1 认证（Auth）

| 方法 | 路径                              | 说明         |
| ---- | --------------------------------- | ------------ |
| GET  | /api/v1/auth/bootstrap/status       | 查询首次部署是否需要创建站长账号 |
| POST | /api/v1/auth/bootstrap/owner        | 首次部署创建站长账号并授予 owner 角色 |
| POST | /api/v1/auth/register             | 注册本地账号，并创建用户扩展表 |
| POST | /api/v1/auth/login                | 用户名、邮箱或手机号 + 密码登录 |
| GET  | /api/v1/auth/oauth/{provider}/authorize | 获取 OAuth 授权地址，当前支持 `github` |
| POST | /api/v1/auth/oauth/{provider}/callback | OAuth 回调；已绑定则返回 Token，未绑定则返回待选择状态 |
| POST | /api/v1/auth/oauth/{provider}/bind | 登录已有账号并绑定第三方账号 |
| POST | /api/v1/auth/oauth/{provider}/register | 使用第三方资料创建新账号并绑定 |
| POST | /api/v1/auth/logout               | 登出         |
| POST | /api/v1/auth/token/refresh        | 刷新 Token   |
| POST | /api/v1/auth/verify-email         | 邮箱验证     |
| POST | /api/v1/auth/resend-verification  | 重发验证码   |
| POST | /api/v1/auth/forgot-password      | 忘记密码     |
| POST | /api/v1/auth/reset-password       | 重置密码     |

旧 `/api/v1/auth/github/authorize`、`/api/v1/auth/github/callback` 已删除，统一使用 provider 化 OAuth 接口。旧 `/api/v1/auth/change-password` 已删除，统一使用 `/api/v1/me/password`。

### 5.2 当前用户（Me）

| 方法  | 路径                    | 说明         |
| ----- | ----------------------- | ------------ |
| GET   | /api/v1/me              | 当前用户信息，包含 contact/profile/settings |
| PUT/PATCH | /api/v1/me          | 更新昵称、头像、联系方式、资料与设置 |
| POST/PUT | /api/v1/me/password | 修改密码     |
| GET   | /api/v1/iam/me/permissions | 权限列表 |
| GET   | /api/v1/me/roles        | 角色信息     |
| GET   | /api/v1/me/activity     | 活动记录     |

### 5.3 IAM

| 方法   | 路径                                        | 说明             |
| ------ | ------------------------------------------- | ---------------- |
| GET    | /api/v1/iam/roles                           | 角色列表         |
| POST   | /api/v1/iam/roles                           | 创建角色         |
| GET    | /api/v1/iam/roles/{id}                      | 角色详情         |
| PATCH  | /api/v1/iam/roles/{id}                      | 更新角色         |
| DELETE | /api/v1/iam/roles/{id}                      | 删除角色         |
| GET    | /api/v1/iam/roles/{id}/permissions          | 角色权限         |
| PUT    | /api/v1/iam/roles/{id}/permissions          | 设置角色权限     |
| GET    | /api/v1/iam/permissions                     | 权限列表         |
| POST   | /api/v1/iam/permissions                     | 创建权限         |
| GET    | /api/v1/iam/permissions/{id}                | 权限详情         |
| PATCH  | /api/v1/iam/permissions/{id}                | 更新权限         |
| GET    | /api/v1/iam/users/{uid}/roles               | 用户角色         |
| POST   | /api/v1/iam/users/{uid}/roles/manage        | 分配用户角色     |
| DELETE | /api/v1/iam/users/{uid}/roles/manage        | 移除用户角色     |
| GET    | /api/v1/iam/users/{uid}/overrides           | 用户覆盖列表     |
| POST   | /api/v1/iam/users/{uid}/overrides/manage    | 创建用户覆盖     |
| DELETE | /api/v1/iam/users/{uid}/overrides/manage    | 移除用户覆盖     |
| GET    | /api/v1/iam/resource-policies               | 资源策略列表     |
| POST   | /api/v1/iam/resource-policies               | 创建资源策略     |
| PATCH  | /api/v1/iam/resource-policies/{id}          | 修改资源策略     |
| DELETE | /api/v1/iam/resource-policies/{id}          | 删除资源策略     |

### 5.4 用户管理

| 方法 | 路径                         | 说明         |
| ---- | ---------------------------- | ------------ |
| GET  | /api/v1/users                | 用户列表     |
| GET  | /api/v1/users/{uid}          | 用户详情     |
| PATCH| /api/v1/users/{uid}          | 更新用户     |
| POST | /api/v1/users/{uid}/toggle-active | 启用或禁用 |

用户响应主键字段为 `uid`。用户资料分为 `contact`、`profile`、`settings` 三组嵌套字段，邮箱和手机号不再位于用户核心对象顶层。

### 5.5 博客

| 方法   | 路径                              | 说明         |
| ------ | --------------------------------- | ------------ |
| GET    | /api/v1/blog/posts                | 文章列表     |
| POST   | /api/v1/blog/posts                | 创建文章     |
| GET    | /api/v1/blog/posts/{slug}         | 文章详情     |
| PATCH  | /api/v1/blog/posts/{id}           | 更新文章     |
| DELETE | /api/v1/blog/posts/{id}           | 删除文章     |
| POST   | /api/v1/blog/posts/{id}/publish   | 发布         |
| POST   | /api/v1/blog/posts/{id}/unpublish | 撤回         |
| GET    | /api/v1/blog/categories           | 分类列表     |
| POST   | /api/v1/blog/categories           | 创建分类     |
| GET    | /api/v1/blog/tags                 | 标签列表     |
| POST   | /api/v1/blog/tags                 | 创建标签     |

### 5.6 Wiki

| 方法   | 路径                                     | 说明            |
| ------ | ---------------------------------------- | --------------- |
| GET    | /api/v1/wiki/spaces                      | 空间列表        |
| POST   | /api/v1/wiki/spaces                      | 创建空间        |
| GET    | /api/v1/wiki/spaces/{id}                 | 空间详情        |
| PATCH  | /api/v1/wiki/spaces/{id}                 | 更新空间        |
| GET    | /api/v1/wiki/pages                       | 页面列表        |
| POST   | /api/v1/wiki/pages                       | 创建页面        |
| GET    | /api/v1/wiki/pages/{id}                  | 页面详情        |
| PATCH  | /api/v1/wiki/pages/{id}                  | 更新页面        |
| DELETE | /api/v1/wiki/pages/{id}                  | 删除页面        |
| GET    | /api/v1/wiki/pages/{id}/history          | 版本历史        |
| POST   | /api/v1/wiki/pages/{id}/restore-version  | 恢复版本        |

### 5.7 云盘

| 方法   | 路径                                | 说明         |
| ------ | ----------------------------------- | ------------ |
| GET    | /api/v1/storage/files               | 文件列表     |
| POST   | /api/v1/storage/files/upload        | 上传文件     |
| GET    | /api/v1/storage/files/{id}          | 文件详情     |
| DELETE | /api/v1/storage/files/{id}          | 删除文件     |
| POST   | /api/v1/storage/files/{id}/move     | 移动         |
| POST   | /api/v1/storage/files/{id}/copy     | 复制         |
| POST   | /api/v1/storage/files/{id}/share    | 分享         |
| POST   | /api/v1/storage/files/{id}/restore  | 恢复         |
| GET    | /api/v1/storage/folders             | 文件夹列表   |
| POST   | /api/v1/storage/folders             | 创建文件夹   |
| PATCH  | /api/v1/storage/folders/{id}        | 更新文件夹   |
| DELETE | /api/v1/storage/folders/{id}        | 删除文件夹   |
| GET    | /api/v1/storage/shares              | 分享列表     |
| DELETE | /api/v1/storage/shares/{id}         | 取消分享     |

### 5.8 临时传输

| 方法   | 路径                                  | 说明         |
| ------ | ------------------------------------- | ------------ |
| POST   | /api/v1/temp-transfer/upload          | 上传         |
| GET    | /api/v1/temp-transfer/tasks           | 任务列表     |
| GET    | /api/v1/temp-transfer/tasks/{id}      | 任务详情     |
| DELETE | /api/v1/temp-transfer/tasks/{id}      | 删除任务     |
| POST   | /api/v1/temp-transfer/tasks/{id}/expire| 手动过期    |
| GET    | /api/v1/public/temp-transfer/{token}  | 公开下载     |

### 5.9 SSH 网关

| 方法 | 路径                                | 说明         |
| ---- | ----------------------------------- | ------------ |
| GET  | /api/v1/ssh/hosts                   | 主机列表     |
| POST | /api/v1/ssh/hosts                   | 添加主机     |
| GET  | /api/v1/ssh/hosts/{id}              | 主机详情     |
| PATCH| /api/v1/ssh/hosts/{id}              | 更新主机     |
| DELETE| /api/v1/ssh/hosts/{id}             | 删除主机     |
| POST | /api/v1/ssh/sessions                | 创建会话     |
| GET  | /api/v1/ssh/sessions                | 会话列表     |
| GET  | /api/v1/ssh/sessions/{id}           | 会话详情     |
| POST | /api/v1/ssh/sessions/{id}/close     | 关闭会话     |
| WS   | /ws/ssh/sessions/{id}               | 终端通道     |

### 5.10 FRP 隧道

| 方法   | 路径                               | 说明         |
| ------ | ---------------------------------- | ------------ |
| GET    | /api/v1/frp/tunnels                | 隧道列表     |
| POST   | /api/v1/frp/tunnels                | 创建隧道     |
| GET    | /api/v1/frp/tunnels/{id}           | 隧道详情     |
| PATCH  | /api/v1/frp/tunnels/{id}           | 更新隧道     |
| DELETE | /api/v1/frp/tunnels/{id}           | 删除隧道     |
| POST   | /api/v1/frp/tunnels/{id}/enable    | 启用         |
| POST   | /api/v1/frp/tunnels/{id}/disable   | 禁用         |
| GET    | /api/v1/frp/clients                | 客户端列表   |
| GET    | /api/v1/frp/stats                  | 统计         |

### 5.11 网络工具

| 方法 | 路径                              | 说明         |
| ---- | --------------------------------- | ------------ |
| POST | /api/v1/network/speed-tests       | 发起测速     |
| GET  | /api/v1/network/speed-tests       | 测速记录     |
| GET  | /api/v1/network/speed-tests/{id}  | 测速详情     |
| POST | /api/v1/network/ping              | Ping         |
| POST | /api/v1/network/port-check        | 端口检测     |

### 5.12 Minecraft

| 方法 | 路径                                   | 说明         |
| ---- | -------------------------------------- | ------------ |
| GET  | /api/v1/mc/servers                     | 服务列表     |
| POST | /api/v1/mc/servers                     | 创建服务     |
| GET  | /api/v1/mc/servers/{id}                | 服务详情     |
| PATCH| /api/v1/mc/servers/{id}                | 更新配置     |
| POST | /api/v1/mc/servers/{id}/start          | 启动         |
| POST | /api/v1/mc/servers/{id}/stop           | 停止         |
| POST | /api/v1/mc/servers/{id}/restart        | 重启         |
| GET  | /api/v1/mc/servers/{id}/players        | 在线玩家     |
| GET  | /api/v1/mc/servers/{id}/logs           | 日志         |
| POST | /api/v1/mc/servers/{id}/backup         | 备份         |
| WS   | /ws/mc/servers/{id}/console            | 控制台       |

### 5.13 邮件

| 方法   | 路径                         | 说明         |
| ------ | ---------------------------- | ------------ |
| GET    | /api/v1/mail/accounts        | 邮箱列表     |
| POST   | /api/v1/mail/accounts        | 添加邮箱     |
| PATCH  | /api/v1/mail/accounts/{id}   | 更新邮箱     |
| DELETE | /api/v1/mail/accounts/{id}   | 删除邮箱     |
| GET    | /api/v1/mail/templates       | 模板列表     |
| POST   | /api/v1/mail/templates       | 创建模板     |
| POST   | /api/v1/mail/send            | 发送邮件     |
| GET    | /api/v1/mail/logs            | 发送记录     |

### 5.14 远程开发

| 方法 | 路径                                    | 说明         |
| ---- | --------------------------------------- | ------------ |
| GET  | /api/v1/dev/workspaces                  | 工作区列表   |
| POST | /api/v1/dev/workspaces                  | 创建工作区   |
| GET  | /api/v1/dev/workspaces/{id}             | 工作区详情   |
| PATCH| /api/v1/dev/workspaces/{id}             | 更新工作区   |
| POST | /api/v1/dev/workspaces/{id}/start       | 启动         |
| POST | /api/v1/dev/workspaces/{id}/stop        | 停止         |
| GET  | /api/v1/dev/workspaces/{id}/status      | 状态         |
| GET  | /api/v1/dev/workspaces/{id}/access      | 接入信息     |

### 5.15 审计

| 方法 | 路径                           | 说明         |
| ---- | ------------------------------ | ------------ |
| GET  | /api/v1/audit/logs             | 操作日志     |
| GET  | /api/v1/audit/logins           | 登录日志     |
| GET  | /api/v1/audit/security-events  | 安全事件     |

### 5.16 系统配置

| 方法  | 路径                            | 说明         |
| ----- | ------------------------------- | ------------ |
| GET   | /api/v1/system/config           | 获取配置     |
| PATCH | /api/v1/system/config           | 更新配置     |
| GET   | /api/v1/system/modules          | 模块列表     |
| PATCH | /api/v1/system/modules/{code}   | 模块开关     |
