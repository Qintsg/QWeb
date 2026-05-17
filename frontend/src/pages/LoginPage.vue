<!--
  登录页面视图。

  :project: QWeb
  :file: LoginPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { useAuthStore } from "@/stores/auth"

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loginIdentifier = ref("")
const password = ref("")
const loading = ref(false)
const githubLoading = ref(false)
const errorMsg = ref("")

function redirectPath(): string {
  return (route.query.redirect as string) || "/dashboard"
}

async function handleLogin(): Promise<void> {
  if (!loginIdentifier.value.trim() || !password.value) {
    errorMsg.value = t("auth.fillAllFields")
    return
  }

  loading.value = true
  errorMsg.value = ""
  try {
    await authStore.login({ login: loginIdentifier.value.trim(), password: password.value })
    router.push(redirectPath())
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.loginFailed")
  } finally {
    loading.value = false
  }
}

async function handleGitHubLogin(): Promise<void> {
  githubLoading.value = true
  errorMsg.value = ""
  try {
    await authStore.startGitHubLogin(redirectPath())
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.githubLoginFailed")
    githubLoading.value = false
  }
}
</script>

<template>
  <section class="auth-panel" aria-labelledby="login-title">
    <header class="auth-panel__header">
      <p>Local or OAuth</p>
      <h2 id="login-title">{{ t('auth.login') }}</h2>
      <span>{{ t('auth.loginSubtitle') }}</span>
    </header>

    <form class="auth-form" @submit.prevent="handleLogin">
      <div v-if="errorMsg" id="login-error" class="auth-alert" role="alert">
        <span class="material-symbols-rounded" aria-hidden="true">error</span>
        <span>{{ errorMsg }}</span>
      </div>

      <md-outlined-text-field
        id="login-identifier"
        :label="t('auth.accountIdentifier')"
        :value="loginIdentifier"
        :error="Boolean(errorMsg)"
        :error-text="errorMsg"
        :aria-describedby="errorMsg ? 'login-error' : undefined"
        autocomplete="username"
        required
        @input="loginIdentifier = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>

      <md-outlined-text-field
        id="login-password"
        type="password"
        :label="t('auth.password')"
        :value="password"
        autocomplete="current-password"
        required
        @input="password = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>

      <md-filled-button
        type="submit"
        class="auth-button"
        :disabled="loading || githubLoading"
        :aria-busy="loading"
      >
        <md-circular-progress v-if="loading" slot="icon" indeterminate></md-circular-progress>
        {{ loading ? t('common.loading') : t('auth.login') }}
      </md-filled-button>

      <div class="auth-divider"><span>{{ t('auth.orLoginWith') }}</span></div>

      <md-outlined-button
        type="button"
        class="auth-button"
        :disabled="githubLoading || loading"
        :aria-busy="githubLoading"
        @click="handleGitHubLogin"
      >
        <span slot="icon" class="material-symbols-rounded" aria-hidden="true">code</span>
        {{ githubLoading ? t('common.loading') : t('auth.githubLogin') }}
      </md-outlined-button>

      <p class="auth-link">
        {{ t('auth.noAccount') }}
        <router-link to="/register">{{ t('auth.register') }}</router-link>
      </p>
    </form>
  </section>
</template>

<style scoped>
.auth-panel {
  inline-size: 100%;
  display: grid;
  gap: var(--space-lg);
}

.auth-panel__header {
  display: grid;
  gap: var(--space-xs);
}

.auth-panel__header p {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.auth-panel__header h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.auth-panel__header span,
.auth-link {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.auth-form {
  display: grid;
  gap: var(--space-md);
}

.auth-form md-outlined-text-field,
.auth-button {
  inline-size: 100%;
}

.auth-alert {
  min-block-size: 3rem;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-md);
  border: 0.0625rem solid var(--md-sys-color-error);
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.auth-divider {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-medium-font);
  font-size: var(--md-sys-typescale-label-medium-size);
  font-weight: var(--md-sys-typescale-label-medium-weight);
  line-height: var(--md-sys-typescale-label-medium-line-height);
}

.auth-divider::before,
.auth-divider::after {
  content: "";
  flex: 1;
  block-size: 0.0625rem;
  background: var(--md-sys-color-outline-variant);
}

.auth-link {
  text-align: center;
}

.auth-link a {
  color: var(--md-sys-color-primary);
  font-weight: var(--md-sys-typescale-label-large-weight);
}
</style>
