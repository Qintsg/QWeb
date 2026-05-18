<!--
  自适应侧边导航栏。

  :project: QWeb
  :file: AppSidebar.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <nav class="app-nav" aria-label="主导航">
    <router-link to="/dashboard" class="app-nav__brand" aria-label="返回仪表盘">
      <span class="app-nav__logo" aria-hidden="true">
        <img v-if="siteStore.metadata.logo_url" :src="siteStore.metadata.logo_url" alt="" />
        <span v-else>{{ siteStore.brandInitial }}</span>
      </span>
      <span class="app-nav__brand-copy">
        <strong>{{ siteStore.siteName }}</strong>
        <small>管理控制台</small>
      </span>
    </router-link>

    <ul class="app-nav__list">
      <li v-for="item in visibleNavItems" :key="item.path">
        <router-link :to="item.path" class="app-nav__item" :aria-label="t(item.labelKey)">
          <span class="material-symbols-rounded" aria-hidden="true">{{ item.icon }}</span>
          <span>{{ t(item.labelKey) }}</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { usePermission } from "@/composables/usePermission"
import { useSiteStore } from "@/stores/site"

const { t } = useI18n()
const { hasPermission } = usePermission()
const siteStore = useSiteStore()

interface NavItem {
  path: string
  labelKey: string
  icon: string
  permission?: string
}

const navItems: NavItem[] = [
  { path: "/dashboard", labelKey: "nav.dashboard", icon: "dashboard" },
  { path: "/users", labelKey: "nav.userManagement", icon: "group", permission: "accounts.user.view" },
  { path: "/roles", labelKey: "nav.roleManagement", icon: "admin_panel_settings", permission: "iam.role.view" },
  { path: "/permissions", labelKey: "nav.permissionManagement", icon: "vpn_key", permission: "iam.permission.view" },
  { path: "/service-links", labelKey: "nav.serviceLinks", icon: "hub", permission: "homepage.service_link.manage" },
  { path: "/site-settings", labelKey: "nav.siteSettings", icon: "tune", permission: "system_config.config.update" },
  { path: "/audit-logs", labelKey: "nav.auditLogs", icon: "assignment", permission: "audit.log.view" },
  { path: "/login-logs", labelKey: "nav.loginLogs", icon: "shield_lock", permission: "audit.log.view" },
  { path: "/profile", labelKey: "nav.profile", icon: "person" },
]

const visibleNavItems = computed(() =>
  navItems.filter((item) => !item.permission || hasPermission(item.permission))
)
</script>

<style scoped>
.app-nav {
  position: sticky;
  inset-block-start: 0;
  block-size: 100dvh;
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  padding: var(--space-md);
  border-inline-end: 0.0625rem solid var(--md-sys-color-outline-variant);
  background: var(--md-sys-color-surface-container-low);
}

.app-nav__brand {
  min-block-size: 4rem;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-sm);
  border-radius: var(--md-sys-shape-corner-extra-large);
}

.app-nav__logo {
  inline-size: 3rem;
  block-size: 3rem;
  display: inline-grid;
  place-items: center;
  flex: 0 0 auto;
  border-radius: var(--md-sys-shape-corner-large);
  color: var(--md-sys-color-on-primary);
  background: linear-gradient(135deg, var(--md-sys-color-primary), var(--md-sys-color-tertiary));
  box-shadow: var(--md-sys-elevation-level2);
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.app-nav__logo img,
.app-nav__logo > span {
  inline-size: 100%;
  block-size: 100%;
  display: grid;
  place-items: center;
  border-radius: inherit;
  object-fit: cover;
}

.app-nav__brand-copy {
  display: grid;
  gap: var(--space-xs);
}

.app-nav__brand-copy strong {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-title-medium-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.app-nav__brand-copy small {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-small-font);
  font-size: var(--md-sys-typescale-label-small-size);
  font-weight: var(--md-sys-typescale-label-small-weight);
  line-height: var(--md-sys-typescale-label-small-line-height);
}

.app-nav__list {
  display: grid;
  gap: var(--space-xs);
  list-style: none;
  overflow-y: auto;
}

.app-nav__item {
  min-block-size: 3.5rem;
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding-inline: var(--space-md);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  transition:
    color var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    background var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard);
}

.app-nav__item:hover {
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-container);
  transform: translateX(var(--space-xs));
}

.app-nav__item.router-link-active {
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
}

@media (min-width: 600px) and (max-width: 1199px) {
  .app-nav {
    inline-size: var(--q-layout-rail-width);
    padding-inline: var(--space-sm);
  }

  .app-nav__brand-copy,
  .app-nav__item span:last-child {
    position: absolute;
    inline-size: 1px;
    block-size: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
  }

  .app-nav__brand,
  .app-nav__item {
    justify-content: center;
    padding-inline: 0;
  }

  .app-nav__item:hover {
    transform: translateY(calc(var(--space-xs) * -1));
  }
}

@media (max-width: 599px) {
  .app-nav {
    position: fixed;
    inset-block: auto 0;
    inset-inline: 0;
    z-index: 40;
    block-size: var(--q-layout-bottom-nav-height);
    flex-direction: row;
    align-items: center;
    padding-block: var(--space-xs) max(var(--space-xs), env(safe-area-inset-bottom));
    padding-inline: var(--space-sm);
    border-block-start: 0.0625rem solid var(--md-sys-color-outline-variant);
    border-inline-end: none;
    box-shadow: var(--md-sys-elevation-level3);
  }

  .app-nav__brand {
    display: none;
  }

  .app-nav__list {
    inline-size: 100%;
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 1fr;
    overflow-x: auto;
  }

  .app-nav__item {
    min-block-size: 4rem;
    flex-direction: column;
    justify-content: center;
    gap: var(--space-xs);
    padding-inline: var(--space-xs);
    border-radius: var(--md-sys-shape-corner-large);
    font-size: var(--md-sys-typescale-label-small-size);
    line-height: var(--md-sys-typescale-label-small-line-height);
  }

  .app-nav__item:hover {
    transform: none;
  }
}
</style>
