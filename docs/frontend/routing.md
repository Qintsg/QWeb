# 前端路由规划

> Vue Router 4 路由结构与权限守卫

---

## 1. 路由区域划分

| 区域 | Layout | 认证要求 | 说明 |
|------|--------|----------|------|
| 公开区 | `PublicLayout` | 无 | 首页、关于、博客列表等 |
| 认证区 | 无（独立页面） | 未登录 | 登录、注册、忘记密码 |
| 用户工作区 | `DashboardLayout` | 登录 | 仪表盘、个人设置、业务模块 |
| 管理后台 | `AdminLayout` | 登录 + 管理员权限 | 系统配置、审计日志、用户管理 |

### 1.1 静态公开首页

仓库根目录 `index.html` 是面向 `qintsg.cn` 与 `www.qintsg.cn` 的静态公开首页。

- 不依赖 Vue Router、登录态、后台管理或后端 API。
- 服务入口数据由当前数据库 `homepage_service_link` 可见记录固化生成。
- 卡片跳转使用普通 `<a>` 外链，打开对应服务域名。
- `frontend/index.html` 仍是 Vite 应用入口，二者部署职责分离。

---

## 2. 路由树

```text
/                           # 公开首页
/about                      # 关于页
/blog                       # 博客列表（公开）
/blog/:slug                 # 博客详情（公开）
/wiki                       # Wiki 首页（公开/部分）
/wiki/:slug                 # Wiki 页面

/bootstrap/owner             # 首次部署创建站长账号
/auth/login                 # 登录
/auth/register              # 注册
/auth/forgot-password       # 忘记密码
/auth/reset-password        # 重置密码
/auth/github/callback       # GitHub OAuth 回调与首次绑定/注册选择

/dashboard                  # 仪表盘首页
/dashboard/profile          # 个人资料
/dashboard/security         # 安全设置

/storage                    # 文件管理
/storage/shared/:token      # 分享链接访问
/transfer                   # 临时传输
/transfer/:token            # 临时取件

/blog/editor                # 文章编辑器（需权限）
/blog/manage                # 文章管理（需权限）
/wiki/editor/:slug?         # Wiki 编辑器（需权限）

/ssh                        # SSH 管理
/ssh/sessions/:id           # SSH 终端

/frp                        # FRP 管理
/network                    # 网络工具
/mc                         # MC 管理
/mc/servers/:id/console     # MC 控制台

/mail                       # 邮件中心
/dev                        # 开发工作区

/admin                      # 管理后台首页
/admin/users                # 用户管理
/admin/roles                # 角色管理
/admin/permissions          # 权限管理
/admin/audit                # 审计日志
/admin/config               # 站点设置、系统配置与模块开关
/admin/notifications        # 通知管理
```

---

### 2.1 认证路由约定

- 首次部署时，前端先调用 `/api/v1/auth/bootstrap/status/`；若后端返回需要创建站长账号，则所有路由优先重定向到 `/bootstrap/owner`。
- `/bootstrap/owner` 提交 `/api/v1/auth/bootstrap/owner/` 创建第一个站长账号并授予 `owner` 角色；一旦已有 owner 用户，该公开入口关闭。
- GitHub 回调页统一承载三种状态：已绑定登录成功、未绑定时选择绑定已有账号、未绑定时创建新账号。
- 前端统一调用 provider 化接口 `/api/v1/auth/oauth/{provider}/...`，当前仅接线 `github`；旧 `/api/v1/auth/github/...` 后端入口已删除。
- 第三方邮箱相同只能用于提示用户，不作为自动绑定依据；绑定已有账号必须完成本地账号认证。

---

## 3. 路由守卫

### 3.1 全局前置守卫

```text
router.beforeEach:
1. 调用后端首次部署状态接口；如需要创建站长账号，优先重定向 /bootstrap/owner
2. 检查目标路由 meta.requiresAuth
3. 未登录 → 重定向 /auth/login?redirect=目标路径
4. 已登录访问 /auth/* 或 /bootstrap/owner → 重定向 /dashboard
5. 检查目标路由 meta.permission，权限码使用 `{module}.{resource}.{action}` 格式，与后端 IAM 保持一致
6. 权限不足 → 重定向 /403，并保留来源路径
7. 检查目标路由 meta.requiredModule
8. 模块已关闭 → 重定向 /module-disabled
```

### 3.2 路由 Meta 定义

```typescript
interface RouteMeta {
  requiresAuth?: boolean        // 是否需要登录
  permission?: string           // 所需权限码
  requiredModule?: string       // 所需模块开关
  layout?: string               // 使用的 Layout
  title?: string                // 页面标题
}
```

---

## 4. 路由文件组织

```text
src/router/
├─ index.ts           # Router 实例、全局守卫
├─ guards.ts          # 守卫逻辑抽离
└─ routes/            # 按区域拆分路由配置
   ├─ public.ts       # 公开路由
   ├─ auth.ts         # 认证路由
   ├─ dashboard.ts    # 工作区路由
   ├─ blog.ts         # 博客路由
   ├─ wiki.ts         # Wiki 路由
   ├─ storage.ts      # 存储路由
   ├─ tools.ts        # SSH/FRP/网络工具/MC 路由
   ├─ mail.ts         # 邮件路由
   ├─ dev.ts          # 开发工作区路由
   └─ admin.ts        # 管理后台路由
```
