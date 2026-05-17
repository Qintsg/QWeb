<!--
  404 页面视图。

  :project: QWeb
  :file: NotFoundPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { useI18n } from "vue-i18n"

const { t } = useI18n()
</script>

<template>
  <main id="main-content" class="not-found" tabindex="-1">
    <span class="not-found__code">404</span>
    <span class="material-symbols-rounded not-found__icon" aria-hidden="true">explore_off</span>
    <h1>{{ t('error.notFound') }}</h1>
    <router-link to="/" class="not-found__link">
      {{ t('common.backHome') }}
      <span class="material-symbols-rounded" aria-hidden="true">home</span>
    </router-link>
  </main>
</template>

<style scoped>
.not-found {
  min-block-size: 100dvh;
  display: grid;
  place-items: center;
  align-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
  text-align: center;
  background:
    radial-gradient(circle at 50% 20%, color-mix(in srgb, var(--md-sys-color-primary) 18%, transparent), transparent 24rem),
    var(--md-sys-color-surface);
}

.not-found__code {
  color: var(--md-sys-color-primary);
  font-family: var(--q-font-mono);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.not-found__icon {
  inline-size: 5rem;
  block-size: 5rem;
  display: grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
  font-size: 2rem;
}

.not-found h1 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.not-found__link {
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
