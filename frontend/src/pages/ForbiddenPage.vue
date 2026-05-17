<!--
  403 无权限页面视图。

  :project: QWeb
  :file: ForbiddenPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { useI18n } from "vue-i18n"

const { t } = useI18n()
</script>

<template>
  <section class="error-page" aria-labelledby="forbidden-title">
    <span class="error-page__code">403</span>
    <span class="material-symbols-rounded error-page__icon" aria-hidden="true">lock</span>
    <h1 id="forbidden-title">{{ t('error.forbidden') }}</h1>
    <p>{{ t('error.forbiddenDescription') }}</p>
    <router-link to="/dashboard" class="error-page__link">
      {{ t('common.backDashboard') }}
      <span class="material-symbols-rounded" aria-hidden="true">arrow_forward</span>
    </router-link>
  </section>
</template>

<style scoped>
.error-page {
  min-block-size: calc(100dvh - 10rem);
  display: grid;
  place-items: center;
  align-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
  text-align: center;
}

.error-page__code {
  color: var(--md-sys-color-primary);
  font-family: var(--q-font-mono);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.error-page__icon {
  inline-size: 5rem;
  block-size: 5rem;
  display: grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
  font-size: 2rem;
}

.error-page h1 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.error-page p {
  max-inline-size: 32rem;
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  font-weight: var(--md-sys-typescale-body-large-weight);
  line-height: var(--md-sys-typescale-body-large-line-height);
}

.error-page__link {
  min-block-size: 3rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-lg);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}
</style>
