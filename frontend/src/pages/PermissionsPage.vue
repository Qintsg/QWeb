<script setup lang="ts">
/**
 * 权限管理页面
 * TODO: Phase 7 实现权限列表、查询
 */
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="page-container">
    <h1 class="page-title">{{ t('nav.permissions') }}</h1>
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
