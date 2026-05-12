<!--
  实现 RolesPage 页面视图。

  :project: QWeb
  :file: RolesPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getRoles, createRole, updateRole, deleteRole, type RoleListQuery } from '@/api/iam'
import type { Role } from '@/types/auth'

const { t } = useI18n()

const loading = ref(false)
const roles = ref<Role[]>([])
const query = ref<RoleListQuery>({
  search: '',
})

const isDialogOpen = ref(false)
const dialogMode = ref<'create'|'edit'>('create')
const editId = ref('')
const dialogForm = ref({
  name: '',
  display_name: '',
  description: '',
})

async function fetchRoles() {
  loading.value = true
  try {
    const res = await getRoles(query.value)
    roles.value = res.data.data || []
  } catch (err) {
    console.error('Failed to fetch roles', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchRoles())

function handleSearch() {
  fetchRoles()
}

function openCreate() {
  dialogMode.value = 'create'
  dialogForm.value = { name: '', display_name: '', description: '' }
  isDialogOpen.value = true
}

function openEdit(role: Role) {
  dialogMode.value = 'edit'
  editId.value = role.id
  dialogForm.value = {
    name: role.name,
    display_name: role.display_name,
    description: role.description || '',
  }
  isDialogOpen.value = true
}

function closeDialog() {
  isDialogOpen.value = false
}

async function handleSave() {
  try {
    if (dialogMode.value === 'create') {
      await createRole(dialogForm.value)
    } else {
      await updateRole(editId.value, dialogForm.value)
    }
    isDialogOpen.value = false
    fetchRoles()
  } catch (err) {
    console.error('Save failed', err)
    alert('Save failed')
  }
}

async function handleDelete(role: Role) {
  if (confirm(`Delete role ${role.display_name}?`)) {
    try {
      await deleteRole(role.id)
      fetchRoles()
    } catch (err) {
      console.error('Delete failed', err)
    }
  }
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.roles', 'Role Management') }}</h1>
      <fluent-button appearance="accent" @click="openCreate">Add Role</fluent-button>
    </div>

    <fluent-card class="table-card">
      <div class="toolbar">
        <fluent-text-field
          :value="query.search"
          @input="query.search = ($event.target as HTMLInputElement).value"
          @keyup.enter="handleSearch"
          placeholder="Search by name..."
        >
          <span slot="end" class="search-icon" @click="handleSearch">🔍</span>
        </fluent-text-field>
      </div>

      <div class="table-responsive">
        <table class="qweb-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Display Name</th>
              <th>Description</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="roles.length === 0">
              <td colspan="5" class="text-center">No roles found.</td>
            </tr>
            <tr v-else v-for="role in roles" :key="role.id">
              <td><fluent-badge>{{ role.name }}</fluent-badge></td>
              <td>{{ role.display_name }}</td>
              <td>{{ role.description || '-' }}</td>
              <td>{{ new Date(role.created_at || '').toLocaleDateString() }}</td>
              <td>
                <div class="action-buttons">
                  <fluent-button appearance="stealth" @click="openEdit(role)">Edit</fluent-button>
                  <fluent-button appearance="stealth" style="color: var(--q-color-error)" @click="handleDelete(role)">Delete</fluent-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </fluent-card>

    <fluent-dialog :hidden="!isDialogOpen" id="role-dialog" trap-focus modal>
      <div class="dialog-content">
        <h2 slot="header">{{ dialogMode === 'create' ? 'Create Role' : 'Edit Role' }}</h2>
        <div class="dialog-body">
          <div class="form-field">
            <label>System Name</label>
            <fluent-text-field
              :value="dialogForm.name"
              @input="dialogForm.name = ($event.target as HTMLInputElement).value"
              :disabled="dialogMode === 'edit'"
              placeholder="e.g. system:admin"
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
            <label>Description</label>
            <fluent-text-area
              :value="dialogForm.description"
              @input="dialogForm.description = ($event.target as HTMLInputElement).value"
              style="width: 100%"
              rows="3"
            ></fluent-text-area>
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
.page-container { padding: var(--q-space-32); }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--q-space-24); }
.page-title { margin: 0; font-size: 1.5rem; font-weight: 600; color: var(--q-color-text-primary); }
.table-card { padding: var(--q-space-24); border-radius: var(--q-radius-lg); background: var(--q-color-surface); box-shadow: var(--q-shadow-sm); }
.toolbar { margin-bottom: var(--q-space-24); display: flex; gap: var(--q-space-16); }
.search-icon { cursor: pointer; padding: 0 8px; line-height: 32px; }
.table-responsive { overflow-x: auto; }
.qweb-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.qweb-table th, .qweb-table td { text-align: left; padding: var(--q-space-16); border-bottom: 1px solid var(--q-color-stroke); }
.qweb-table th { font-weight: 600; color: var(--q-color-text-secondary); background: var(--q-color-surface-alt, #fafafa); }
.text-center { text-align: center !important; color: var(--q-color-text-secondary); padding: var(--q-space-32) !important; }
.action-buttons { display: flex; gap: var(--q-space-12); }
.dialog-content { padding: var(--q-space-24) var(--q-space-32); min-width: 400px; }
.dialog-content h2 { margin-top: 0; margin-bottom: var(--q-space-16); }
.dialog-body { display: flex; flex-direction: column; gap: var(--q-space-16); margin-bottom: var(--q-space-32); }
.form-field { display: flex; flex-direction: column; gap: var(--q-space-8); }
.form-field label { font-size: 0.875rem; font-weight: 500; color: var(--q-color-text-secondary); }
.dialog-footer { display: flex; justify-content: flex-end; gap: var(--q-space-16); }
</style>
