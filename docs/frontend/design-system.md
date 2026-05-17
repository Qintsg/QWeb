# 前端设计系统

> 基于 Material Design 3 与 `@material/web` 的前端 UI 规范

---

## 1. 设计基线

- **设计系统**：Material Design 3
- **实现方式**：优先使用 `@material/web` custom elements；缺失组件用语义 HTML + Material 3 token 实现。
- **规范来源**：根目录 `DESIGN.md` 是当前 UI 的约束源，包含 token、组件、响应式、无障碍和 Definition of Done。
- **核心文件**：
  - `src/styles/tokens.css` — Material 3 `--md-sys-*` 设计 token、形状、间距、排版、动效与布局 token。
  - `src/styles/material-setup.ts` — 注册 `@material/web` custom elements。
  - `src/style.css` — 最小 reset、全局字体、可访问性辅助类、路由过渡。
  - `vite.config.ts` — 将 `md-*` 标记为 Vue custom element，避免 Vue 把 Material Web 组件解析为本地组件。

根目录 `index.html` 是独立部署的静态公开首页；`frontend/index.html` 是 Vite SPA 宿主入口，已加载 Material Symbols 与 Roboto 字体族。

---

## 2. Token 使用规则

组件和页面样式必须消费语义 token：

- 颜色使用 `--md-sys-color-*`，成对使用背景与 `on-*` 前景。
- 字体使用 `--md-sys-typescale-*`。
- 圆角使用 `--md-sys-shape-corner-*`。
- 间距使用 `--space-*`。
- 动效使用 `--md-sys-motion-*`。
- 层级使用 `--md-sys-color-surface-container-*` 和 `--md-sys-elevation-*`。

组件层不得硬编码 hex、rgb、裸 `px` 字号、任意圆角或任意动效时长。允许使用 `rem`、`clamp()`、`min()`、`max()` 等响应式表达式，但内部值仍应来自 token。

---

## 3. 组件组织

```text
src/components/
├─ common/                 # 当前共享组件与布局基础件
│  ├─ AppHeader.vue
│  ├─ AppIconButton.vue
│  ├─ AppSidebar.vue
│  ├─ PageHeader.vue
│  └─ StatusPill.vue
```

约束：

- 多处复用的 UI 必须抽成共享组件。
- 所有 Vue SFC 使用 `<script setup lang="ts">` 和 `<style scoped>`。
- 交互元素必须使用原生交互元素或 Material Web 交互组件，不用 `div/span` 伪装按钮。
- 图标使用 Material Symbols，不混用图标库。

---

## 4. 布局系统

| Layout | 使用场景 | 当前实现 |
|--------|----------|----------|
| `PublicLayout.vue` | 登录、注册、OAuth 回调 | Material 3 认证壳层、主题/语言切换、一个页面级 `<h1>` |
| `DashboardLayout.vue` | 登录后的工作区与管理页 | Material 3 App Shell、自适应导航、顶部应用栏、路由过渡 |
| `AdminLayout.vue` | 管理后台 | 当前复用 `DashboardLayout` |

`DashboardLayout` 使用 `useWindowSizeClass()`：

- Compact：底部导航。
- Medium / Expanded：导航 rail。
- Large / Extra-large：持久侧边 drawer。

---

## 5. 页面结构与可访问性

- 每个路由视图必须保证页面整体只有一个 `<h1>`。
- `App.vue` 提供 skip link，主要布局中的 `<main id="main-content">` 是跳转目标。
- 表格数据使用原生 `<table>`、`<thead>`、`<tbody>`、`<th scope="col">`。
- 空状态、错误状态、加载状态必须有文本；加载超过短暂时间时使用 `md-circular-progress` 或可见状态文案。
- 所有按钮/链接目标至少满足 48×48 CSS px 可点击目标。
- 动效必须尊重 `prefers-reduced-motion`，全局 reset 已提供兜底。

---

## 6. 状态管理与 API 层

```text
src/api/client.ts          # Axios 实例、JWT 注入、401 refresh
src/stores/auth.ts         # token、当前用户、登录/登出/OAuth
src/stores/permission.ts   # IAM 权限缓存
src/composables/useTheme.ts
src/composables/useWindowSizeClass.ts
```

前端权限只做体验优化；真正安全校验以后端 IAM 为准。路由与按钮使用后端一致的 `{module}.{resource}.{action}` 权限码。

---

## 7. 当前页面重构范围

已迁移为 Material 3 视觉与交互语言的页面：

- `HomePage.vue`
- `LoginPage.vue`
- `RegisterPage.vue`
- `GitHubCallbackPage.vue`
- `DashboardPage.vue`
- `UsersPage.vue`
- `RolesPage.vue`
- `PermissionsPage.vue`
- `AuditLogsPage.vue`
- `LoginLogsPage.vue`
- `ServiceLinksPage.vue`
- `ProfilePage.vue`
- `ForbiddenPage.vue`
- `NotFoundPage.vue`

---

## 8. 验证

前端构建验证：

```bash
cd frontend
npm run build
```

当前构建会出现 Vite chunk size warning；这是警告不是失败。后续如需优化，可将 Material Web 组件改为更细粒度按路由懒加载，或配置 `build.rollupOptions.output.manualChunks`。
