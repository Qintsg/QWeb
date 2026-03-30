<script setup lang="ts">
/**
 * 个人资料页面
 * TODO: Phase 7 实现资料编辑、密码修改、安全设置
 */
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'

const { t } = useI18n()
const { user, displayName, userGroup } = useAuth()
</script>

<template>
  <div class="page-container">
    <h1 class="page-title">{{ t('nav.profile') }}</h1>

    <div v-if="user" class="profile-card">
      <div class="profile-avatar">{{ displayName.charAt(0).toUpperCase() }}</div>
      <div class="profile-info">
        <h2>{{ displayName }}</h2>
        <p>{{ user.email }}</p>
        <span class="profile-group">{{ userGroup }}</span>
      </div>
    </div>

    <p class="page-placeholder">{{ t('common.comingSoon') }}</p>
  </div>
</template>

<style scoped>
.page-container {
  padding: var(--qweb-spacing-xl);
}

.page-title {
  margin: 0 0 var(--qweb-spacing-lg);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.profile-card {
  display: flex;
  align-items: center;
  gap: var(--qweb-spacing-lg);
  padding: var(--qweb-spacing-xl);
  margin-bottom: var(--qweb-spacing-xl);
  background: var(--qweb-surface);
  border-radius: var(--qweb-radius-md);
  border: 1px solid var(--qweb-border);
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--qweb-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  flex-shrink: 0;
}

.profile-info h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--qweb-text-primary);
}

.profile-info p {
  margin: var(--qweb-spacing-xs) 0 0;
  color: var(--qweb-text-secondary);
  font-size: 0.875rem;
}

.profile-group {
  display: inline-block;
  margin-top: var(--qweb-spacing-sm);
  padding: 2px 10px;
  border-radius: var(--qweb-radius-full);
  background: var(--qweb-primary-light, rgba(14, 154, 167, 0.1));
  color: var(--qweb-primary);
  font-size: 0.75rem;
  font-weight: 600;
}

.page-placeholder {
  color: var(--qweb-text-secondary);
}
</style>
