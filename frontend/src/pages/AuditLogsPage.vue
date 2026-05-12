<!--
  实现 AuditLogsPage 页面视图。

  :project: QWeb
  :file: AuditLogsPage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getAuditLogs, type AuditLogQuery, type AuditLog } from '@/api/audit'

const { t } = useI18n()

const loading = ref(false)
const logs = ref<AuditLog[]>([])
const totalCount = ref(0)
const query = ref<AuditLogQuery>({
  page: 1,
  page_size: 20,
  search: '',
})

async function fetchLogs() {
  loading.value = true
  try {
    const res = await getAuditLogs(query.value)
    const data = res.data.data
    logs.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error('Failed to fetch logs', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchLogs())

function handleSearch() {
  query.value.page = 1
  fetchLogs()
}

function parseDate(d: string) {
  return new Date(d).toLocaleString()
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">Operation Audit Logs</h1>
    </div>

    <fluent-card class="table-card">
      <div class="toolbar">
        <fluent-text-field
          :value="query.search"
          @input="query.search = ($event.target as HTMLInputElement).value"
          @keyup.enter="handleSearch"
          placeholder="Search by action, module, description..."
          style="width: 300px"
        >
          <span slot="end" class="search-icon" @click="handleSearch">🔍</span>
        </fluent-text-field>
      </div>

      <div class="table-responsive">
        <table class="qweb-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>User</th>
              <th>Action</th>
              <th>Module</th>
              <th>Description</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="logs.length === 0">
              <td colspan="6" class="text-center">No logs found.</td>
            </tr>
            <tr v-else v-for="log in logs" :key="log.id">
              <td>{{ parseDate(log.created_at) }}</td>
              <td>{{ log.username || 'System' }}</td>
              <td><fluent-badge>{{ log.action }}</fluent-badge></td>
              <td>{{ log.module }}</td>
              <td>{{ log.description }}</td>
              <td>{{ log.ip_address || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="totalCount > query.page_size!">
        <fluent-button 
          :disabled="query.page === 1" 
          @click="query.page!--; fetchLogs()"
        >Prev</fluent-button>
        <span>Page {{ query.page }} (Total: {{ totalCount }})</span>
        <fluent-button 
          :disabled="(query.page! * query.page_size!) >= totalCount" 
          @click="query.page!++; fetchLogs()"
        >Next</fluent-button>
      </div>
    </fluent-card>
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
.pagination { margin-top: var(--q-space-24); display: flex; justify-content: center; align-items: center; gap: var(--q-space-16); }
</style>
