<!--
  操作审计日志页面视图。

  :project: QWeb
  :file: AuditLogsPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { getAuditLogs, type AuditLog, type AuditLogQuery } from "@/api/audit"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const loading = ref(false)
const logs = ref<AuditLog[]>([])
const totalCount = ref(0)
const query = ref<AuditLogQuery>({ page: 1, page_size: 20, search: "" })

async function fetchLogs(): Promise<void> {
  loading.value = true
  try {
    const res = await getAuditLogs(query.value)
    const data = res.data.data
    logs.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error("Failed to fetch logs", err)
  } finally {
    loading.value = false
  }
}

function handleSearch(): void {
  query.value.page = 1
  fetchLogs()
}

function parseDate(dateValue: string): string {
  return new Date(dateValue).toLocaleString()
}

onMounted(() => fetchLogs())
</script>

<template>
  <div class="data-page">
    <PageHeader
      title="Operation Audit Logs"
      description="查看高风险动作和管理操作的审计轨迹。"
      eyebrow="Audit"
    >
      <template #actions>
        <StatusPill :label="`${totalCount} records`" tone="warning" icon="history" />
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="audit-table-title">
      <div class="data-toolbar">
        <h2 id="audit-table-title">操作日志</h2>
        <md-outlined-text-field
          :value="query.search"
          label="Search action, module, description"
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
              <th scope="col">Time</th>
              <th scope="col">User</th>
              <th scope="col">Action</th>
              <th scope="col">Module</th>
              <th scope="col">Description</th>
              <th scope="col">IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="table-state">Loading...</td>
            </tr>
            <tr v-else-if="logs.length === 0">
              <td colspan="6" class="table-state">No logs found.</td>
            </tr>
            <tr v-for="log in logs" v-else :key="log.id">
              <td>{{ parseDate(log.created_at) }}</td>
              <td>{{ log.username || 'System' }}</td>
              <td><StatusPill :label="log.action" tone="primary" icon="bolt" /></td>
              <td>{{ log.module }}</td>
              <td>{{ log.description }}</td>
              <td>{{ log.ip_address || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="totalCount > query.page_size!" class="pagination">
        <md-outlined-button type="button" :disabled="query.page === 1" @click="query.page!--; fetchLogs()">Prev</md-outlined-button>
        <span>Page {{ query.page }} (Total: {{ totalCount }})</span>
        <md-outlined-button type="button" :disabled="(query.page! * query.page_size!) >= totalCount" @click="query.page!++; fetchLogs()">Next</md-outlined-button>
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

.data-toolbar,
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.data-toolbar {
  justify-content: space-between;
}

.data-toolbar h2 {
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.data-toolbar md-outlined-text-field {
  inline-size: min(100%, 24rem);
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

.pagination {
  justify-content: center;
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
