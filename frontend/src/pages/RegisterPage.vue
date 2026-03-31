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
    <fluent-card class="register-card">
      <h1 class="register-title">{{ t('auth.register') }}</h1>

      <form class="register-form" @submit.prevent="handleRegister">
        <div v-if="errorMsg" class="register-error">{{ errorMsg }}</div>

        <div class="form-field">
          <label for="reg-username">{{ t('auth.username') }}</label>
          <fluent-text-field
            id="reg-username"
            :value="username"
            @input="username = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.username')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <div class="form-field">
          <label for="reg-email">{{ t('auth.email') }}</label>
          <fluent-text-field
            id="reg-email"
            type="email"
            :value="email"
            @input="email = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.email')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <div class="form-field">
          <label for="reg-password">{{ t('auth.password') }}</label>
          <fluent-text-field
            id="reg-password"
            type="password"
            :value="password"
            @input="password = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.password')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <div class="form-field">
          <label for="reg-confirm">{{ t('auth.confirmPassword') }}</label>
          <fluent-text-field
            id="reg-confirm"
            type="password"
            :value="confirmPassword"
            @input="confirmPassword = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.confirmPassword')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <fluent-button
          type="submit"
          appearance="accent"
          class="register-btn"
          :disabled="loading"
          @click="handleRegister"
        >
          {{ loading ? t('common.loading') : t('auth.register') }}
        </fluent-button>

        <p class="register-link">
          {{ t('auth.hasAccount') }}
          <router-link to="/login">
            <fluent-anchor appearance="hyperlink">{{ t('auth.login') }}</fluent-anchor>
          </router-link>
        </p>
      </form>
    </fluent-card>
  </div>
</template>

<style scoped>
.register-page {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.register-card {
  padding: var(--q-space-32);
  border-radius: var(--q-radius-lg);
  box-shadow: var(--q-shadow-md);
  background: var(--q-color-surface);
}

.register-title {
  margin: 0 0 var(--q-space-32);
  font-size: 1.75rem;
  font-weight: 600;
  text-align: center;
  color: var(--q-color-text-primary);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-24);
}

.register-error {
  padding: var(--q-space-12) var(--q-space-16);
  border-radius: var(--q-radius-sm);
  background: var(--q-color-error-light, #fde7e7);
  color: var(--q-color-error, #d32f2f);
  font-size: 0.875rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-8);
}

.form-field label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--q-color-text-secondary);
}

.register-btn {
  width: 100%;
  margin-top: var(--q-space-12);
}

.register-link {
  text-align: center;
  font-size: 0.875rem;
  margin-top: var(--q-space-16);
  color: var(--q-color-text-secondary);
}

.register-link a {
  text-decoration: none;
}
</style>
