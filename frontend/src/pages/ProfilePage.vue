<script setup lang="ts">
/**
 * 个人资料页面
 */
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'
import { useAuthStore } from '@/stores/auth'
import { updateMe, changePassword } from '@/api/auth'

const { t } = useI18n()
const { user, displayName, userGroup } = useAuth()
const authStore = useAuthStore()

// Profile Form
const profileLoading = ref(false)
const profileMsg = ref({ type: '', text: '' })
const profileForm = ref({
  display_name: '',
  phone: '',
  website: '',
  bio: '',
})

// Password Form
const pwdLoading = ref(false)
const pwdMsg = ref({ type: '', text: '' })
const pwdForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

onMounted(() => {
  if (user.value) {
    profileForm.value.display_name = user.value.display_name || ''
    profileForm.value.phone = user.value.profile?.phone || ''
    profileForm.value.website = user.value.profile?.website || ''
    profileForm.value.bio = user.value.profile?.bio || ''
  }
})

async function handleUpdateProfile() {
  profileLoading.value = true
  profileMsg.value = { type: '', text: '' }
  try {
    const payload = {
      display_name: profileForm.value.display_name,
      profile: {
        phone: profileForm.value.phone,
        website: profileForm.value.website,
        bio: profileForm.value.bio,
      }
    }
    const res = await updateMe(payload as any)
    // 更新本地 state
    authStore.user = res.data.data
    profileMsg.value = { type: 'success', text: 'Profile updated successfully!' }
  } catch (err: any) {
    profileMsg.value = { type: 'error', text: err.message || 'Update failed' }
  } finally {
    profileLoading.value = false
  }
}

async function handleChangePassword() {
  if (pwdForm.value.new_password !== pwdForm.value.confirm_password) {
    pwdMsg.value = { type: 'error', text: 'Passwords do not match' }
    return
  }
  pwdLoading.value = true
  pwdMsg.value = { type: '', text: '' }
  try {
    await changePassword({
      old_password: pwdForm.value.old_password,
      new_password: pwdForm.value.new_password,
      new_password_confirm: pwdForm.value.confirm_password,
    })
    pwdMsg.value = { type: 'success', text: 'Password changed successfully!' }
    pwdForm.value = { old_password: '', new_password: '', confirm_password: '' } // reset
  } catch (err: any) {
    pwdMsg.value = { type: 'error', text: err.message || 'Change password failed' }
  } finally {
    pwdLoading.value = false
  }
}
</script>

<template>
  <div class="page-container">
    <h1 class="page-title">{{ t('nav.profile') }}</h1>

    <div class="grid-layout" v-if="user">
      <!-- Profile Header / Ident -->
      <fluent-card class="profile-card ident-card">
        <div class="profile-avatar">{{ displayName.charAt(0).toUpperCase() }}</div>
        <div class="profile-info">
          <h2>{{ displayName }}</h2>
          <p>{{ user.username }} ({{ user.email }})</p>
          <span class="profile-group">{{ userGroup }}</span>
        </div>
      </fluent-card>

      <!-- Edit Profile -->
      <fluent-card class="profile-card">
        <h3>Edit Profile</h3>
        <form class="fluent-form" @submit.prevent="handleUpdateProfile">
          <div v-if="profileMsg.text" :class="['alert', 'alert-' + profileMsg.type]">
            {{ profileMsg.text }}
          </div>

          <div class="form-field">
            <label>Display Name</label>
            <fluent-text-field
              :value="profileForm.display_name"
              @input="profileForm.display_name = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <div class="form-field">
            <label>Phone</label>
            <fluent-text-field
              :value="profileForm.phone"
              @input="profileForm.phone = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <div class="form-field">
            <label>Website</label>
            <fluent-text-field
              :value="profileForm.website"
              @input="profileForm.website = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <div class="form-field">
            <label>Bio</label>
            <fluent-text-area
              :value="profileForm.bio"
              @input="profileForm.bio = ($event.target as HTMLInputElement).value"
              rows="3"
              style="width: 100%"
            ></fluent-text-area>
          </div>

          <fluent-button
            type="submit"
            appearance="accent"
            :disabled="profileLoading"
            @click="handleUpdateProfile"
          >
            {{ profileLoading ? t('common.loading') : 'Save Changes' }}
          </fluent-button>
        </form>
      </fluent-card>

      <!-- Change Password -->
      <fluent-card class="profile-card">
        <h3>Change Password</h3>
        <form class="fluent-form" @submit.prevent="handleChangePassword">
          <div v-if="pwdMsg.text" :class="['alert', 'alert-' + pwdMsg.type]">
            {{ pwdMsg.text }}
          </div>

          <div class="form-field">
            <label>Current Password</label>
            <fluent-text-field
              type="password"
              :value="pwdForm.old_password"
              @input="pwdForm.old_password = ($event.target as HTMLInputElement).value"
              required
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <div class="form-field">
            <label>New Password</label>
            <fluent-text-field
              type="password"
              :value="pwdForm.new_password"
              @input="pwdForm.new_password = ($event.target as HTMLInputElement).value"
              required
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <div class="form-field">
            <label>Confirm New Password</label>
            <fluent-text-field
              type="password"
              :value="pwdForm.confirm_password"
              @input="pwdForm.confirm_password = ($event.target as HTMLInputElement).value"
              required
              style="width: 100%"
            ></fluent-text-field>
          </div>

          <fluent-button
            type="submit"
            appearance="accent"
            :disabled="pwdLoading"
            @click="handleChangePassword"
          >
            {{ pwdLoading ? t('common.loading') : 'Change Password' }}
          </fluent-button>
        </form>
      </fluent-card>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: var(--qweb-spacing-xl);
}

.page-title {
  margin: 0 0 var(--qweb-spacing-lg);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.grid-layout {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-lg);
  max-width: 600px;
}

.profile-card {
  padding: var(--qweb-spacing-xl);
  border-radius: var(--qweb-radius-lg);
  background: var(--qweb-surface);
  box-shadow: var(--qweb-shadow-sm);
}

.ident-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--qweb-spacing-lg);
}

h3 {
  margin-top: 0;
  margin-bottom: var(--qweb-spacing-lg);
  font-size: 1.25rem;
  color: var(--qweb-text-primary);
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--qweb-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  flex-shrink: 0;
}

.profile-info h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--qweb-text-primary);
}

.profile-info p {
  margin: var(--qweb-spacing-xs) 0 0;
  color: var(--qweb-text-secondary);
  font-size: 0.875rem;
}

.profile-group {
  display: inline-block;
  margin-top: var(--qweb-spacing-sm);
  padding: 2px 10px;
  border-radius: var(--qweb-radius-full);
  background: var(--qweb-primary-light, rgba(14, 154, 167, 0.1));
  color: var(--qweb-primary);
  font-size: 0.75rem;
  font-weight: 600;
}

.fluent-form {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-lg);
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

.alert {
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
  border-radius: var(--qweb-radius-sm);
  font-size: 0.875rem;
}
.alert-error {
  background: var(--qweb-danger-light, #fde7e7);
  color: var(--qweb-danger, #d32f2f);
}
.alert-success {
  background: rgba(16, 124, 16, 0.1);
  color: #107c10;
}
</style>



