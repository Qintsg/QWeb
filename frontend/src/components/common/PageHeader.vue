<!--
  Material 3 页面标题区。

  :project: QWeb
  :file: PageHeader.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <header class="page-header" :class="{ 'page-header--compact': compact }">
    <div class="page-header__eyebrow" v-if="eyebrow || $slots.eyebrow">
      <slot name="eyebrow">{{ eyebrow }}</slot>
    </div>
    <div class="page-header__main">
      <div class="page-header__copy">
        <h1 class="page-header__title">{{ title }}</h1>
        <p v-if="description" class="page-header__description">{{ description }}</p>
      </div>
      <div v-if="$slots.actions" class="page-header__actions">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description?: string
  eyebrow?: string
  compact?: boolean
}>()
</script>

<style scoped>
.page-header {
  display: grid;
  gap: var(--space-md);
  padding-block: var(--space-xl) var(--space-lg);
}

.page-header--compact {
  padding-block: var(--space-lg) var(--space-md);
}

.page-header__eyebrow {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-header__main {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-lg);
}

.page-header__copy {
  display: grid;
  gap: var(--space-sm);
  max-inline-size: 70ch;
}

.page-header__title {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.page-header__description {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  font-weight: var(--md-sys-typescale-body-large-weight);
  line-height: var(--md-sys-typescale-body-large-line-height);
}

.page-header__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  justify-content: end;
}

@media (max-width: 839px) {
  .page-header__main {
    align-items: start;
    flex-direction: column;
  }

  .page-header__actions {
    justify-content: start;
  }
}
</style>
