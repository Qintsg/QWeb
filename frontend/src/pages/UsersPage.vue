<!--
  用户管理页面视图。

  :project: QWeb
  :file: UsersPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { getUsers, toggleUserActive, updateUser, type UserListQuery } from "@/api/users"
import type { UserGroup, UserInfo } from "@/types/auth"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()

const loading = ref(false)
const users = ref<UserInfo[]>([])
const totalCount = ref(0)
const query = ref<UserListQuery>({
  page: 1,
  page_size: 10,
  search: "",
})

const isDialogOpen = ref(false)
const editId = ref("")
const dialogForm = ref({
  username: "",
  email: "",
  nickname: "",
  user_group: "user",
})

const userGroups: UserGroup[] = ["owner", "admin", "trusted", "user", "guest"]

async function fetchUsers(): Promise<void> {
  loading.value = true
  try {
    const res = await getUsers(query.value)
    const data = res.data.data
    users.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error("Failed to fetch users", err)
  } finally {
    loading.value = false
  }
}

function handleSearch(): void {
  query.value.page = 1
  fetchUsers()
}

function openEdit(user: UserInfo): void {
  editId.value = String(user.uid)
  dialogForm.value = {
    username: user.username,
    email: user.contact?.email || "",
    nickname: user.nickname || "",
    user_group: user.user_type === "admin" ? "admin" : "user",
  }
  isDialogOpen.value = true
}

function closeDialog(): void {
  isDialogOpen.value = false
}

async function handleSave(): Promise<void> {
  try {
    const payload: Partial<UserInfo> = {
      nickname: dialogForm.value.nickname,
      contact: { email: dialogForm.value.email } as UserInfo["contact"],
    }
    await updateUser(editId.value, payload)
    isDialogOpen.value = false
    fetchUsers()
  } catch (err) {
    console.error("Save user failed", err)
    window.alert("Save failed. See console for details.")
  }
}

async function handleToggleActive(user: UserInfo): Promise<void> {
  const action = user.is_active ? "disable" : "enable"
  if (window.confirm(`Are you sure you want to ${action} user ${user.username}?`)) {
    try {
      await toggleUserActive(user.uid)
      fetchUsers()
    } catch (err) {
      console.error("Toggle active failed", err)
      window.alert("Operation failed. See console for details.")
    }
  }
}

function userTone(user: UserInfo): "primary" | "success" | "error" {
  if (!user.is_active) return "error"
  if (user.user_type === "admin") return "primary"
  return "success"
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="data-page">
    <PageHeader
      :title="t('nav.users', 'User Management')"
      description="管理账号状态、联系方式与后台可见身份信息。"
      eyebrow="Accounts"
    >
      <template #actions>
        <StatusPill :label="`${totalCount} users`" tone="primary" icon="group" />
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="users-table-title">
      <div class="data-toolbar">
        <h2 id="users-table-title">用户列表</h2>
        <md-outlined-text-field
          :value="query.search"
          label="Search username or email"
          @input="query.search = ($event.target as HTMLInputElement).value"
          @keyup.enter="handleSearch"
        >
          <span slot="trailing-icon" class="material-symbols-rounded" aria-hidden="true">search</span>
        </md-outlined-text-field>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Display Name</th>
              <th scope="col">Group</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="table-state">Loading...</td>
            </tr>
            <tr v-else-if="users.length === 0">
              <td colspan="6" class="table-state">No users found.</td>
            </tr>
            <tr v-for="user in users" v-else :key="user.uid">
              <td>{{ user.username }}</td>
              <td>{{ user.contact?.email || '-' }}</td>
              <td>{{ user.nickname || '-' }}</td>
              <td><StatusPill :label="user.user_type" :tone="userTone(user)" icon="badge" /></td>
              <td><StatusPill :label="user.is_active ? 'Active' : 'Inactive'" :tone="user.is_active ? 'success' : 'error'" :icon="user.is_active ? 'check_circle' : 'block'" /></td>
              <td>
                <div class="row-actions">
                  <md-text-button type="button" @click="openEdit(user)">Edit</md-text-button>
                  <md-text-button type="button" @click="handleToggleActive(user)">
                    {{ user.is_active ? 'Disable' : 'Enable' }}
                  </md-text-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="totalCount > query.page_size!" class="pagination">
        <md-outlined-button type="button" :disabled="query.page === 1" @click="query.page!--; fetchUsers()">Prev</md-outlined-button>
        <span>Page {{ query.page }}</span>
        <md-outlined-button type="button" :disabled="(query.page! * query.page_size!) >= totalCount" @click="query.page!++; fetchUsers()">Next</md-outlined-button>
      </div>
    </section>

    <md-dialog :open="isDialogOpen" @closed="closeDialog">
      <div slot="headline">Edit User</div>
      <form slot="content" class="dialog-form" method="dialog" @submit.prevent="handleSave">
        <md-outlined-text-field :value="dialogForm.username" label="Username" disabled></md-outlined-text-field>
        <md-outlined-text-field type="email" :value="dialogForm.email" label="Email" @input="dialogForm.email = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="dialogForm.nickname" label="Nickname" @input="dialogForm.nickname = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-select :value="dialogForm.user_group" label="User Group" disabled>
          <md-select-option v-for="group in userGroups" :key="group" :value="group">{{ group }}</md-select-option>
        </md-outlined-select>
      </form>
      <div slot="actions">
        <md-text-button type="button" @click="closeDialog">Cancel</md-text-button>
        <md-filled-button type="button" @click="handleSave">Save</md-filled-button>
      </div>
    </md-dialog>
  </div>
</template>

<style scoped>
.data-page,
.data-surface,
.dialog-form {
  display: grid;
  gap: var(--space-lg);
}

.data-surface {
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
}

.data-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-md);
}

.data-toolbar h2 {
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.data-toolbar md-outlined-text-field {
  inline-size: min(100%, 22rem);
}

.table-wrap {
  overflow-x: auto;
}

table {
  inline-size: 100%;
  border-collapse: collapse;
}

th,
td {
  padding-block: var(--space-md);
  padding-inline: var(--space-md);
  border-block-end: 0.0625rem solid var(--md-sys-color-outline-variant);
  text-align: start;
  vertical-align: middle;
}

th {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

td,
.pagination {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.table-state {
  padding: var(--space-xxl);
  color: var(--md-sys-color-on-surface-variant);
  text-align: center;
}

.row-actions,
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.pagination {
  justify-content: center;
}

.dialog-form md-outlined-text-field,
.dialog-form md-outlined-select {
  inline-size: min(100%, 28rem);
}

@media (max-width: 839px) {
  .data-toolbar {
    align-items: start;
    flex-direction: column;
  }

  .data-toolbar md-outlined-text-field {
    inline-size: 100%;
  }
}
</style>
