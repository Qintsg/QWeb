<script setup lang="ts">
/**
 * 操作日志页面
 * TODO: Phase 7 实现审计日志列表、筛选、详情
 */
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="page-container">
    <h1 class="page-title">{{ t('nav.auditLogs') }}</h1>
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
