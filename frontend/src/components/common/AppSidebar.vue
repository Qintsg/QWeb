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
  { path: '/', labelKey: 'nav.dashboard', icon: '📊' },
  { path: '/users', labelKey: 'nav.users', icon: '👥', permission: 'accounts.view_user' },
  { path: '/roles', labelKey: 'nav.roles', icon: '🛡️', permission: 'iam.view_role' },
  { path: '/permissions', labelKey: 'nav.permissions', icon: '🔑', permission: 'iam.view_permission' },
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
  background: var(--qweb-neutral-1);
  border-right: 1px solid var(--qweb-border);
  display: flex;
  flex-direction: column;
  z-index: var(--qweb-z-sidebar);
  transition: width 0.2s ease;
  overflow: hidden;
}

.sidebar--collapsed {
  width: 64px;
}

.sidebar__brand {
  display: flex;
  align-items: center;
  gap: var(--qweb-spacing-sm);
  padding: var(--qweb-spacing-md) var(--qweb-spacing-md);
  border-bottom: 1px solid var(--qweb-border);
  cursor: pointer;
  min-height: 56px;
}

.sidebar__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--qweb-radius-sm);
  background: var(--qweb-primary);
  color: white;
  font-weight: 700;
  font-size: var(--qweb-font-base);
  flex-shrink: 0;
}

.sidebar__brand-text {
  font-weight: 600;
  font-size: var(--qweb-font-lg);
  color: var(--qweb-text-primary);
  white-space: nowrap;
}

.sidebar__nav {
  flex: 1;
  padding: var(--qweb-spacing-sm) 0;
  overflow-y: auto;
}

.sidebar__item {
  display: flex;
  align-items: center;
  gap: var(--qweb-spacing-sm);
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
  margin: 2px var(--qweb-spacing-xs);
  border-radius: var(--qweb-radius-md);
  color: var(--qweb-text-secondary);
  text-decoration: none;
  font-size: var(--qweb-font-sm);
  white-space: nowrap;
  transition: all 0.15s ease;
}

.sidebar__item:hover {
  background: var(--qweb-neutral-2);
  color: var(--qweb-text-primary);
}

.sidebar__item--active {
  background: var(--qweb-primary-light);
  color: var(--qweb-primary);
  font-weight: 500;
}

.sidebar__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  flex-shrink: 0;
  font-size: var(--qweb-font-base);
}

.sidebar__label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar__footer {
  border-top: 1px solid var(--qweb-border);
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
}

.sidebar__toggle {
  width: 100%;
  padding: var(--qweb-spacing-xs);
  background: transparent;
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-sm);
  cursor: pointer;
  color: var(--qweb-text-secondary);
  font-size: var(--qweb-font-sm);
  transition: all 0.15s ease;
}

.sidebar__toggle:hover {
  border-color: var(--qweb-primary);
  color: var(--qweb-primary);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
}
</style>
