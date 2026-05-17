<!--
  Material 3 图标按钮。

  :project: QWeb
  :file: AppIconButton.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <button
    type="button"
    class="icon-button"
    :class="{ 'icon-button--active': active }"
    :aria-label="label"
    @click="$emit('click')"
  >
    <span class="material-symbols-rounded" aria-hidden="true">{{ icon }}</span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  icon: string
  active?: boolean
}>()

defineEmits<{
  click: []
}>()
</script>

<style scoped>
.icon-button {
  inline-size: 3rem;
  block-size: 3rem;
  display: inline-grid;
  place-items: center;
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  background: transparent;
  transition:
    color var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    background var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard);
}

.icon-button:hover {
  color: var(--md-sys-color-on-surface);
  background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent);
}

.icon-button:active {
  transform: scale(0.96);
}

.icon-button--active {
  color: var(--md-sys-color-primary);
  background: var(--md-sys-color-primary-container);
}
</style>
