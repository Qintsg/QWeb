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
    <fluent-card class="login-card">
      <h1 class="login-title">{{ t('auth.login') }}</h1>

      <form class="login-form" @submit.prevent="handleLogin">
        <div v-if="errorMsg" class="login-error">{{ errorMsg }}</div>

        <div class="form-field">
          <label for="username">{{ t('auth.username') }}</label>
          <fluent-text-field
            id="username"
            :value="username"
            @input="username = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.username')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <div class="form-field">
          <label for="password">{{ t('auth.password') }}</label>
          <fluent-text-field
            id="password"
            type="password"
            :value="password"
            @input="password = ($event.target as HTMLInputElement).value"
            :placeholder="t('auth.password')"
            required
            style="width: 100%"
          ></fluent-text-field>
        </div>

        <fluent-button
          type="submit"
          appearance="accent"
          class="login-btn"
          :disabled="loading"
          @click="handleLogin"
        >
          {{ loading ? t('common.loading') : t('auth.login') }}
        </fluent-button>

        <p class="login-link">
          {{ t('auth.noAccount') }}
          <router-link to="/register">
            <fluent-anchor appearance="hyperlink">{{ t('auth.register') }}</fluent-anchor>
          </router-link>
        </p>
      </form>
    </fluent-card>
  </div>
</template>

<style scoped>
.login-page {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.login-card {
  padding: var(--qweb-spacing-xl);
  border-radius: var(--qweb-radius-lg);
  box-shadow: var(--qweb-shadow-md);
  background: var(--qweb-surface);
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

.login-btn {
  width: 100%;
  margin-top: var(--qweb-spacing-sm);
}

.login-link {
  text-align: center;
  font-size: 0.875rem;
  margin-top: var(--qweb-spacing-md);
  color: var(--qweb-text-secondary);
}

.login-link a {
  text-decoration: none;
}
</style>
