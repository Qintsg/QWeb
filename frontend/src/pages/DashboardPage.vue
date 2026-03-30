<script setup lang="ts">
/**
 * 仪表盘首页
 * 展示欢迎信息、快速入口与系统状态概览
 * TODO: Phase 7 实现统计卡片、活动流、模块入口
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

        <router-link v-if="hasPermission('accounts.view_user')" to="/users" class="nav-card">
          <div class="nav-icon">👥</div>
          <span>{{ t('nav.userManagement') }}</span>
        </router-link>

        <router-link v-if="hasPermission('iam.view_role')" to="/roles" class="nav-card">
          <div class="nav-icon">🛡️</div>
          <span>{{ t('nav.roleManagement') }}</span>
        </router-link>

        <router-link v-if="hasPermission('audit.view_auditlog')" to="/audit-logs" class="nav-card">
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
  padding: var(--qweb-spacing-xl);
}

.welcome-section {
  margin-bottom: var(--qweb-spacing-2xl);
}

.welcome-title {
  margin: 0 0 var(--qweb-spacing-xs);
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.welcome-subtitle {
  margin: 0 0 var(--qweb-spacing-sm);
  color: var(--qweb-text-secondary);
  font-size: 0.95rem;
}

.user-group-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: var(--qweb-radius-full);
  background: var(--qweb-primary-light, rgba(14, 154, 167, 0.1));
  color: var(--qweb-primary);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.section-title {
  margin: 0 0 var(--qweb-spacing-md);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.quick-nav {
  margin-bottom: var(--qweb-spacing-2xl);
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--qweb-spacing-md);
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--qweb-spacing-sm);
  padding: var(--qweb-spacing-lg);
  background: var(--qweb-surface);
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-md);
  text-decoration: none;
  color: var(--qweb-text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.nav-card:hover {
  border-color: var(--qweb-primary);
  box-shadow: 0 2px 8px rgba(14, 154, 167, 0.12);
}

.nav-icon {
  font-size: 1.5rem;
}

.status-section {
  margin-bottom: var(--qweb-spacing-xl);
}

.page-placeholder {
  color: var(--qweb-text-secondary);
}
</styl
<style scoped>
.page-container {
  padding: var(--qweb-spacing-xl);
}

.welcome-section {
  margin-bottom: var(--qweb-spacing-2xl);
}

.welcome-title {
  margin: 0 0 var(--qweb-spacing-xs);
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.welcome-subtitle {
  margin: 0 0 var(--qweb-spacing-sm);
  color: var(--qweb-text-secondary);
  font-size: 0.95rem;
}

.user-group-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: var(--qweb-radius-full);
  background: var(--qweb-primary-light, rgba(14, 154, 167, 0.1));
  color: var(--qweb-primary);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.section-title {
  margin: 0 0 var(--qweb-spacing-md);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.quick-nav {
  margin-bottom: var(--qweb-spacing-2xl);
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--qweb-spacing-md);
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--qweb-spacing-sm);
  padding: var(--qweb-spacing-lg);
  background: var(--qweb-surface);
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-md);
  text-decoration: none;
  color: var(--qweb-text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.nav-card:hover {
  border-color: var(--qweb-primary);
  box-shadow: 0 2px 8px rgba(14, 154, 167, 0.12);
}

.nav-icon {
  font-size: 1.5rem;
}

.status-section {
  margin-bottom: var(--qweb-spacing-xl);
}

.page-placeholder {
  color: var(--qweb-text-secondary);
}
</styl
<style scoped>
.page-container {
  padding: var(--qweb-spacing-xl);
}

.welcome-section {
  margin-bottom: var(--qweb-spacing-2xl);
}

.welcome-title {
  margin: 0 0 var(--qweb-spacing-xs);
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.welcome-subtitle {
  margin: 0 0 var(--qweb-spacing-sm);
  color: var(--qweb-text-secondary);
  font-size: 0.95rem;
}

.user-group-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: var(--qweb-radius-full);
  background: var(--qweb-primary-light, rgba(14, 154, 167, 0.1));
  color: var(--qweb-primary);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.section-title {
  margin: 0 0 var(--qweb-spacing-md);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.quick-nav {
  margin-bottom: var(--qweb-spacing-2xl);
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--qweb-spacing-md);
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--qweb-spacing-sm);
  padding: var(--qweb-spacing-lg);
  background: var(--qweb-surface);
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-md);
  text-decoration: none;
  color: var(--qweb-text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.nav-card:hover {
  border-color: var(--qweb-primary);
  box-shadow: 0 2px 8px rgba(14, 154, 167, 0.12);
}

.nav-icon {
  font-size: 1.5rem;
}

.status-section {
  margin-bottom: var(--qweb-spacing-xl);
}

.page-placeholder {
  color: var(--qweb-text-secondary);
}
</style>
