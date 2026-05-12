<!--
  实现 GitHubCallbackPage 页面视图。

  :project: QWeb
  :file: GitHubCallbackPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import type { OAuthChoiceResponse } from '@/types/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n()

const loading = ref(true)
const actionLoading = ref(false)
const errorMsg = ref('')
const choice = ref<OAuthChoiceResponse | null>(null)
const existingLogin = ref('')
const existingPassword = ref('')
const newUsername = ref('')
const newNickname = ref('')

onMounted(async () => {
  const code = typeof route.query.code === 'string' ? route.query.code : ''
  const state = typeof route.query.state === 'string' ? route.query.state : ''

  if (!code || !state) {
    errorMsg.value = t('auth.githubCallbackMissing')
    loading.value = false
    return
  }

  try {
    const result = await authStore.completeGitHubOAuth({ code, state })
    if (result.status === 'requires_account_choice') {
      choice.value = result
      newUsername.value = result.suggested_username
      newNickname.value = result.suggested_nickname
      loading.value = false
      return
    }
    router.replace(result.redirect || '/dashboard')
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.githubLoginFailed')
    loading.value = false
  }
})

async function bindExistingAccount() {
  if (!choice.value || !existingLogin.value.trim() || !existingPassword.value) {
    errorMsg.value = t('auth.fillAllFields')
    return
  }
  actionLoading.value = true
  errorMsg.value = ''
  try {
    const result = await authStore.bindGitHubOAuth({
      pending_token: choice.value.pending_token,
      login: existingLogin.value.trim(),
      password: existingPassword.value,
    })
    router.replace(result.redirect || '/dashboard')
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.oauthBindFailed')
  } finally {
    actionLoading.value = false
  }
}

async function createNewAccount() {
  if (!choice.value || !newUsername.value.trim()) {
    errorMsg.value = t('auth.usernameRequired')
    return
  }
  actionLoading.value = true
  errorMsg.value = ''
  try {
    const result = await authStore.registerGitHubOAuth({
      pending_token: choice.value.pending_token,
      username: newUsername.value.trim(),
      nickname: newNickname.value.trim(),
    })
    router.replace(result.redirect || '/dashboard')
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t('auth.oauthRegisterFailed')
  } finally {
    actionLoading.value = false
  }
}
</script>

<template>
  <section class="oauth-page" aria-labelledby="oauth-title">
    <div v-if="loading" class="oauth-state">
      <fluent-progress-ring></fluent-progress-ring>
      <h1 id="oauth-title">{{ t('auth.githubCallbackProcessing') }}</h1>
      <p>{{ t('auth.githubCallbackHint') }}</p>
    </div>

    <div v-else-if="errorMsg && !choice" class="oauth-state">
      <h1 id="oauth-title">{{ t('auth.githubLoginFailed') }}</h1>
      <p class="oauth-error" role="alert">{{ errorMsg }}</p>
      <router-link to="/login" class="oauth-link">{{ t('auth.backToLogin') }}</router-link>
    </div>

    <div v-else-if="choice" class="oauth-choice">
      <header class="oauth-choice__header">
        <h1 id="oauth-title">{{ t('auth.oauthAccountChoiceTitle') }}</h1>
        <p>{{ t('auth.oauthAccountChoiceSubtitle') }}</p>
      </header>

      <div v-if="errorMsg" class="oauth-error" role="alert">{{ errorMsg }}</div>

      <div class="oauth-profile">
        <img v-if="choice.provider_avatar_url" :src="choice.provider_avatar_url" alt="" />
        <div>
          <strong>{{ choice.suggested_nickname || choice.suggested_username }}</strong>
          <span>{{ choice.provider_email || choice.provider }}</span>
        </div>
      </div>

      <p v-if="choice.email_matches_existing_account" class="oauth-notice">
        {{ t('auth.oauthEmailMatched') }}
      </p>

      <div class="oauth-grid">
        <form class="oauth-card" @submit.prevent="bindExistingAccount">
          <h2>{{ t('auth.bindExistingAccount') }}</h2>
          <div class="oauth-field">
            <label for="oauth-existing-login">{{ t('auth.accountIdentifier') }}</label>
            <fluent-text-field
              id="oauth-existing-login"
              :value="existingLogin"
              autocomplete="username"
              @input="existingLogin = ($event.target as HTMLInputElement).value"
            ></fluent-text-field>
          </div>
          <div class="oauth-field">
            <label for="oauth-existing-password">{{ t('auth.password') }}</label>
            <fluent-text-field
              id="oauth-existing-password"
              type="password"
              :value="existingPassword"
              autocomplete="current-password"
              @input="existingPassword = ($event.target as HTMLInputElement).value"
            ></fluent-text-field>
          </div>
          <fluent-button type="submit" appearance="accent" :disabled="actionLoading">
            {{ t('auth.bindAndLogin') }}
          </fluent-button>
        </form>

        <form class="oauth-card" @submit.prevent="createNewAccount">
          <h2>{{ t('auth.createOAuthAccount') }}</h2>
          <div class="oauth-field">
            <label for="oauth-new-username">{{ t('auth.username') }}</label>
            <fluent-text-field
              id="oauth-new-username"
              :value="newUsername"
              autocomplete="username"
              @input="newUsername = ($event.target as HTMLInputElement).value"
            ></fluent-text-field>
          </div>
          <div class="oauth-field">
            <label for="oauth-new-nickname">{{ t('auth.nickname') }}</label>
            <fluent-text-field
              id="oauth-new-nickname"
              :value="newNickname"
              @input="newNickname = ($event.target as HTMLInputElement).value"
            ></fluent-text-field>
          </div>
          <fluent-button type="submit" appearance="outline" :disabled="actionLoading">
            {{ t('auth.createAndLogin') }}
          </fluent-button>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.oauth-page {
  width: min(100%, 760px);
}

.oauth-state,
.oauth-choice {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-20);
}

.oauth-state {
  align-items: center;
  text-align: center;
}

.oauth-state h1,
.oauth-choice__header h1 {
  margin: 0;
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-2xl);
  font-weight: var(--q-font-weight-semibold);
}

.oauth-state p,
.oauth-choice__header p {
  margin: 0;
  color: var(--q-color-text-secondary);
  line-height: var(--q-line-height-base);
}

.oauth-error,
.oauth-notice {
  padding: var(--q-space-12) var(--q-space-16);
  border-radius: var(--q-radius-sm);
  font-size: var(--q-font-size-sm);
}

.oauth-error {
  border: 1px solid var(--q-color-error, #d13438);
  background: var(--q-color-error-light, #fde7e9);
  color: var(--q-color-error, #d13438);
}

.oauth-notice {
  border: 1px solid var(--q-color-stroke);
  background: var(--q-color-canvas);
  color: var(--q-color-text-secondary);
}

.oauth-profile {
  display: flex;
  align-items: center;
  gap: var(--q-space-12);
  padding: var(--q-space-12);
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-md);
  background: var(--q-color-canvas);
}

.oauth-profile img {
  width: 44px;
  height: 44px;
  border-radius: 50%;
}

.oauth-profile div {
  display: flex;
  min-width: 0;
  flex-direction: column;
}

.oauth-profile strong,
.oauth-profile span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.oauth-profile span {
  color: var(--q-color-text-secondary);
  font-size: var(--q-font-size-sm);
}

.oauth-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--q-space-16);
}

.oauth-card {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-16);
  padding: var(--q-space-20);
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-md);
}

.oauth-card h2 {
  margin: 0;
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-lg);
}

.oauth-field {
  display: flex;
  flex-direction: column;
  gap: var(--q-space-8);
}

.oauth-field label {
  color: var(--q-color-text-primary);
  font-size: var(--q-font-size-sm);
  font-weight: var(--q-font-weight-semibold);
}

.oauth-field fluent-text-field,
.oauth-card fluent-button {
  width: 100%;
}

.oauth-link {
  color: var(--q-color-brand);
  font-weight: var(--q-font-weight-semibold);
  text-decoration: none;
}

@media (max-width: 760px) {
  .oauth-grid {
    grid-template-columns: 1fr;
  }
}
</style>
