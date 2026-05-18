<!--
  首次部署站长账号创建页面。

  :project: QWeb
  :file: BootstrapOwnerPage.vue
  :author: Qintsg
  :date: 2026-05-18 11:35
-->
<script setup lang="ts">
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { useAuthStore } from "@/stores/auth"

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const username = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const errorMsg = ref("")

const usernameHint = computed(() => t("auth.usernameRule"))

function validateForm(): boolean {
  if (!username.value.trim() || !email.value.trim() || !password.value || !confirmPassword.value) {
    errorMsg.value = t("auth.fillRegisterFields")
    return false
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = t("auth.passwordMismatch")
    return false
  }
  return true
}

async function handleCreateOwner(): Promise<void> {
  if (!validateForm()) return

  errorMsg.value = ""
  try {
    await authStore.createOwnerAccount({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
      password_confirm: confirmPassword.value,
    })
    router.push({ name: "dashboard" })
  } catch (err: unknown) {
    errorMsg.value = (err as Error).message || t("auth.bootstrapOwnerFailed")
  }
}
</script>

<template>
  <section class="auth-panel" aria-labelledby="bootstrap-owner-title">
    <header class="auth-panel__header">
      <p>首次部署</p>
      <h2 id="bootstrap-owner-title">{{ t('auth.bootstrapOwnerTitle') }}</h2>
      <span>{{ t('auth.bootstrapOwnerSubtitle') }}</span>
    </header>

    <form class="auth-form" @submit.prevent="handleCreateOwner">
      <div v-if="errorMsg" id="bootstrap-owner-error" class="auth-alert" role="alert">
        <span class="material-symbols-rounded" aria-hidden="true">error</span>
        <span>{{ errorMsg }}</span>
      </div>

      <md-outlined-text-field
        id="bootstrap-owner-username"
        :label="t('auth.username')"
        :value="username"
        supporting-text=" "
        autocomplete="username"
        required
        @input="username = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>
      <p class="auth-help">{{ usernameHint }}</p>

      <md-outlined-text-field
        id="bootstrap-owner-email"
        type="email"
        :label="t('auth.email')"
        :value="email"
        autocomplete="email"
        required
        @input="email = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>

      <md-outlined-text-field
        id="bootstrap-owner-password"
        type="password"
        :label="t('auth.password')"
        :value="password"
        autocomplete="new-password"
        required
        @input="password = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>

      <md-outlined-text-field
        id="bootstrap-owner-confirm"
        type="password"
        :label="t('auth.confirmPassword')"
        :value="confirmPassword"
        autocomplete="new-password"
        required
        @input="confirmPassword = ($event.target as HTMLInputElement).value"
      ></md-outlined-text-field>

      <md-filled-button
        type="submit"
        class="auth-button"
        :disabled="authStore.loading"
        :aria-busy="authStore.loading"
      >
        <md-circular-progress v-if="authStore.loading" slot="icon" indeterminate></md-circular-progress>
        {{ authStore.loading ? t('common.loading') : t('auth.createOwnerAccount') }}
      </md-filled-button>
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
.auth-help {
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
</style>
