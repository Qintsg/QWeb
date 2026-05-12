<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loginIdentifier = ref('')
const password = ref('')
const loading = ref(false)
const githubLoading = ref(false)
const errorMsg = ref('')

function redirectPath() {
  return (route.query.redirect as string) || '/dashboard'
}

async function handleLogin() {
  if (!loginIdentifier.value.trim() || !password.value) {
    errorMsg.value = t('auth.fillAllFields')
    return
  }

  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.login({ login: loginIdentifier.value.trim(), password: password.value })
    router.push(redirectPath())
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.loginFailed')
  } finally {
    loading.value = false
  }
}

async function handleGitHubLogin() {
  githubLoading.value = true
  errorMsg.value = ''
  try {
    await authStore.startGitHubLogin(redirectPath())
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.githubLoginFailed')
    githubLoading.value = false
  }
}
</script>

<template>
  <section class="auth-panel" aria-labelledby="login-title">
    <header class="auth-panel__header">
      <h1 id="login-title">{{ t('auth.login') }}</h1>
      <p>{{ t('auth.loginSubtitle') }}</p>
    </header>

    <form class="auth-form" @submit.prevent="handleLogin">
      <div v-if="errorMsg" class="auth-alert" role="alert">{{ errorMsg }}</div>

      <div class="auth-field">
        <label for="login-identifier">{{ t('auth.accountIdentifier') }}</label>
        <fluent-text-field
          id="login-identifier"
          :value="loginIdentifier"
          :placeholder="t('auth.accountIdentifierPlaceholder')"
          :aria-invalid="Boolean(errorMsg)"
          autocomplete="username"
          required
          @input="loginIdentifier = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
      </div>

      <div class="auth-field">
        <label for="login-password">{{ t('auth.password') }}</label>
        <fluent-text-field
          id="login-password"
          type="password"
          :value="password"
          :placeholder="t('auth.password')"
          autocomplete="current-password"
          required
          @input="password = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
      </div>

      <fluent-button
        type="submit"
        appearance="accent"
        class="auth-button"
        :disabled="loading || githubLoading"
      >
        {{ loading ? t('common.loading') : t('auth.login') }}
      </fluent-button>

      <div class="auth-divider"><span>{{ t('auth.orLoginWith') }}</span></div>

      <fluent-button
        type="button"
        appearance="outline"
        class="auth-button"
        :disabled="githubLoading || loading"
        @click="handleGitHubLogin"
      >
        {{ githubLoading ? t('common.loading') : t('auth.githubLogin') }}
      </fluent-button>

      <p class="auth-link">
        {{ t('auth.noAccount') }}
        <router-link to="/register">{{ t('auth.register') }}</router-link>
      </p>
    </form>
  </section>
</template>

<style scoped>
.auth-panel {
  width: 100%;
}

.auth-panel__header {
  margin-bottom: var(--q-space-24);
}

.auth-panel__header h1 {
  margin: 0;
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-2xl);
  font-weight: var(--q-font-weight-semibold);
}

.auth-panel__header p {
  margin: var(--q-space-8) 0 0;
  color: var(--q-color-text-secondary);
  line-height: var(--q-line-height-base);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-20);
}

.auth-alert {
  padding: var(--q-space-12) var(--q-space-16);
  border: 1px solid var(--q-color-error, #d13438);
  border-radius: var(--q-radius-sm);
  background: var(--q-color-error-light, #fde7e9);
  color: var(--q-color-error, #d13438);
  font-size: var(--q-font-size-sm);
}

.auth-field {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-8);
}

.auth-field label {
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-sm);
  font-weight: var(--q-font-weight-semibold);
}

.auth-field fluent-text-field,
.auth-button {
  width: 100%;
}

.auth-divider {
  display: flex;
  align-items: center;
  gap: var(--q-space-12);
  color: var(--q-color-text-tertiary);
  font-size: var(--q-font-size-sm);
}

.auth-divider::before,
.auth-divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--q-color-divider);
}

.auth-link {
  margin: 0;
  color: var(--q-color-text-secondary);
  font-size: var(--q-font-size-sm);
  text-align: center;
}

.auth-link a {
  color: var(--q-color-brand);
  font-weight: var(--q-font-weight-semibold);
  text-decoration: none;
}
</style>
