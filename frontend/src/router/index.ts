import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/**
 * 路由配置
 * - 公开页面使用 PublicLayout
 * - 已认证页面使用 DashboardLayout
 * - 路由守卫校验登录状态
 */

/** 公开路由（无需登录） */
const publicRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { layout: 'public', title: '登录' },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/pages/RegisterPage.vue'),
    meta: { layout: 'public', title: '注册' },
  },
]

/** 需要认证的路由 */
const authenticatedRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
    meta: { title: '仪表盘' },
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/pages/UsersPage.vue'),
    meta: { title: '用户管理', permission: 'accounts.view_user' },
  },
  {
    path: '/roles',
    name: 'roles',
    component: () => import('@/pages/RolesPage.vue'),
    meta: { title: '角色管理', permission: 'iam.view_role' },
  },
  {
    path: '/permissions',
    name: 'permissions',
    component: () => import('@/pages/PermissionsPage.vue'),
    meta: { title: '权限管理', permission: 'iam.view_permission' },
  },
  {
    path: '/audit-logs',
    name: 'audit-logs',
    component: () => import('@/pages/AuditLogsPage.vue'),
    meta: { title: '操作日志', permission: 'audit.view_auditlog' },
  },
  {
    path: '/login-logs',
    name: 'login-logs',
    component: () => import('@/pages/LoginLogsPage.vue'),
    meta: { title: '登录日志', permission: 'audit.view_loginlog' },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/pages/ProfilePage.vue'),
    meta: { title: '个人资料' },
  },
]

/** 布局包裹路由 */
const routes: RouteRecordRaw[] = [
  // 公开布局
  {
    path: '/',
    component: () => import('@/layouts/PublicLayout.vue'),
    children: publicRoutes,
  },
  // 已认证布局
  {
    path: '/',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: authenticatedRoutes,
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/NotFoundPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/** 全局前置守卫：认证与权限检查 */
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // 尝试初始化用户状态（首次加载时）
  if (!authStore.isAuthenticated && !authStore.loading) {
    await authStore.initialize()
  }

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (requiresAuth && !authStore.isAuthenticated) {
    // 未登录 → 重定向到登录页
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    // 已登录 → 跳过公开页面
    next({ name: 'dashboard' })
    return
  }

  next()
})

/** 路由后置守卫：更新页面标题 */
router.afterEach((to) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - QWeb` : 'QWeb'
})

export default router
