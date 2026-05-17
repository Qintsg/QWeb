<!--
  权限注册表页面视图。

  :project: QWeb
  :file: PermissionsPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { getPermissions, type PermissionListQuery } from "@/api/iam"
import type { Permission } from "@/types/auth"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()

const loading = ref(false)
const permissions = ref<Permission[]>([])
const query = ref<PermissionListQuery>({ search: "" })

async function fetchPermissions(): Promise<void> {
  loading.value = true
  try {
    const res = await getPermissions(query.value)
    permissions.value = res.data.data || []
  } catch (err) {
    console.error("Failed to fetch permissions", err)
  } finally {
    loading.value = false
  }
}

function handleSearch(): void {
  fetchPermissions()
}

onMounted(() => fetchPermissions())
</script>

<template>
  <div class="data-page">
    <PageHeader
      title="Permissions Registry"
      description="权限码使用 module.resource.action 结构，是后端安全校验和前端体验过滤的共同语言。"
      eyebrow="IAM"
    >
      <template #actions>
        <StatusPill :label="`${permissions.length} permissions`" tone="primary" icon="vpn_key" />
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="permissions-table-title">
      <div class="data-toolbar">
        <h2 id="permissions-table-title">权限列表</h2>
        <md-outlined-text-field
          :value="query.search"
          label="Search code or name"
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
              <th scope="col">Code</th>
              <th scope="col">Name</th>
              <th scope="col">Module</th>
              <th scope="col">Resource</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="table-state">Loading...</td>
            </tr>
            <tr v-else-if="permissions.length === 0">
              <td colspan="5" class="table-state">No permissions found.</td>
            </tr>
            <tr v-for="permission in permissions" v-else :key="permission.id">
              <td><code>{{ permission.code }}</code></td>
              <td>{{ permission.name }}</td>
              <td>{{ permission.module }}</td>
              <td>{{ permission.resource || '-' }}</td>
              <td>
                <StatusPill
                  :label="permission.is_active ? 'Active' : 'Inactive'"
                  :tone="permission.is_active ? 'success' : 'neutral'"
                  :icon="permission.is_active ? 'check_circle' : 'pause_circle'"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<style scoped>
.data-page,
.data-surface {
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

td {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

code {
  color: var(--md-sys-color-primary);
  font-family: var(--q-font-mono);
}

.table-state {
  padding: var(--space-xxl);
  color: var(--md-sys-color-on-surface-variant);
  text-align: center;
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
