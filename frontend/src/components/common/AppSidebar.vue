<!--
  侧边导航栏
  支持折叠/展开，根据权限动态渲染导航项
-->
<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <!-- 品牌标识 -->
    <div class="sidebar__brand" @click="$emit('toggle')">
      <span class="sidebar__logo">Q</span>
      <span v-if="!collapsed" class="sidebar__brand-text">QWeb</span>
    </div>

    <!-- 导航列表 -->
    <nav class="sidebar__nav">
      <router-link
        v-for="item in visibleNavItems"
        :key="item.path"
        :to="item.path"
        class="sidebar__item"
        active-class="sidebar__item--active"
      >
        <span class="sidebar__icon">{{ item.icon }}</span>
        <span v-if="!collapsed" class="sidebar__label">{{ t(item.labelKey) }}</span>
      </router-link>
    </nav>

    <!-- 底部折叠按钮 -->
    <div class="sidebar__footer">
      <button class="sidebar__toggle" @click="$emit('toggle')">
        {{ collapsed ? '→' : '←' }}
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { usePermission } from '@/composables/usePermission'

defineProps<{
  collapsed: boolean
}>()

defineEmits<{
  toggle: []
}>()

const { t } = useI18n()
const { hasPermission } = usePermission()

/** 导航项定义 */
interface NavItem {
  path: string
  labelKey: string
  icon: string
  /** 所需权限码，为空表示所有已认证用户可见 */
  permission?: string
}

const navItems: NavItem[] = [
  { path: '/dashboard', labelKey: 'nav.dashboard', icon: '📊' },
  { path: '/users', labelKey: 'nav.users', icon: '👥', permission: 'accounts.view_user' },
  { path: '/roles', labelKey: 'nav.roles', icon: '🛡️', permission: 'iam.view_role' },
  { path: '/permissions', labelKey: 'nav.permissions', icon: '🔑', permission: 'iam.view_permission' },
  { path: '/service-links', labelKey: 'nav.serviceLinks', icon: '🔗', permission: 'homepage.service_link.manage' },
  { path: '/audit-logs', labelKey: 'nav.auditLogs', icon: '📋', permission: 'audit.view_auditlog' },
  { path: '/login-logs', labelKey: 'nav.loginLogs', icon: '🔒', permission: 'audit.view_loginlog' },
  { path: '/profile', labelKey: 'nav.profile', icon: '👤' },
]

/** 根据权限过滤可见导航项 */
const visibleNavItems = computed(() =>
  navItems.filter((item) => !item.permission || hasPermission(item.permission))
)
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 260px;
  background: var(--q-color-surface);
  border-right: 1px solid var(--q-color-stroke);
  display: flex;
  flex-direction: column;
  z-index: var(--q-z-sticky);
  transition: width 0.2s ease;
  overflow: hidden;
}

.sidebar--collapsed {
  width: 64px;
}

.sidebar__brand {
  display: flex;
  align-items: center;
  gap: var(--q-space-12);
  padding: var(--q-space-16) var(--q-space-16);
  border-bottom: 1px solid var(--q-color-stroke);
  cursor: pointer;
  min-height: 56px;
}

.sidebar__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--q-radius-sm);
  background: var(--q-color-brand);
  color: white;
  font-weight: 700;
  font-size: var(--q-font-size-base);
  flex-shrink: 0;
}

.sidebar__brand-text {
  font-weight: 600;
  font-size: var(--q-font-size-lg);
  color: var(--q-color-text-primary);
  white-space: nowrap;
}

.sidebar__nav {
  flex: 1;
  padding: var(--q-space-12) 0;
  overflow-y: auto;
}

.sidebar__item {
  display: flex;
  align-items: center;
  gap: var(--q-space-12);
  padding: var(--q-space-12) var(--q-space-16);
  margin: 2px var(--q-space-8);
  border-radius: var(--q-radius-md);
  color: var(--q-color-text-secondary);
  text-decoration: none;
  font-size: var(--q-font-size-sm);
  white-space: nowrap;
  transition: all 0.15s ease;
}

.sidebar__item:hover {
  background: var(--q-color-canvas);
  color: var(--q-color-text-primary);
}

.sidebar__item--active {
  background: var(--q-color-brand-light);
  color: var(--q-color-brand);
  font-weight: 500;
}

.sidebar__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  flex-shrink: 0;
  font-size: var(--q-font-size-base);
}

.sidebar__label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar__footer {
  border-top: 1px solid var(--q-color-stroke);
  padding: var(--q-space-12) var(--q-space-16);
}

.sidebar__toggle {
  width: 100%;
  padding: var(--q-space-8);
  background: transparent;
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-sm);
  cursor: pointer;
  color: var(--q-color-text-secondary);
  font-size: var(--q-font-size-sm);
  transition: all 0.15s ease;
}

.sidebar__toggle:hover {
  border-color: var(--q-color-brand);
  color: var(--q-color-brand);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
}
</style>
