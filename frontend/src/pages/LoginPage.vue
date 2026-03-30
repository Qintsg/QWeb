<script setup lang="ts">
/**
 * 登录页面
 * TODO: Phase 7 实现完整登录表单
 */
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

/** 处理登录 */
async function handleLogin() {
  if (!username.value || !password.value) {
    errorMsg.value = t('auth.fillAllFields')
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await authStore.login({ username: username.value, password: password.value })
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.loginFailed')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <h1 class="login-title">{{ t('auth.login') }}</h1>

    <form class="login-form" @submit.prevent="handleLogin">
      <div v-if="errorMsg" class="login-error">{{ errorMsg }}</div>

      <div class="form-field">
        <label for="username">{{ t('auth.username') }}</label>
        <input
          id="username"
          v-model="username"
          type="text"
          :placeholder="t('auth.usernamePlaceholder')"
          autocomplete="username"
          required
        />
      </div>

      <div class="form-field">
        <label for="password">{{ t('auth.password') }}</label>
        <input
          id="password"
          v-model="password"
          type="password"
          :placeholder="t('auth.passwordPlaceholder')"
          autocomplete="current-password"
          required
        />
      </div>

      <button type="submit" class="login-btn" :disabled="loading">
        {{ loading ? t('common.loading') : t('auth.login') }}
      </button>

      <p class="login-link">
        {{ t('auth.noAccount') }}
        <router-link to="/register">{{ t('auth.register') }}</router-link>
      </p>
    </form>
  </div>
</template>

<style scoped>
.login-page {
  width: 100%;
  max-width: 400px;
}

.login-title {
  margin: 0 0 var(--qweb-spacing-xl);
  font-size: 1.75rem;
  font-weight: 600;
  text-align: center;
  color: var(--qweb-text-primary);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-lg);
}

.login-error {
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
  border-radius: var(--qweb-radius-sm);
  background: var(--qweb-danger-light, #fde7e7);
  color: var(--qweb-danger, #d32f2f);
  font-size: 0.875rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-xs);
}

.form-field label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--qweb-text-secondary);
}

.form-field input {
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-sm);
  font-size: 0.9375rem;
  background: var(--qweb-surface);
  color: var(--qweb-text-primary);
  transition: border-color 0.2s;
}

.form-field input:focus {
  border-color: var(--qweb-primary);
  outline: none;
  box-shadow: 0 0 0 2px var(--qweb-primary-light, rgba(14, 154, 167, 0.15));
}

.login-btn {
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-lg);
  border: none;
  border-radius: var(--qweb-radius-sm);
  background: var(--qweb-primary);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.login-btn:hover:not(:disabled) {
  background: var(--qweb-primary-dark);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 0.875rem;
  color: var(--qweb-text-secondary);
}

.login-link a {
  color: var(--qweb-primary);
  font-weight: 500;
}
</style>
