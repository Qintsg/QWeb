<!--
  首页页脚。

  :project: QWeb
  :file: HomeFooter.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { computed } from "vue"

const currentYear = computed(() => new Date().getFullYear())
</script>

<template>
  <footer class="footer">
    <p>Copyright &copy; {{ currentYear }} Qintsg. All rights reserved.</p>
    <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">沪ICP备2026000797号-2</a>
  </footer>
</template>

<style scoped>
.footer {
  display: grid;
  place-items: center;
  gap: var(--space-xs);
  padding-block: var(--space-xl);
  padding-inline: var(--space-md);
  border-block-start: 0.0625rem solid var(--md-sys-color-outline-variant);
  color: var(--md-sys-color-on-surface-variant);
  background: var(--md-sys-color-surface-container-low);
  font-family: var(--md-sys-typescale-body-small-font);
  font-size: var(--md-sys-typescale-body-small-size);
  font-weight: var(--md-sys-typescale-body-small-weight);
  line-height: var(--md-sys-typescale-body-small-line-height);
}
</style>
