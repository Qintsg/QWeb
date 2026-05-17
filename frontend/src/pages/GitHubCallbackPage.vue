<!--
  GitHub OAuth 回调页面视图。

  :project: QWeb
  :file: GitHubCallbackPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { useAuthStore } from "@/stores/auth"
import type { OAuthChoiceResponse } from "@/types/auth"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n()

const loading = ref(true)
const actionLoading = ref(false)
const errorMsg = ref("")
const choice = ref<OAuthChoiceResponse | null>(null)
const existingLogin = ref("")
const existingPassword = ref("")
const newUsername = ref("")
const newNickname = ref("")

onMounted(async () => {
  const code = typeof route.query.code === "string" ? route.query.code : ""
  const state = typeof route.query.state === "string" ? route.query.state : ""

  if (!code || !state) {
    errorMsg.value = t("auth.githubCallbackMissing")
    loading.value = false
    return
  }

  try {
    const result = await authStore.completeGitHubOAuth({ code, state })
    if (result.status === "requires_account_choice") {
      choice.value = result
      newUsername.value = result.suggested_username
      newNickname.value = result.suggested_nickname
      loading.value = false
      return
    }
    router.replace(result.redirect || "/dashboard")
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.githubLoginFailed")
    loading.value = false
  }
})

async function bindExistingAccount(): Promise<void> {
  if (!choice.value || !existingLogin.value.trim() || !existingPassword.value) {
    errorMsg.value = t("auth.fillAllFields")
    return
  }
  actionLoading.value = true
  errorMsg.value = ""
  try {
    const result = await authStore.bindGitHubOAuth({
      pending_token: choice.value.pending_token,
      login: existingLogin.value.trim(),
      password: existingPassword.value,
    })
    router.replace(result.redirect || "/dashboard")
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.oauthBindFailed")
  } finally {
    actionLoading.value = false
  }
}

async function createNewAccount(): Promise<void> {
  if (!choice.value || !newUsername.value.trim()) {
    errorMsg.value = t("auth.usernameRequired")
    return
  }
  actionLoading.value = true
  errorMsg.value = ""
  try {
    const result = await authStore.registerGitHubOAuth({
      pending_token: choice.value.pending_token,
      username: newUsername.value.trim(),
      nickname: newNickname.value.trim(),
    })
    router.replace(result.redirect || "/dashboard")
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.oauthRegisterFailed")
  } finally {
    actionLoading.value = false
  }
}
</script>

<template>
  <section class="oauth-page" aria-labelledby="oauth-title">
    <div v-if="loading" class="oauth-state" role="status" aria-live="polite">
      <md-circular-progress indeterminate aria-label="正在处理 GitHub 登录"></md-circular-progress>
      <h2 id="oauth-title">{{ t('auth.githubCallbackProcessing') }}</h2>
      <p>{{ t('auth.githubCallbackHint') }}</p>
    </div>

    <div v-else-if="errorMsg && !choice" class="oauth-state">
      <span class="material-symbols-rounded oauth-state__icon" aria-hidden="true">error</span>
      <h2 id="oauth-title">{{ t('auth.githubLoginFailed') }}</h2>
      <p class="oauth-alert" role="alert">{{ errorMsg }}</p>
      <router-link to="/login" class="oauth-link">{{ t('auth.backToLogin') }}</router-link>
    </div>

    <div v-else-if="choice" class="oauth-choice">
      <header class="oauth-choice__header">
        <p>GitHub OAuth</p>
        <h2 id="oauth-title">{{ t('auth.oauthAccountChoiceTitle') }}</h2>
        <span>{{ t('auth.oauthAccountChoiceSubtitle') }}</span>
      </header>

      <div v-if="errorMsg" class="oauth-alert" role="alert">
        <span class="material-symbols-rounded" aria-hidden="true">error</span>
        <span>{{ errorMsg }}</span>
      </div>

      <div class="oauth-profile">
        <img
          v-if="choice.provider_avatar_url"
          :src="choice.provider_avatar_url"
          alt=""
          width="56"
          height="56"
        />
        <span v-else class="oauth-profile__fallback" aria-hidden="true">G</span>
        <div>
          <strong>{{ choice.suggested_nickname || choice.suggested_username }}</strong>
          <span>{{ choice.provider_email || choice.provider }}</span>
        </div>
      </div>

      <p v-if="choice.email_matches_existing_account" class="oauth-notice">
        <span class="material-symbols-rounded" aria-hidden="true">info</span>
        {{ t('auth.oauthEmailMatched') }}
      </p>

      <div class="oauth-grid">
        <form class="oauth-card" @submit.prevent="bindExistingAccount">
          <h3>{{ t('auth.bindExistingAccount') }}</h3>
          <md-outlined-text-field
            id="oauth-existing-login"
            :label="t('auth.accountIdentifier')"
            :value="existingLogin"
            autocomplete="username"
            required
            @input="existingLogin = ($event.target as HTMLInputElement).value"
          ></md-outlined-text-field>
          <md-outlined-text-field
            id="oauth-existing-password"
            type="password"
            :label="t('auth.password')"
            :value="existingPassword"
            autocomplete="current-password"
            required
            @input="existingPassword = ($event.target as HTMLInputElement).value"
          ></md-outlined-text-field>
          <md-filled-button type="submit" :disabled="actionLoading" :aria-busy="actionLoading">
            {{ t('auth.bindAndLogin') }}
          </md-filled-button>
        </form>

        <form class="oauth-card" @submit.prevent="createNewAccount">
          <h3>{{ t('auth.createOAuthAccount') }}</h3>
          <md-outlined-text-field
            id="oauth-new-username"
            :label="t('auth.username')"
            :value="newUsername"
            autocomplete="username"
            required
            @input="newUsername = ($event.target as HTMLInputElement).value"
          ></md-outlined-text-field>
          <md-outlined-text-field
            id="oauth-new-nickname"
            :label="t('auth.nickname')"
            :value="newNickname"
            @input="newNickname = ($event.target as HTMLInputElement).value"
          ></md-outlined-text-field>
          <md-outlined-button type="submit" :disabled="actionLoading" :aria-busy="actionLoading">
            {{ t('auth.createAndLogin') }}
          </md-outlined-button>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.oauth-page {
  inline-size: min(100%, 48rem);
}

.oauth-state,
.oauth-choice,
.oauth-choice__header {
  display: grid;
  gap: var(--space-md);
}

.oauth-state {
  place-items: center;
  text-align: center;
}

.oauth-state__icon {
  inline-size: 3rem;
  block-size: 3rem;
  display: inline-grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
}

.oauth-choice__header p {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.oauth-state h2,
.oauth-choice__header h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.oauth-state p,
.oauth-choice__header span {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.oauth-alert,
.oauth-notice,
.oauth-profile {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  border-radius: var(--md-sys-shape-corner-large);
}

.oauth-alert {
  border: 0.0625rem solid var(--md-sys-color-error);
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
}

.oauth-notice,
.oauth-profile {
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  color: var(--md-sys-color-on-surface-variant);
  background: var(--md-sys-color-surface-container-low);
}

.oauth-profile img,
.oauth-profile__fallback {
  inline-size: 3.5rem;
  block-size: 3.5rem;
  border-radius: var(--md-sys-shape-corner-full);
}

.oauth-profile__fallback {
  display: inline-grid;
  place-items: center;
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
}

.oauth-profile div {
  min-inline-size: 0;
  display: grid;
  gap: var(--space-xs);
}

.oauth-profile strong,
.oauth-profile span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.oauth-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-md);
}

.oauth-card {
  display: grid;
  gap: var(--space-md);
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
}

.oauth-card h3 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.oauth-card md-outlined-text-field,
.oauth-card md-filled-button,
.oauth-card md-outlined-button {
  inline-size: 100%;
}

.oauth-link {
  min-block-size: 3rem;
  display: inline-flex;
  align-items: center;
  color: var(--md-sys-color-primary);
  font-weight: var(--md-sys-typescale-label-large-weight);
}

@media (max-width: 760px) {
  .oauth-grid {
    grid-template-columns: 1fr;
  }
}
</style>
