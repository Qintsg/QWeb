# 前端设计系统

> 基于 Fluent 2 Design System 的前端 UI 规范

---

## 1. 设计基线

- **设计系统**：Microsoft Fluent 2 Design System
- **实现方式**：基于 Fluent 2 的 Design Token 自行开发 Vue 组件，或使用社区 Fluent Vue 库
- **核心文件**：
  - `src/styles/tokens.css` — Fluent 2 Design Token 定义
  - `src/styles/theme.css` — 主题配置（浅色/深色）
  - `src/styles/fluent2.css` — 全局 Fluent 2 基础样式

根目录 `index.html` 是独立部署的静态首页，不能消费 Vue 运行时或 `src/styles/tokens.css`。该文件以内联 CSS 复用当前 Fluent 2 视觉基线：青色品牌色、暖橙强调色、暖色中性画布、8px 卡片圆角、清晰焦点态与响应式网格。

---

## 2. 组件目录结构

```text
src/components/
├─ ui/                # 通用 UI 组件（按钮、输入、卡片、弹窗等）
├─ business/          # 业务组件（文件卡片、权限选择器等）
└─ layout/            # 布局组件（导航、侧边栏、面包屑等）
```

---

## 3. 布局系统

| Layout | 使用场景 | 特征 |
|--------|----------|------|
| `PublicLayout.vue` | 首页、博客列表、公开页面 | 轻量顶栏 + 内容区 |
| `DashboardLayout.vue` | 用户工作区、业务模块 | 侧边导航 + 顶栏 + 内容区 |
| `AdminLayout.vue` | 管理后台 | 管理专用侧边导航 + 内容区 |

---

## 4. Token 使用规范

### 4.1 颜色

- 使用 Fluent 2 语义化 Token，不直接使用 hex 值
- 支持浅色/深色主题切换
- 品牌色通过 Token 统一定义

### 4.2 间距

- 使用 Fluent 2 标准间距 Token（`--spacingHorizontalS`, `--spacingVerticalM` 等）
- 不使用魔法数字

### 4.3 排版

- 字体族、字号、行高使用 Fluent 2 排版 Token
- 标题层级与 Fluent 2 Type Ramp 对齐

### 4.4 圆角与阴影

- 圆角使用 `--borderRadiusMedium` 等 Token
- 阴影使用 Fluent 2 Elevation Token

---

## 5. 页面区域与权限展示

### 5.1 页面权限控制原则

- **前端不负责安全，只负责体验优化**
- 真正校验必须以后端为准
- 前端在登录后拉取用户权限列表，控制：
  - 菜单项显示/隐藏
  - 按钮启用/禁用
  - 路由访问体验

### 5.2 权限数据流

```text
用户登录 → 获取 JWT → 拉取用户信息 + 权限列表
→ 存入 Pinia (auth store + permission store)
→ 路由守卫读取权限 → 组件根据权限条件渲染
```

### 5.3 权限指令（建议）

```vue
<!-- 有权限时显示 -->
<button v-permission="'blog.post.publish'">发布文章</button>

<!-- 无权限时禁用 -->
<button v-permission:disable="'admin.users.delete'">删除用户</button>
```

---

## 6. 状态管理

### 6.1 Store 划分

```text
src/stores/
├─ auth.ts            # 认证状态（token、登录/登出）
├─ app.ts             # 应用全局状态（主题、语言、侧边栏）
├─ permission.ts      # 权限缓存（角色、权限列表）
└─ notification.ts    # 通知状态
```

### 6.2 API 层

```text
src/api/
├─ client.ts          # Axios/ofetch 实例（统一拦截器、JWT 注入、错误处理）
├─ auth.ts            # 认证相关 API
├─ users.ts           # 用户相关 API
├─ iam.ts             # IAM 相关 API
├─ blog.ts            # 博客 API
├─ wiki.ts            # Wiki API
├─ storage.ts         # 存储 API
├─ ssh.ts             # SSH API
├─ frp.ts             # FRP API
├─ network.ts         # 网络工具 API
├─ mc.ts              # MC 管理 API
├─ mail.ts            # 邮件 API
├─ dev.ts             # 开发工作区 API
└─ system.ts          # 系统配置/审计 API
```

### 6.3 Composables

```text
src/composables/
├─ useAuth.ts         # 认证相关组合函数
├─ usePermission.ts   # 权限判断组合函数
├─ useTheme.ts        # 主题切换
├─ usePagination.ts   # 分页逻辑
└─ useWebSocket.ts    # WebSocket 连接管理
```
