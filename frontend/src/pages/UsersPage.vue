<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getUsers, createUser, updateUser, deleteUser, type UserListQuery, type CreateUserRequest } from '@/api/users'
import type { UserInfo, UserGroup } from '@/types/auth'

const { t } = useI18n()

const loading = ref(false)
const users = ref<UserInfo[]>([])
const totalCount = ref(0)
const query = ref<UserListQuery>({
  page: 1,
  page_size: 10,
  search: '',
})

const isDialogOpen = ref(false)
const dialogMode = ref<'create'|'edit'>('create')
const editId = ref('')
const dialogForm = ref<CreateUserRequest>({
  username: '',
  email: '',
  password: '',
  display_name: '',
  user_group: 'user',
})

const userGroups: UserGroup[] = ['owner', 'admin', 'trusted', 'user', 'guest']

async function fetchUsers() {
  loading.value = true
  try {
    const res = await getUsers(query.value)
    // res.data 遵循 ApiResponse<PaginatedResponse<UserInfo>>
    const data = res.data.data
    users.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error('Failed to fetch users', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})

function handleSearch() {
  query.value.page = 1
  fetchUsers()
}

function openCreate() {
  dialogMode.value = 'create'
  dialogForm.value = {
    username: '',
    email: '',
    password: '',
    display_name: '',
    user_group: 'user',
  }
  isDialogOpen.value = true
}

function openEdit(user: UserInfo) {
  dialogMode.value = 'edit'
  editId.value = user.id
  dialogForm.value = {
    username: user.username,
    email: user.email,
    password: '', // Leave blank, only fill if changing
    display_name: user.display_name || '',
    user_group: user.user_group,
  }
  isDialogOpen.value = true
}

function closeDialog() {
  isDialogOpen.value = false
}

async function handleSave() {
  try {
    if (dialogMode.value === 'create') {
      await createUser(dialogForm.value)
    } else {
      const payload: Partial<UserInfo> = {
        email: dialogForm.value.email,
        display_name: dialogForm.value.display_name,
        user_group: dialogForm.value.user_group,
      }
      if (dialogForm.value.password) {
        // Assume API takes password in patch if we want to reset it, or we handle it separately.
        (payload as any).password = dialogForm.value.password
      }
      await updateUser(editId.value, payload)
    }
    isDialogOpen.value = false
    fetchUsers()
  } catch (err) {
    console.error('Save user failed', err)
    alert('Save failed. See console for details.')
  }
}

async function handleDelete(user: UserInfo) {
  if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
    try {
      await deleteUser(user.id)
      fetchUsers()
    } catch (err) {
      console.error('Delete failed', err)
      alert('Delete failed. See console for details.')
    }
  }
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.users', 'User Management') }}</h1>
      <fluent-button appearance="accent" @click="openCreate">Add User</fluent-button>
    </div>

    <fluent-card class="table-card">
      <div class="toolbar">
        <fluent-text-field
          :value="query.search"
          @input="query.search = ($event.target as HTMLInputElement).value"
          @keyup.enter="handleSearch"
          placeholder="Search username or email..."
        >
          <span slot="end" class="search-icon" @click="handleSearch">🔍</span>
        </fluent-text-field>
      </div>

      <div class="table-responsive">
        <table class="qweb-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Display Name</th>
              <th>Group</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="users.length === 0">
              <td colspan="6" class="text-center">No users found.</td>
            </tr>
            <tr v-else v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.display_name || '-' }}</td>
              <td>
                <fluent-badge :appearance="user.user_group === 'admin' || user.user_group === 'owner' ? 'accent' : 'neutral'">
                  {{ user.user_group }}
                </fluent-badge>
              </td>
              <td>
                <span :class="['status-dot', user.is_active ? 'active' : 'inactive']"></span>
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </td>
              <td>
                <div class="action-buttons">
                  <fluent-button appearance="stealth" @click="openEdit(user)">Edit</fluent-button>
                  <fluent-button appearance="stealth" style="color: var(--qweb-danger)" @click="handleDelete(user)">Delete</fluent-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="totalCount > query.page_size!">
        <fluent-button 
          :disabled="query.page === 1" 
          @click="query.page!--; fetchUsers()"
        >Prev</fluent-button>
        <span>Page {{ query.page }}</span>
        <fluent-button 
          :disabled="(query.page! * query.page_size!) >= totalCount" 
          @click="query.page!++; fetchUsers()"
        >Next</fluent-button>
      </div>
    </fluent-card>

    <!-- Dialog -->
    <fluent-dialog :hidden="!isDialogOpen" id="user-dialog" trap-focus modal>
      <div class="dialog-content">
        <h2 slot="header">{{ dialogMode === 'create' ? 'Create User' : 'Edit User' }}</h2>
        <div class="dialog-body">
          <div class="form-field">
            <label>Username</label>
            <fluent-text-field
              :value="dialogForm.username"
              @input="dialogForm.username = ($event.target as HTMLInputElement).value"
              :disabled="dialogMode === 'edit'"
              style="width: 100%"
            ></fluent-text-field>
          </div>
          <div class="form-field">
            <label>Email</label>
            <fluent-text-field
              type="email"
              :value="dialogForm.email"
              @input="dialogForm.email = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>
          <div class="form-field">
            <label>Display Name</label>
            <fluent-text-field
              :value="dialogForm.display_name"
              @input="dialogForm.display_name = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>
          <div class="form-field">
            <label>Password {{ dialogMode === 'edit' ? '(Leave blank to keep)' : '' }}</label>
            <fluent-text-field
              type="password"
              :value="dialogForm.password"
              @input="dialogForm.password = ($event.target as HTMLInputElement).value"
              style="width: 100%"
            ></fluent-text-field>
          </div>
          <div class="form-field">
            <label>User Group</label>
            <select class="native-select" v-model="dialogForm.user_group" style="width: 100%">
              <option v-for="g in userGroups" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
        </div>
        <div class="dialog-footer" slot="footer">
          <fluent-button appearance="outline" @click="closeDialog">Cancel</fluent-button>
          <fluent-button appearance="accent" @click="handleSave">Save</fluent-button>
        </div>
      </div>
    </fluent-dialog>
  </div>
</template>

<style scoped>
.page-container {
  padding: var(--qweb-spacing-xl);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--qweb-spacing-lg);
}

.page-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--qweb-text-primary);
}

.table-card {
  padding: var(--qweb-spacing-lg);
  border-radius: var(--qweb-radius-lg);
  background: var(--qweb-surface);
  box-shadow: var(--qweb-shadow-sm);
}

.toolbar {
  margin-bottom: var(--qweb-spacing-lg);
  display: flex;
  gap: var(--qweb-spacing-md);
}

.search-icon {
  cursor: pointer;
  padding: 0 8px;
  line-height: 32px;
}

.table-responsive {
  overflow-x: auto;
}

.qweb-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.qweb-table th,
.qweb-table td {
  text-align: left;
  padding: var(--qweb-spacing-md);
  border-bottom: 1px solid var(--qweb-border);
}

.qweb-table th {
  font-weight: 600;
  color: var(--qweb-text-secondary);
  background: var(--qweb-surface-alt, #fafafa);
}

.text-center {
  text-align: center !important;
  color: var(--qweb-text-secondary);
  padding: var(--qweb-spacing-xl) !important;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}
.status-dot.active {
  background: #107c10;
}
.status-dot.inactive {
  background: var(--qweb-danger, #d32f2f);
}

.action-buttons {
  display: flex;
  gap: var(--qweb-spacing-sm);
}

.pagination {
  margin-top: var(--qweb-spacing-lg);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--qweb-spacing-md);
}

.dialog-content {
  padding: var(--qweb-spacing-lg) var(--qweb-spacing-xl);
  min-width: 400px;
}

.dialog-content h2 {
  margin-top: 0;
  margin-bottom: var(--qweb-spacing-md);
}

.dialog-body {
  display: flex;
  flex-direction: column;
  gap: var(--qweb-spacing-md);
  margin-bottom: var(--qweb-spacing-xl);
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

.native-select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid var(--qweb-border);
  background: var(--qweb-surface);
  font-size: 0.875rem;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--qweb-spacing-md);
}
</style>
