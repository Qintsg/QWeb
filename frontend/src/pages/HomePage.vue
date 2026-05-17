<!--
  公开首页页面视图。

  :project: QWeb
  :file: HomePage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { getPublicServiceLinks, type ServiceLink } from "@/api/homepage"
import { useAuthStore } from "@/stores/auth"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()
const authStore = useAuthStore()

const serviceLinks = ref<ServiceLink[]>([])
const loading = ref(true)
const error = ref("")

const categoryConfig: Record<string, { label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" }> = {
  project: { label: "项目展示", icon: "school", tone: "primary" },
  server: { label: "服务器管理", icon: "dns", tone: "warning" },
  tool: { label: "工具", icon: "construction", tone: "success" },
  other: { label: "其他", icon: "hub", tone: "neutral" },
}

const currentYear = computed(() => new Date().getFullYear())
const featuredLinks = computed(() => serviceLinks.value.slice(0, 3))

function getCategoryConfig(category: string): { label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" } {
  return categoryConfig[category] ?? categoryConfig.other
}

function getIconForLink(link: ServiceLink): string {
  return link.icon || getCategoryConfig(link.category).icon
}

async function fetchLinks(): Promise<void> {
  loading.value = true
  error.value = ""
  try {
    const response = await getPublicServiceLinks()
    serviceLinks.value = response.data.data ?? []
  } catch {
    error.value = "加载服务链接失败"
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  authStore.initialize()
  fetchLinks()
})
</script>

<template>
  <div class="home-page">
    <header class="hero">
      <nav class="hero__nav" aria-label="公开导航">
        <a href="#services" class="hero__brand" aria-label="Qintsg's Web">
          <span aria-hidden="true">Q</span>
          <strong>Qintsg</strong>
        </a>
        <div class="hero__nav-actions">
          <a href="https://github.com/qintsg" target="_blank" rel="noopener noreferrer">GitHub</a>
          <router-link v-if="authStore.isAuthenticated" to="/dashboard">控制台</router-link>
          <router-link v-else to="/login">{{ t('auth.login') }}</router-link>
        </div>
      </nav>

      <section class="hero__canvas" aria-labelledby="home-title">
        <div class="hero__copy">
          <p class="hero__eyebrow">Personal Infrastructure Portal</p>
          <h1 id="home-title">Qintsg's Web</h1>
          <p class="hero__subtitle">把服务入口、身份权限、审计记录和个人项目收束到一个可控的 Material 3 门户。</p>
          <div class="hero__actions">
            <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="hero__primary-action">
              进入控制台
              <span class="material-symbols-rounded" aria-hidden="true">arrow_forward</span>
            </router-link>
            <router-link v-else to="/login" class="hero__primary-action">
              登录工作区
              <span class="material-symbols-rounded" aria-hidden="true">login</span>
            </router-link>
            <a href="#services" class="hero__secondary-action">查看服务</a>
          </div>
        </div>

        <aside class="hero__visual" aria-label="基础设施状态摘要">
          <div class="hero__orb" aria-hidden="true"></div>
          <div class="hero__signal">
            <span></span><span></span><span></span>
          </div>
          <div class="hero__terminal">
            <p>qweb.status</p>
            <strong>{{ serviceLinks.length }}</strong>
            <span>visible services</span>
          </div>
          <ul class="hero__featured" aria-label="精选服务">
            <li v-for="link in featuredLinks" :key="link.id">
              <span class="material-symbols-rounded" aria-hidden="true">{{ getIconForLink(link) }}</span>
              <span>{{ link.title }}</span>
            </li>
            <li v-if="featuredLinks.length === 0">
              <span class="material-symbols-rounded" aria-hidden="true">pending</span>
              <span>等待服务链接</span>
            </li>
          </ul>
        </aside>
      </section>
    </header>

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
          <span>{{ t('common.loading') }}</span>
        </div>

        <div v-else-if="error" class="services__state" role="alert">
          <span class="material-symbols-rounded" aria-hidden="true">error</span>
          <p>{{ error }}</p>
          <md-filled-button type="button" @click="fetchLinks">重试</md-filled-button>
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

    <footer class="footer">
      <p>Copyright &copy; {{ currentYear }} Qintsg. All rights reserved.</p>
      <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">沪ICP备2026000797号-2</a>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  min-block-size: 100dvh;
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface);
}

.hero {
  position: relative;
  min-block-size: 100svh;
  overflow: hidden;
  background:
    radial-gradient(circle at 78% 18%, color-mix(in srgb, var(--md-sys-color-tertiary) 24%, transparent), transparent 30rem),
    radial-gradient(circle at 16% 24%, color-mix(in srgb, var(--md-sys-color-primary) 24%, transparent), transparent 34rem),
    linear-gradient(135deg, var(--md-sys-color-surface), var(--md-sys-color-surface-container-low));
}

.hero::after {
  content: "";
  position: absolute;
  inset: 12% -20% auto auto;
  inline-size: 55rem;
  block-size: 55rem;
  border: 0.0625rem solid color-mix(in srgb, var(--md-sys-color-primary) 26%, transparent);
  border-radius: var(--md-sys-shape-corner-full);
  pointer-events: none;
}

.hero__nav {
  position: relative;
  z-index: 2;
  min-block-size: 5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-md);
  padding-inline: clamp(var(--space-md), 4vw, var(--space-3xl));
}

.hero__brand,
.hero__nav-actions,
.hero__nav-actions a {
  display: inline-flex;
  align-items: center;
}

.hero__brand {
  min-block-size: 3rem;
  gap: var(--space-sm);
}

.hero__brand span {
  inline-size: 2.5rem;
  block-size: 2.5rem;
  display: inline-grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-large);
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
}

.hero__brand strong,
.hero__nav-actions a {
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

.hero__nav-actions {
  gap: var(--space-sm);
}

.hero__nav-actions a {
  min-block-size: 3rem;
  padding-inline: var(--space-md);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  background: color-mix(in srgb, var(--md-sys-color-surface-container) 72%, transparent);
}

.hero__canvas {
  position: relative;
  z-index: 1;
  min-block-size: calc(100svh - 5rem);
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(20rem, 1fr);
  align-items: center;
  gap: clamp(var(--space-xl), 6vw, var(--space-4xl));
  padding-block: var(--space-xl) var(--space-3xl);
  padding-inline: clamp(var(--space-md), 6vw, var(--space-4xl));
}

.hero__copy {
  max-inline-size: 44rem;
  display: grid;
  gap: var(--space-lg);
  animation: hero-in var(--md-sys-motion-duration-long) var(--md-sys-motion-easing-emphasized-decelerate) both;
}

.hero__eyebrow,
.services__eyebrow {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero h1 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-display-large-font);
  font-size: clamp(var(--md-sys-typescale-display-small-size), 8vw, var(--md-sys-typescale-display-large-size));
  font-weight: var(--md-sys-typescale-display-large-weight);
  line-height: var(--md-sys-typescale-display-large-line-height);
  letter-spacing: -0.04em;
}

.hero__subtitle {
  max-inline-size: 38rem;
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  font-weight: var(--md-sys-typescale-body-large-weight);
  line-height: var(--md-sys-typescale-body-large-line-height);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.hero__primary-action,
.hero__secondary-action {
  min-block-size: 3.5rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding-inline: var(--space-lg);
  border-radius: var(--md-sys-shape-corner-full);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

.hero__primary-action {
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  box-shadow: var(--md-sys-elevation-level2);
}

.hero__secondary-action {
  color: var(--md-sys-color-primary);
  background: var(--md-sys-color-primary-container);
}

.hero__visual {
  position: relative;
  min-block-size: 30rem;
  display: grid;
  align-content: center;
  gap: var(--space-lg);
  animation: visual-in var(--md-sys-motion-duration-extra-long) var(--md-sys-motion-easing-emphasized-decelerate) both;
}

.hero__orb {
  position: absolute;
  inset: 10% 5% auto auto;
  inline-size: min(36vw, 24rem);
  aspect-ratio: 1;
  border-radius: var(--md-sys-shape-corner-full);
  background:
    radial-gradient(circle at 35% 35%, var(--md-sys-color-primary-container), transparent 42%),
    radial-gradient(circle at 65% 70%, var(--md-sys-color-tertiary-container), transparent 45%);
  filter: blur(0.125rem);
  opacity: 0.88;
}

.hero__signal {
  position: relative;
  z-index: 1;
  min-block-size: 16rem;
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: color-mix(in srgb, var(--md-sys-color-surface-container) 76%, transparent);
  box-shadow: var(--md-sys-elevation-level3);
  overflow: hidden;
}

.hero__signal span {
  position: absolute;
  inset-block-start: calc(var(--space-xxl) * var(--item, 1));
  inset-inline: var(--space-lg);
  block-size: 0.125rem;
  border-radius: var(--md-sys-shape-corner-full);
  background: linear-gradient(90deg, transparent, var(--md-sys-color-primary), transparent);
  animation: scan 4s var(--md-sys-motion-easing-standard) infinite;
}

.hero__signal span:nth-child(2) {
  --item: 2;
  animation-delay: 700ms;
}

.hero__signal span:nth-child(3) {
  --item: 3;
  animation-delay: 1400ms;
}

.hero__terminal,
.hero__featured {
  position: relative;
  z-index: 2;
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-large);
  background: var(--md-sys-color-surface-container-high);
  box-shadow: var(--md-sys-elevation-level2);
}

.hero__terminal {
  justify-self: start;
  min-inline-size: 14rem;
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-lg);
  margin-block-start: -10rem;
  margin-inline-start: var(--space-lg);
}

.hero__terminal p,
.hero__terminal span {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--q-font-mono);
  font-size: var(--md-sys-typescale-body-small-size);
  line-height: var(--md-sys-typescale-body-small-line-height);
}

.hero__terminal strong {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-display-small-font);
  font-size: var(--md-sys-typescale-display-small-size);
  font-weight: var(--md-sys-typescale-display-small-weight);
  line-height: var(--md-sys-typescale-display-small-line-height);
}

.hero__featured {
  justify-self: end;
  min-inline-size: min(100%, 22rem);
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-sm);
  list-style: none;
}

.hero__featured li {
  min-block-size: 3rem;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-md);
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-container);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

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

@keyframes hero-in {
  from { opacity: 0; transform: translateY(var(--space-lg)); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes visual-in {
  from { opacity: 0; transform: translateY(var(--space-xl)) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes scan {
  0% { transform: translateX(-40%); opacity: 0; }
  30%, 70% { opacity: 1; }
  100% { transform: translateX(40%); opacity: 0; }
}

@keyframes row-in {
  from { opacity: 0; transform: translateY(var(--space-md)); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 839px) {
  .hero__canvas {
    grid-template-columns: 1fr;
  }

  .hero__visual {
    min-block-size: 24rem;
  }

  .services__header {
    align-items: start;
    flex-direction: column;
  }
}

@media (max-width: 599px) {
  .hero {
    min-block-size: auto;
  }

  .hero__nav-actions a:first-child {
    display: none;
  }

  .hero__canvas {
    min-block-size: auto;
  }

  .hero__visual {
    min-block-size: 18rem;
  }

  .hero__terminal {
    margin-block-start: -8rem;
    margin-inline-start: 0;
  }

  .service-link {
    grid-template-columns: auto minmax(0, 1fr) auto;
  }

  .service-link__pill {
    grid-column: 2 / -1;
    justify-self: start;
  }
}
</style>
