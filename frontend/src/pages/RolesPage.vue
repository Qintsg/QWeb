<!--
  角色管理页面视图。

  :project: QWeb
  :file: RolesPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { createRole, deleteRole, getRoles, updateRole, type RoleListQuery } from "@/api/iam"
import type { Role } from "@/types/auth"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()

const loading = ref(false)
const roles = ref<Role[]>([])
const query = ref<RoleListQuery>({ search: "" })
const isDialogOpen = ref(false)
const dialogMode = ref<"create" | "edit">("create")
const editId = ref("")
const dialogForm = ref({ name: "", display_name: "", description: "" })

async function fetchRoles(): Promise<void> {
  loading.value = true
  try {
    const res = await getRoles(query.value)
    roles.value = res.data.data || []
  } catch (err) {
    console.error("Failed to fetch roles", err)
  } finally {
    loading.value = false
  }
}

function handleSearch(): void {
  fetchRoles()
}

function openCreate(): void {
  dialogMode.value = "create"
  dialogForm.value = { name: "", display_name: "", description: "" }
  isDialogOpen.value = true
}

function openEdit(role: Role): void {
  dialogMode.value = "edit"
  editId.value = role.id
  dialogForm.value = {
    name: role.name,
    display_name: role.display_name,
    description: role.description || "",
  }
  isDialogOpen.value = true
}

function closeDialog(): void {
  isDialogOpen.value = false
}

async function handleSave(): Promise<void> {
  try {
    if (dialogMode.value === "create") await createRole(dialogForm.value)
    else await updateRole(editId.value, dialogForm.value)
    isDialogOpen.value = false
    fetchRoles()
  } catch (err) {
    console.error("Save failed", err)
    window.alert("Save failed")
  }
}

async function handleDelete(role: Role): Promise<void> {
  if (window.confirm(`Delete role ${role.display_name}?`)) {
    try {
      await deleteRole(role.id)
      fetchRoles()
    } catch (err) {
      console.error("Delete failed", err)
    }
  }
}

onMounted(() => fetchRoles())
</script>

<template>
  <div class="data-page">
    <PageHeader
      :title="t('nav.roles', 'Role Management')"
      description="维护 IAM 角色模板；最终权限仍由角色权限与用户覆盖共同决定。"
      eyebrow="IAM"
    >
      <template #actions>
        <md-filled-button type="button" @click="openCreate">
          <span slot="icon" class="material-symbols-rounded" aria-hidden="true">add</span>
          Add Role
        </md-filled-button>
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="roles-table-title">
      <div class="data-toolbar">
        <h2 id="roles-table-title">角色列表</h2>
        <md-outlined-text-field
          :value="query.search"
          label="Search by name"
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
              <th scope="col">Name</th>
              <th scope="col">Display Name</th>
              <th scope="col">Description</th>
              <th scope="col">Created At</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="table-state">Loading...</td>
            </tr>
            <tr v-else-if="roles.length === 0">
              <td colspan="5" class="table-state">No roles found.</td>
            </tr>
            <tr v-for="role in roles" v-else :key="role.id">
              <td><StatusPill :label="role.name" :tone="role.is_system ? 'primary' : 'neutral'" icon="admin_panel_settings" /></td>
              <td>{{ role.display_name }}</td>
              <td>{{ role.description || '-' }}</td>
              <td>{{ role.created_at ? new Date(role.created_at).toLocaleDateString() : '-' }}</td>
              <td>
                <div class="row-actions">
                  <md-text-button type="button" @click="openEdit(role)">Edit</md-text-button>
                  <md-text-button type="button" @click="handleDelete(role)">Delete</md-text-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <md-dialog :open="isDialogOpen" @closed="closeDialog">
      <div slot="headline">{{ dialogMode === 'create' ? 'Create Role' : 'Edit Role' }}</div>
      <form slot="content" class="dialog-form" method="dialog" @submit.prevent="handleSave">
        <md-outlined-text-field :value="dialogForm.name" label="System Name" :disabled="dialogMode === 'edit'" @input="dialogForm.name = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="dialogForm.display_name" label="Display Name" @input="dialogForm.display_name = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="dialogForm.description" label="Description" type="textarea" rows="3" @input="dialogForm.description = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
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
}

th {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
}

td,
.row-actions {
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

.row-actions {
  display: flex;
  gap: var(--space-sm);
}

.dialog-form md-outlined-text-field {
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
