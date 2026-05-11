<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n()

const errorMsg = ref('')

onMounted(async () => {
  const code = typeof route.query.code === 'string' ? route.query.code : ''
  const state = typeof route.query.state === 'string' ? route.query.state : ''

  if (!code || !state) {
    errorMsg.value = t('auth.githubCallbackMissing')
    return
  }

  try {
    const result = await authStore.completeGitHubOAuth({ code, state })
    router.replace(result.redirect || '/dashboard')
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.githubLoginFailed')
  }
})
</script>

<template>
  <div class="github-callback-page">
    <fluent-card class="github-callback-card">
      <fluent-progress-ring v-if="!errorMsg"></fluent-progress-ring>
      <h1 class="github-callback-title">
        {{ errorMsg ? t('auth.githubLoginFailed') : t('auth.githubCallbackProcessing') }}
      </h1>
      <p class="github-callback-text">
        {{ errorMsg || t('auth.githubCallbackHint') }}
      </p>
      <router-link v-if="errorMsg" to="/login" class="github-callback-link">
        {{ t('auth.backToLogin') }}
      </router-link>
    </fluent-card>
  </div>
</template>

<style scoped>
.github-callback-page {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
}

.github-callback-card {
  padding: var(--q-space-32);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--q-space-16);
  text-align: center;
  border-radius: var(--q-radius-lg);
  background: var(--q-color-surface);
  box-shadow: var(--q-shadow-md);
}

.github-callback-title {
  margin: 0;
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-xl);
  font-weight: var(--q-font-weight-semibold);
}

.github-callback-text {
  margin: 0;
  color: var(--q-color-text-secondary);
  line-height: var(--q-line-height-base);
}

.github-callback-link {
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: var(--q-space-8);
  padding: 0 var(--q-space-20);
  border-radius: var(--q-radius-sm);
  background: var(--q-color-brand);
  color: var(--q-color-text-on-brand);
  font-weight: var(--q-font-weight-semibold);
  text-decoration: none;
}

.github-callback-link:hover,
.github-callback-link:focus-visible {
  background: var(--q-color-brand-hover);
  outline: none;
}
</style>
