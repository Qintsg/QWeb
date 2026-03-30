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
  padding: var(--qweb-spacing-xl);
}

.not-found-code {
  margin: 0;
  font-size: 6rem;
  font-weight: 700;
  color: var(--qweb-primary);
  line-height: 1;
}

.not-found-text {
  margin: var(--qweb-spacing-md) 0 var(--qweb-spacing-xl);
  font-size: 1.25rem;
  color: var(--qweb-text-secondary);
}

.not-found-link {
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-xl);
  border-radius: var(--qweb-radius-sm);
  background: var(--qweb-primary);
  color: #fff;
  font-weight: 600;
  transition: background 0.2s;
}

.not-found-link:hover {
  background: var(--qweb-primary-dark);
}
</style>
