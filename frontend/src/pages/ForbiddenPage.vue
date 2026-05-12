<!--
  实现 ForbiddenPage 页面视图。

  :project: QWeb
  :file: ForbiddenPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="forbidden-page">
    <p class="forbidden-page__code">403</p>
    <h1 class="forbidden-page__title">{{ t('error.forbidden') }}</h1>
    <p class="forbidden-page__description">{{ t('error.forbiddenDescription') }}</p>
    <router-link to="/dashboard" class="forbidden-page__link">
      {{ t('common.backDashboard') }}
    </router-link>
  </div>
</template>

<style scoped>
.forbidden-page {
  min-height: calc(100vh - var(--q-header-height));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--q-space-12);
  padding: var(--q-space-32);
  text-align: center;
}

.forbidden-page__code {
  margin: 0;
  color: var(--q-color-brand);
  font-size: var(--q-font-size-3xl);
  font-weight: var(--q-font-weight-bold);
  line-height: 1;
}

.forbidden-page__title {
  margin: 0;
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-xl);
  font-weight: var(--q-font-weight-semibold);
}

.forbidden-page__description {
  max-width: 420px;
  margin: 0;
  color: var(--q-color-text-secondary);
  line-height: var(--q-line-height-base);
}

.forbidden-page__link {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: var(--q-space-8);
  padding: 0 var(--q-space-20);
  border-radius: var(--q-radius-sm);
  background: var(--q-color-brand);
  color: var(--q-color-text-on-brand);
  font-weight: var(--q-font-weight-semibold);
  text-decoration: none;
}

.forbidden-page__link:hover,
.forbidden-page__link:focus-visible {
  background: var(--q-color-brand-hover);
  outline: none;
}
</style>
