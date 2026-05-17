<!--
  首页服务目录区块。

  :project: QWeb
  :file: ServiceDirectory.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import type { ServiceLink } from "@/api/homepage"
import StatusPill from "@/components/common/StatusPill.vue"

defineProps<{
  serviceLinks: ServiceLink[]
  loading: boolean
  error: string
}>()

const emit = defineEmits<{
  retry: []
}>()

const categoryConfig: Record<string, { label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" }> = {
  project: { label: "项目展示", icon: "school", tone: "primary" },
  server: { label: "服务器管理", icon: "dns", tone: "warning" },
  tool: { label: "工具", icon: "construction", tone: "success" },
  other: { label: "其他", icon: "hub", tone: "neutral" },
}

function getCategoryConfig(category: string): { label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" } {
  return categoryConfig[category] ?? categoryConfig.other
}

function getIconForLink(link: ServiceLink): string {
  return link.icon || getCategoryConfig(link.category).icon
}
</script>

<template>
  <main id="main-content" class="home-page__main" tabindex="-1">
    <section id="services" class="services" aria-labelledby="services-title">
      <div class="services__header">
        <div>
          <p class="services__eyebrow">Service Directory</p>
          <h2 id="services-title">服务与项目</h2>
        </div>
        <StatusPill :label="`${serviceLinks.length} 个可见入口`" tone="primary" icon="hub" />
      </div>

      <div v-if="loading" class="services__state" role="status" aria-live="polite">
        <md-circular-progress indeterminate aria-label="正在加载服务链接"></md-circular-progress>
        <span>加载中…</span>
      </div>

      <div v-else-if="error" class="services__state" role="alert">
        <span class="material-symbols-rounded" aria-hidden="true">error</span>
        <p>{{ error }}</p>
        <md-filled-button type="button" @click="emit('retry')">重试</md-filled-button>
      </div>

      <div v-else-if="serviceLinks.length === 0" class="services__state">
        <span class="material-symbols-rounded" aria-hidden="true">inventory_2</span>
        <p>暂无服务链接</p>
      </div>

      <div v-else class="services__grid">
        <a
          v-for="(link, index) in serviceLinks"
          :key="link.id"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="service-link"
          :style="{ '--item-index': index }"
        >
          <span class="service-link__icon material-symbols-rounded" aria-hidden="true">{{ getIconForLink(link) }}</span>
          <span class="service-link__body">
            <strong>{{ link.title }}</strong>
            <span v-if="link.description">{{ link.description }}</span>
            <small v-if="link.remark">{{ link.remark }}</small>
          </span>
          <StatusPill
            class="service-link__pill"
            :label="getCategoryConfig(link.category).label"
            :tone="getCategoryConfig(link.category).tone"
            :icon="getCategoryConfig(link.category).icon"
          />
          <span class="material-symbols-rounded service-link__arrow" aria-hidden="true">open_in_new</span>
        </a>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-page__main {
  padding-block: var(--space-4xl);
  padding-inline: clamp(var(--space-md), 5vw, var(--space-4xl));
}

.services {
  inline-size: min(100%, var(--q-layout-content-max));
  display: grid;
  gap: var(--space-xl);
  margin-inline: auto;
}

.services__header {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-lg);
}

.services__eyebrow {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.services h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.services__state {
  min-block-size: 16rem;
  display: grid;
  place-items: center;
  align-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
  border: 0.0625rem dashed var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-surface-variant);
  background: var(--md-sys-color-surface-container-low);
}

.services__grid {
  display: grid;
  gap: var(--space-md);
}

.service-link {
  --item-delay: calc(var(--item-index) * 60ms);
  position: relative;
  min-block-size: 6rem;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto auto;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-container-low);
  box-shadow: var(--md-sys-elevation-level0);
  animation: row-in var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-emphasized-decelerate) var(--item-delay) both;
  transition:
    background var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    border-color var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    box-shadow var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard);
}

.service-link:hover {
  border-color: var(--md-sys-color-primary);
  background: var(--md-sys-color-surface-container);
  box-shadow: var(--md-sys-elevation-level2);
  transform: translateY(calc(var(--space-xs) * -1));
}

.service-link__icon {
  inline-size: 3rem;
  block-size: 3rem;
  display: inline-grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-large);
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
}

.service-link__body {
  display: grid;
  gap: var(--space-xs);
}

.service-link__body strong {
  font-family: var(--md-sys-typescale-title-medium-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.service-link__body span,
.service-link__body small {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.service-link__body small {
  font-family: var(--q-font-mono);
}

.service-link__arrow {
  color: var(--md-sys-color-on-surface-variant);
}

@keyframes row-in {
  from { opacity: 0; transform: translateY(var(--space-md)); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 839px) {
  .services__header {
    align-items: start;
    flex-direction: column;
  }
}

@media (max-width: 599px) {
  .service-link {
    grid-template-columns: auto minmax(0, 1fr) auto;
  }

  .service-link__pill {
    grid-column: 2 / -1;
    justify-self: start;
  }
}
</style>
