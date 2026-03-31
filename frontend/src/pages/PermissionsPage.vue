<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getPermissions, type PermissionListQuery } from '@/api/iam'
import type { Permission } from '@/types/auth'

const { t } = useI18n()

const loading = ref(false)
const permissions = ref<Permission[]>([])
const totalCount = ref(0)
const query = ref<PermissionListQuery>({
  page: 1,
  page_size: 20,
  search: '',
})

async function fetchPermissions() {
  loading.value = true
  try {
    const res = await getPermissions(query.value)
    const data = res.data.data
    permissions.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error('Failed to fetch permissions', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPermissions())

function handleSearch() {
  query.value.page = 1
  fetchPermissions()
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">Permissions Registry</h1>
    </div>

    <fluent-card class="table-card">
      <div class="toolbar">
        <fluent-text-field
          :value="query.search"
          @input="query.search = ($event.target as HTMLInputElement).value"
          @keyup.enter="handleSearch"
          placeholder="Search code or name..."
        >
          <span slot="end" class="search-icon" @click="handleSearch">🔍</span>
        </fluent-text-field>
      </div>

      <div class="table-responsive">
        <table class="qweb-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Name</th>
              <th>Module</th>
              <th>Category</th>
              <th>Risk Level</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="permissions.length === 0">
              <td colspan="5" class="text-center">No permissions found.</td>
            </tr>
            <tr v-else v-for="p in permissions" :key="p.id">
              <td><fluent-badge>{{ p.code }}</fluent-badge></td>
              <td>{{ p.display_name }}</td>
              <td>{{ p.module }}</td>
              <td>{{ p.category }}</td>
              <td>
                <fluent-badge :appearance="p.is_risk ? 'accent' : 'neutral'" :style="p.is_risk ? 'background: var(--qweb-danger); color: white;' : ''">
                  {{ p.is_risk ? 'High' : 'Normal' }}
                </fluent-badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="totalCount > query.page_size!">
        <fluent-button 
          :disabled="query.page === 1" 
          @click="query.page!--; fetchPermissions()"
        >Prev</fluent-button>
        <span>Page {{ query.page }}</span>
        <fluent-button 
          :disabled="(query.page! * query.page_size!) >= totalCount" 
          @click="query.page!++; fetchPermissions()"
        >Next</fluent-button>
      </div>
    </fluent-card>
  </div>
</template>

<style scoped>
.page-container { padding: var(--qweb-spacing-xl); }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--qweb-spacing-lg); }
.page-title { margin: 0; font-size: 1.5rem; font-weight: 600; color: var(--qweb-text-primary); }
.table-card { padding: var(--qweb-spacing-lg); border-radius: var(--qweb-radius-lg); background: var(--qweb-surface); box-shadow: var(--qweb-shadow-sm); }
.toolbar { margin-bottom: var(--qweb-spacing-lg); display: flex; gap: var(--qweb-spacing-md); }
.search-icon { cursor: pointer; padding: 0 8px; line-height: 32px; }
.table-responsive { overflow-x: auto; }
.qweb-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.qweb-table th, .qweb-table td { text-align: left; padding: var(--qweb-spacing-md); border-bottom: 1px solid var(--qweb-border); }
.qweb-table th { font-weight: 600; color: var(--qweb-text-secondary); background: var(--qweb-surface-alt, #fafafa); }
.text-center { text-align: center !important; color: var(--qweb-text-secondary); padding: var(--qweb-spacing-xl) !important; }
.pagination { margin-top: var(--qweb-spacing-lg); display: flex; justify-content: center; align-items: center; gap: var(--qweb-spacing-md); }
</style>
