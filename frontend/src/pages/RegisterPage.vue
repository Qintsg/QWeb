<!--
  实现 RegisterPage 页面视图。

  :project: QWeb
  :file: RegisterPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { register } from '@/api/auth'

const { t } = useI18n()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errorMsg = ref('')

const usernameHint = computed(() => t('auth.usernameRule'))

function validateForm() {
  if (!username.value.trim() || !email.value.trim() || !password.value || !confirmPassword.value) {
    errorMsg.value = t('auth.fillRegisterFields')
    return false
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = t('auth.passwordMismatch')
    return false
  }
  return true
}

async function handleRegister() {
  if (!validateForm()) return

  loading.value = true
  errorMsg.value = ''
  try {
    await register({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
      password_confirm: confirmPassword.value,
    })
    router.push('/login')
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.registerFailed')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="auth-panel" aria-labelledby="register-title">
    <header class="auth-panel__header">
      <h1 id="register-title">{{ t('auth.register') }}</h1>
      <p>{{ t('auth.registerSubtitle') }}</p>
    </header>

    <form class="auth-form" @submit.prevent="handleRegister">
      <div v-if="errorMsg" class="auth-alert" role="alert">{{ errorMsg }}</div>

      <div class="auth-field">
        <label for="register-username">{{ t('auth.username') }}</label>
        <fluent-text-field
          id="register-username"
          :value="username"
          :placeholder="t('auth.usernamePlaceholder')"
          autocomplete="username"
          required
          @input="username = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
        <span class="auth-help">{{ usernameHint }}</span>
      </div>

      <div class="auth-field">
        <label for="register-email">{{ t('auth.email') }}</label>
        <fluent-text-field
          id="register-email"
          type="email"
          :value="email"
          :placeholder="t('auth.email')"
          autocomplete="email"
          required
          @input="email = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
      </div>

      <div class="auth-field">
        <label for="register-password">{{ t('auth.password') }}</label>
        <fluent-text-field
          id="register-password"
          type="password"
          :value="password"
          autocomplete="new-password"
          required
          @input="password = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
      </div>

      <div class="auth-field">
        <label for="register-confirm">{{ t('auth.confirmPassword') }}</label>
        <fluent-text-field
          id="register-confirm"
          type="password"
          :value="confirmPassword"
          autocomplete="new-password"
          required
          @input="confirmPassword = ($event.target as HTMLInputElement).value"
        ></fluent-text-field>
      </div>

      <fluent-button type="submit" appearance="accent" class="auth-button" :disabled="loading">
        {{ loading ? t('common.loading') : t('auth.register') }}
      </fluent-button>

      <p class="auth-link">
        {{ t('auth.hasAccount') }}
        <router-link to="/login">{{ t('auth.login') }}</router-link>
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

.auth-help {
  color: var(--q-color-text-tertiary);
  font-size: var(--q-font-size-xs);
  line-height: var(--q-line-height-base);
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
