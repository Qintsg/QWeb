<!--
  实现 NotFoundPage 页面视图。

  :project: QWeb
  :file: NotFoundPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
/**
 * 404 页面
 */
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="not-found">
    <h1 class="not-found-code">404</h1>
    <p class="not-found-text">{{ t('error.notFound') }}</p>
    <router-link to="/" class="not-found-link">{{ t('common.backHome') }}</router-link>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: var(--q-space-32);
}

.not-found-code {
  margin: 0;
  font-size: 6rem;
  font-weight: 700;
  color: var(--q-color-brand);
  line-height: 1;
}

.not-found-text {
  margin: var(--q-space-16) 0 var(--q-space-32);
  font-size: 1.25rem;
  color: var(--q-color-text-secondary);
}

.not-found-link {
  padding: var(--q-space-12) var(--q-space-32);
  border-radius: var(--q-radius-sm);
  background: var(--q-color-brand);
  color: #fff;
  font-weight: 600;
  transition: background 0.2s;
}

.not-found-link:hover {
  background: var(--q-color-brand-dark);
}
</style>
