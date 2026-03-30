<script setup lang="ts">
/**
 * 注册页面
 * TODO: Phase 7 实现完整注册流程
 */
import { ref } from 'vue'
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

/** 处理注册 */
async function handleRegister() {
  if (!username.value || !email.value || !password.value) {
    errorMsg.value = t('auth.fillAllFields')
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = t('auth.passwordMismatch')
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await register({
      username: username.value,
      email: email.value,
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
  <div class="register-page">
    <h1 class="register-title">{{ t('auth.register') }}</h1>

    <form class="register-form" @submit.prevent="handleRegister">
      <div v-if="errorMsg" class="register-error">{{ errorMsg }}</div>

      <div class="form-field">
        <label for="reg-username">{{ t('auth.username') }}</label>
        <input id="reg-username" v-model="username" type="text" :placeholder="t('auth.usernamePlaceholder')" required />
      </div>

      <div class="form-field">
        <label for="reg-email">{{ t('auth.email') }}</label>
        <input id="reg-email" v-model="email" type="email" :placeholder="t('auth.emailPlaceholder')" required />
      </div>

      <div class="form-field">
        <label for="reg-password">{{ t('auth.password') }}</label>
        <input id="reg-password" v-model="password" type="password" :placeholder="t('auth.passwordPlaceholder')" required />
      </div>

      <div class="form-field">
        <label for="reg-confirm">{{ t('auth.confirmPassword') }}</label>
        <input id="reg-confirm" v-model="confirmPassword" type="password" :placeholder="t('auth.confirmPasswordPlaceholder')" required />
      </div>

      <button type="submit" class="register-btn" :disabled="loading">
        {{ loading ? t('common.loading') : t('auth.register') }}
      </button>

      <p class="register-link">
        {{ t('auth.hasAccount') }}
        <router-link to="/login">{{ t('auth.login') }}</router-link>
      </p>
    </form>
  </div>
</template>

<style scoped>
.register-page {
  width: 100%;
  max-width: 400px;
}

.register-title {
  margin: 0 0 var(--qweb-spacing-xl);
  font-size: 1.75rem;
  font-weight: 600;
  text-align: center;
  color: var(--qweb-text-primary);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-lg);
}

.register-error {
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

.register-btn {
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

.register-btn:hover:not(:disabled) {
  background: var(--qweb-primary-dark);
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  font-size: 0.875rem;
  color: var(--qweb-text-secondary);
}

.register-link a {
  color: var(--qweb-primary);
  font-weight: 500;
}
</style>
