<!--
  实现 DashboardPage 页面视图。

  :project: QWeb
  :file: DashboardPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
/**
 * 仪表盘首页
 * 展示欢迎信息、权限感知快速入口与当前可用的系统状态占位
 */
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'
import { usePermission } from '@/composables/usePermission'

const { t } = useI18n()
const { displayName, userGroup } = useAuth()
const { hasPermission } = usePermission()
</script>

<template>
  <div class="page-container">
    <!-- 欢迎区 -->
    <section class="welcome-section">
      <h1 class="welcome-title">{{ t('dashboard.welcome', { name: displayName }) }}</h1>
      <p class="welcome-subtitle">{{ t('dashboard.subtitle') }}</p>
      <span class="user-group-badge">{{ userGroup }}</span>
    </section>

    <!-- 快速入口 -->
    <section class="quick-nav">
      <h2 class="section-title">{{ t('dashboard.quickNav') }}</h2>
      <div class="nav-grid">
        <router-link to="/profile" class="nav-card">
          <div class="nav-icon">👤</div>
          <span>{{ t('nav.profile') }}</span>
        </router-link>

        <router-link v-if="hasPermission('accounts.user.view')" to="/users" class="nav-card">
          <div class="nav-icon">👥</div>
          <span>{{ t('nav.userManagement') }}</span>
        </router-link>

        <router-link v-if="hasPermission('iam.role.view')" to="/roles" class="nav-card">
          <div class="nav-icon">🛡️</div>
          <span>{{ t('nav.roleManagement') }}</span>
        </router-link>

        <router-link v-if="hasPermission('audit.log.view')" to="/audit-logs" class="nav-card">
          <div class="nav-icon">📋</div>
          <span>{{ t('nav.auditLogs') }}</span>
        </router-link>
      </div>
    </section>

    <!-- 系统状态占位 -->
    <section class="status-section">
      <h2 class="section-title">{{ t('dashboard.systemStatus') }}</h2>
      <p class="page-placeholder">{{ t('common.comingSoon') }}</p>
    </section>
  </div>
</template>

<style scoped>
.page-container {
  padding: var(--q-space-32);
}

.welcome-section {
  margin-bottom: var(--q-space-40);
}

.welcome-title {
  margin: 0 0 var(--q-space-8);
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--q-color-text-primary);
}

.welcome-subtitle {
  margin: 0 0 var(--q-space-12);
  color: var(--q-color-text-secondary);
  font-size: 0.95rem;
}

.user-group-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: var(--q-radius-full);
  background: var(--q-color-brand-light, rgba(14, 154, 167, 0.1));
  color: var(--q-color-brand);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.section-title {
  margin: 0 0 var(--q-space-16);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--q-color-text-primary);
}

.quick-nav {
  margin-bottom: var(--q-space-40);
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--q-space-16);
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--q-space-12);
  padding: var(--q-space-24);
  background: var(--q-color-surface);
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-md);
  text-decoration: none;
  color: var(--q-color-text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.nav-card:hover {
  border-color: var(--q-color-brand);
  box-shadow: 0 2px 8px rgba(14, 154, 167, 0.12);
}

.nav-icon {
  font-size: 1.5rem;
}

.status-section {
  margin-bottom: var(--q-space-32);
}

.page-placeholder {
  color: var(--q-color-text-secondary);
}
</style>
