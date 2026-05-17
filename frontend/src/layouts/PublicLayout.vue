<!--
  公开布局 - 用于登录、注册、OAuth 回调等未认证页面。

  :project: QWeb
  :file: PublicLayout.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <div class="public-layout">
    <header class="public-layout__header">
      <router-link to="/" class="public-layout__brand" aria-label="返回 QWeb 首页">
        <span aria-hidden="true">Q</span>
        <strong>Qintsg's Web</strong>
      </router-link>
      <div class="public-layout__actions">
        <AppIconButton :label="t('common.switchLang')" icon="translate" @click="toggleLocale" />
        <AppIconButton :label="themeLabel" :icon="themeIcon" @click="toggleTheme" />
      </div>
    </header>

    <main id="main-content" class="public-layout__main" tabindex="-1">
      <section class="public-layout__panel" aria-labelledby="auth-shell-title">
        <div class="public-layout__intro">
          <p class="public-layout__kicker">Secure personal infrastructure</p>
          <h1 id="auth-shell-title">QWeb 身份入口</h1>
          <p>统一进入服务链接、IAM、审计与个人工作区。</p>
        </div>
        <router-view v-slot="{ Component }">
          <Transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import AppIconButton from "@/components/common/AppIconButton.vue"
import { useTheme, type ThemeMode } from "@/composables/useTheme"

const { t, locale } = useI18n()
const { mode } = useTheme()

const themeIcon = computed(() => {
  if (mode.value === "dark") return "dark_mode"
  if (mode.value === "light") return "light_mode"
  return "contrast"
})
const themeLabel = computed(() => `切换主题，当前：${mode.value}`)

function toggleLocale(): void {
  locale.value = locale.value === "zh-CN" ? "en-US" : "zh-CN"
}

function toggleTheme(): void {
  const modes: ThemeMode[] = ["system", "light", "dark"]
  const nextIndex = (modes.indexOf(mode.value) + 1) % modes.length
  mode.value = modes[nextIndex]
}
</script>

<style scoped>
.public-layout {
  position: relative;
  min-block-size: 100dvh;
  display: grid;
  grid-template-rows: auto 1fr;
  overflow: hidden;
  background:
    radial-gradient(circle at 15% 20%, color-mix(in srgb, var(--md-sys-color-primary) 22%, transparent), transparent 28rem),
    radial-gradient(circle at 85% 10%, color-mix(in srgb, var(--md-sys-color-tertiary) 18%, transparent), transparent 24rem),
    var(--md-sys-color-surface);
}

.public-layout::before {
  content: "";
  position: absolute;
  inset: auto -20% -35% 10%;
  block-size: 45%;
  border-radius: var(--md-sys-shape-corner-full);
  background: color-mix(in srgb, var(--md-sys-color-primary) 20%, transparent);
  filter: blur(4rem);
  transform: rotate(-8deg);
  pointer-events: none;
}

.public-layout__header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-md);
  padding-block: var(--space-md);
  padding-inline: clamp(var(--space-md), 4vw, var(--space-xxl));
}

.public-layout__brand {
  min-block-size: 3rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--md-sys-color-on-surface);
}

.public-layout__brand span {
  inline-size: 2.5rem;
  block-size: 2.5rem;
  display: inline-grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-large);
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-title-medium-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.public-layout__brand strong {
  font-family: var(--md-sys-typescale-title-medium-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.public-layout__actions {
  display: flex;
  gap: var(--space-xs);
}

.public-layout__main {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  padding-block: var(--space-lg) var(--space-xxl);
  padding-inline: var(--space-md);
}

.public-layout__panel {
  inline-size: min(100%, 62rem);
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(20rem, 1fr);
  gap: var(--space-xl);
  align-items: center;
  padding: clamp(var(--space-lg), 4vw, var(--space-xxl));
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: color-mix(in srgb, var(--md-sys-color-surface-container-low) 88%, transparent);
  box-shadow: var(--md-sys-elevation-level2);
  backdrop-filter: blur(1.5rem);
}

.public-layout__intro {
  display: grid;
  gap: var(--space-md);
}

.public-layout__kicker {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.public-layout__intro h1 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-display-medium-font);
  font-size: clamp(var(--md-sys-typescale-display-small-size), 6vw, var(--md-sys-typescale-display-medium-size));
  font-weight: var(--md-sys-typescale-display-medium-weight);
  line-height: var(--md-sys-typescale-display-medium-line-height);
}

.public-layout__intro p:last-child {
  max-inline-size: 34rem;
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  font-weight: var(--md-sys-typescale-body-large-weight);
  line-height: var(--md-sys-typescale-body-large-line-height);
}

@media (max-width: 839px) {
  .public-layout__panel {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 599px) {
  .public-layout__brand strong {
    position: absolute;
    inline-size: 1px;
    block-size: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
  }
}
</style>
