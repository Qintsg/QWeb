<script setup lang="ts">
/**
 * 用户管理页面
 * TODO: Phase 7 实现用户列表、搜索、详情
 */
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="page-container">
    <h1 class="page-title">{{ t('nav.users') }}</h1>
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

.page-placeholder {
  color: var(--qweb-text-secondary);
}
</style>
