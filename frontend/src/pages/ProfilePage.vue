<!--
  个人资料页面视图。

  :project: QWeb
  :file: ProfilePage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { changePassword, updateMe } from "@/api/auth"
import { useAuth } from "@/composables/useAuth"
import { useAuthStore } from "@/stores/auth"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()
const { user, displayName, userGroup } = useAuth()
const authStore = useAuthStore()

const profileLoading = ref(false)
const profileMsg = ref({ type: "", text: "" })
const profileForm = ref({ nickname: "", phone: "", website: "", bio: "" })

const pwdLoading = ref(false)
const pwdMsg = ref({ type: "", text: "" })
const pwdForm = ref({ old_password: "", new_password: "", confirm_password: "" })

onMounted(() => {
  if (user.value) {
    profileForm.value.nickname = user.value.nickname || ""
    profileForm.value.phone = user.value.contact?.phone || ""
    profileForm.value.website = user.value.profile?.website || ""
    profileForm.value.bio = user.value.profile?.bio || ""
  }
})

async function handleUpdateProfile(): Promise<void> {
  profileLoading.value = true
  profileMsg.value = { type: "", text: "" }
  try {
    const payload = {
      nickname: profileForm.value.nickname,
      contact: { phone: profileForm.value.phone },
      profile: { website: profileForm.value.website, bio: profileForm.value.bio },
    }
    const res = await updateMe(payload as never)
    authStore.user = res.data.data
    profileMsg.value = { type: "success", text: "Profile updated successfully!" }
  } catch (err: unknown) {
    profileMsg.value = { type: "error", text: (err as Error).message || "Update failed" }
  } finally {
    profileLoading.value = false
  }
}

async function handleChangePassword(): Promise<void> {
  if (pwdForm.value.new_password !== pwdForm.value.confirm_password) {
    pwdMsg.value = { type: "error", text: "Passwords do not match" }
    return
  }
  pwdLoading.value = true
  pwdMsg.value = { type: "", text: "" }
  try {
    await changePassword({
      old_password: pwdForm.value.old_password,
      new_password: pwdForm.value.new_password,
      new_password_confirm: pwdForm.value.confirm_password,
    })
    pwdMsg.value = { type: "success", text: "Password changed successfully!" }
    pwdForm.value = { old_password: "", new_password: "", confirm_password: "" }
  } catch (err: unknown) {
    pwdMsg.value = { type: "error", text: (err as Error).message || "Change password failed" }
  } finally {
    pwdLoading.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <PageHeader :title="t('nav.profile')" description="管理个人资料、联系信息和本地密码。" eyebrow="Identity">
      <template #actions>
        <StatusPill :label="userGroup" tone="primary" icon="verified_user" />
      </template>
    </PageHeader>

    <div v-if="user" class="profile-grid">
      <section class="profile-card ident-card" aria-labelledby="identity-title">
        <div class="profile-avatar" aria-hidden="true">{{ displayName.charAt(0).toUpperCase() }}</div>
        <div class="profile-info">
          <h2 id="identity-title">{{ displayName }}</h2>
          <p>{{ user.username }} · {{ user.contact?.email || '-' }}</p>
          <StatusPill :label="userGroup" tone="primary" icon="badge" />
        </div>
      </section>

      <section class="profile-card" aria-labelledby="edit-profile-title">
        <h2 id="edit-profile-title">Edit Profile</h2>
        <form class="profile-form" @submit.prevent="handleUpdateProfile">
          <div v-if="profileMsg.text" :class="['alert', `alert--${profileMsg.type}`]" role="status">
            <span class="material-symbols-rounded" aria-hidden="true">{{ profileMsg.type === 'success' ? 'check_circle' : 'error' }}</span>
            <span>{{ profileMsg.text }}</span>
          </div>
          <md-outlined-text-field :value="profileForm.nickname" :label="t('auth.nickname')" @input="profileForm.nickname = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-outlined-text-field :value="profileForm.phone" label="Phone" @input="profileForm.phone = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-outlined-text-field :value="profileForm.website" label="Website" @input="profileForm.website = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-outlined-text-field :value="profileForm.bio" label="Bio" type="textarea" rows="3" @input="profileForm.bio = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-filled-button type="submit" :disabled="profileLoading" :aria-busy="profileLoading">
            {{ profileLoading ? t('common.loading') : 'Save Changes' }}
          </md-filled-button>
        </form>
      </section>

      <section class="profile-card" aria-labelledby="password-title">
        <h2 id="password-title">Change Password</h2>
        <form class="profile-form" @submit.prevent="handleChangePassword">
          <div v-if="pwdMsg.text" :class="['alert', `alert--${pwdMsg.type}`]" role="status">
            <span class="material-symbols-rounded" aria-hidden="true">{{ pwdMsg.type === 'success' ? 'check_circle' : 'error' }}</span>
            <span>{{ pwdMsg.text }}</span>
          </div>
          <md-outlined-text-field type="password" :value="pwdForm.old_password" label="Current Password" required @input="pwdForm.old_password = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-outlined-text-field type="password" :value="pwdForm.new_password" label="New Password" required @input="pwdForm.new_password = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-outlined-text-field type="password" :value="pwdForm.confirm_password" label="Confirm New Password" required @input="pwdForm.confirm_password = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
          <md-filled-button type="submit" :disabled="pwdLoading" :aria-busy="pwdLoading">
            {{ pwdLoading ? t('common.loading') : 'Change Password' }}
          </md-filled-button>
        </form>
      </section>
    </div>
  </div>
</template>

<style scoped>
.profile-page,
.profile-grid,
.profile-card,
.profile-form {
  display: grid;
  gap: var(--space-lg);
}

.profile-grid {
  grid-template-columns: minmax(0, 24rem) minmax(0, 1fr);
  align-items: start;
}

.profile-card {
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
}

.ident-card {
  position: sticky;
  inset-block-start: 5.5rem;
}

.profile-avatar {
  inline-size: 5rem;
  block-size: 5rem;
  display: grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-primary);
  background: linear-gradient(135deg, var(--md-sys-color-primary), var(--md-sys-color-tertiary));
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  line-height: var(--md-sys-typescale-headline-large-line-height);
}

.profile-info,
.alert {
  display: grid;
  gap: var(--space-sm);
}

.profile-card h2,
.profile-info h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.profile-info p {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.profile-form md-outlined-text-field,
.profile-form md-filled-button {
  inline-size: 100%;
}

.alert {
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  padding: var(--space-md);
  border-radius: var(--md-sys-shape-corner-large);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.alert--success {
  color: var(--md-sys-color-on-secondary-container);
  background: var(--md-sys-color-secondary-container);
}

.alert--error {
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
}

@media (max-width: 839px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }

  .ident-card {
    position: static;
  }
}
</style>
