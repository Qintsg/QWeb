<!--
  顶部应用栏。

  :project: QWeb
  :file: AppHeader.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <header class="app-header">
    <div class="app-header__context">
      <p class="app-header__kicker">QWeb Console</p>
      <span class="app-header__status" aria-label="运行状态：在线">
        <span aria-hidden="true"></span>
        Online
      </span>
    </div>

    <div class="app-header__actions">
      <AppIconButton
        :label="t('common.switchLang')"
        icon="translate"
        @click="toggleLocale"
      />
      <AppIconButton
        :label="themeLabel"
        :icon="themeIcon"
        @click="toggleTheme"
      />
      <div class="app-header__user">
        <button
          type="button"
          class="app-header__user-button"
          :aria-expanded="userMenuOpen"
          aria-haspopup="menu"
          @click="userMenuOpen = !userMenuOpen"
        >
          <span class="app-header__avatar" aria-hidden="true">{{ displayInitial }}</span>
          <span class="app-header__user-copy">
            <span>{{ displayName || 'QWeb User' }}</span>
            <small>{{ userGroup }}</small>
          </span>
          <span class="material-symbols-rounded" aria-hidden="true">expand_more</span>
        </button>
        <div v-if="userMenuOpen" id="app-header-user-panel" class="app-header__menu">
          <router-link to="/profile" @click="userMenuOpen = false">
            <span class="material-symbols-rounded" aria-hidden="true">person</span>
            {{ t('nav.profile') }}
          </router-link>
          <button type="button" @click="handleLogout">
            <span class="material-symbols-rounded" aria-hidden="true">logout</span>
            {{ t('auth.logout') }}
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { useAuth } from "@/composables/useAuth"
import { useTheme, type ThemeMode } from "@/composables/useTheme"
import AppIconButton from "@/components/common/AppIconButton.vue"

const router = useRouter()
const { t, locale } = useI18n()
const { displayName, userGroup, logout } = useAuth()
const { mode } = useTheme()

const userMenuOpen = ref(false)

const displayInitial = computed(() => (displayName.value || "Q").charAt(0).toUpperCase())
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

async function handleLogout(): Promise<void> {
  userMenuOpen.value = false
  await logout()
  router.push("/login")
}
</script>

<style scoped>
.app-header {
  position: sticky;
  inset-block-start: 0;
  z-index: 20;
  min-block-size: 4.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-md);
  padding-block: var(--space-sm);
  padding-inline: clamp(var(--space-md), 2vw, var(--space-xl));
  border-block-end: 0.0625rem solid var(--md-sys-color-outline-variant);
  background: color-mix(in srgb, var(--md-sys-color-surface-container-low) 88%, transparent);
  backdrop-filter: blur(1.25rem);
  box-shadow: var(--md-sys-elevation-level1);
}

.app-header__context {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-sm);
}

.app-header__kicker {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.app-header__status {
  min-block-size: 2rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding-inline: var(--space-sm);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
  font-family: var(--md-sys-typescale-label-medium-font);
  font-size: var(--md-sys-typescale-label-medium-size);
  font-weight: var(--md-sys-typescale-label-medium-weight);
  line-height: var(--md-sys-typescale-label-medium-line-height);
}

.app-header__status span {
  inline-size: 0.5rem;
  block-size: 0.5rem;
  border-radius: var(--md-sys-shape-corner-full);
  background: var(--md-sys-color-primary);
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.app-header__user {
  position: relative;
}

.app-header__user-button {
  min-block-size: 3rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-sm);
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-container);
}

.app-header__avatar {
  inline-size: 2rem;
  block-size: 2rem;
  display: inline-grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

.app-header__user-copy {
  display: grid;
  text-align: start;
}

.app-header__user-copy span {
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

.app-header__user-copy small {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-small-font);
  font-size: var(--md-sys-typescale-label-small-size);
  font-weight: var(--md-sys-typescale-label-small-weight);
  line-height: var(--md-sys-typescale-label-small-line-height);
}

.app-header__menu {
  position: absolute;
  inset-block-start: calc(100% + var(--space-sm));
  inset-inline-end: 0;
  min-inline-size: 12rem;
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-sm);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-large);
  background: var(--md-sys-color-surface-container-high);
  box-shadow: var(--md-sys-elevation-level3);
}

.app-header__menu a,
.app-header__menu button {
  min-block-size: 3rem;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-md);
  border: none;
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-surface);
  background: transparent;
  text-align: start;
}

.app-header__menu a:hover,
.app-header__menu button:hover {
  background: var(--md-sys-color-surface-container-highest);
}

@media (max-width: 599px) {
  .app-header {
    min-block-size: 4rem;
  }

  .app-header__context,
  .app-header__user-copy,
  .app-header__user-button > .material-symbols-rounded {
    display: none;
  }
}
</style>
