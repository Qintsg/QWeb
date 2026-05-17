<!--
  Material 3 状态徽标。

  :project: QWeb
  :file: StatusPill.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <span class="status-pill" :class="`status-pill--${tone}`">
    <span class="material-symbols-rounded status-pill__icon" aria-hidden="true">{{ icon }}</span>
    <span>{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    tone?: "primary" | "success" | "warning" | "error" | "neutral"
    icon?: string
  }>(),
  {
    tone: "neutral",
    icon: "fiber_manual_record",
  }
)
</script>

<style scoped>
.status-pill {
  min-block-size: 2rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding-inline: var(--space-sm);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  background: var(--md-sys-color-surface-container-low);
  font-family: var(--md-sys-typescale-label-medium-font);
  font-size: var(--md-sys-typescale-label-medium-size);
  font-weight: var(--md-sys-typescale-label-medium-weight);
  line-height: var(--md-sys-typescale-label-medium-line-height);
}

.status-pill__icon {
  font-size: 1rem;
}

.status-pill--primary {
  color: var(--md-sys-color-on-primary-container);
  border-color: color-mix(in srgb, var(--md-sys-color-primary) 28%, var(--md-sys-color-outline-variant));
  background: var(--md-sys-color-primary-container);
}

.status-pill--success {
  color: var(--md-sys-color-on-secondary-container);
  border-color: color-mix(in srgb, var(--md-sys-color-secondary) 32%, var(--md-sys-color-outline-variant));
  background: var(--md-sys-color-secondary-container);
}

.status-pill--warning {
  color: var(--md-sys-color-on-tertiary-container);
  border-color: color-mix(in srgb, var(--md-sys-color-tertiary) 32%, var(--md-sys-color-outline-variant));
  background: var(--md-sys-color-tertiary-container);
}

.status-pill--error {
  color: var(--md-sys-color-on-error-container);
  border-color: color-mix(in srgb, var(--md-sys-color-error) 32%, var(--md-sys-color-outline-variant));
  background: var(--md-sys-color-error-container);
}
</style>
