<!--
  登录审计日志页面视图。

  :project: QWeb
  :file: LoginLogsPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { getLoginLogs, type LoginLog, type LoginLogQuery } from "@/api/audit"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const loading = ref(false)
const logs = ref<LoginLog[]>([])
const totalCount = ref(0)
const query = ref<LoginLogQuery>({ page: 1, page_size: 20, search: "" })

async function fetchLogs(): Promise<void> {
  loading.value = true
  try {
    const res = await getLoginLogs(query.value)
    const data = res.data.data
    logs.value = data.results || []
    totalCount.value = data.count || 0
  } catch (err) {
    console.error("Failed to fetch login logs", err)
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

function actionTone(action: string): "success" | "error" | "neutral" {
  if (action === "login_success") return "success"
  if (action === "login_failed") return "error"
  return "neutral"
}

onMounted(() => fetchLogs())
</script>

<template>
  <div class="data-page">
    <PageHeader
      title="Login Audit Logs"
      description="追踪登录成功、失败、来源 IP 与客户端指纹。"
      eyebrow="Audit"
    >
      <template #actions>
        <StatusPill :label="`${totalCount} login records`" tone="primary" icon="shield_lock" />
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="login-table-title">
      <div class="data-toolbar">
        <h2 id="login-table-title">登录日志</h2>
        <md-outlined-text-field
          :value="query.search"
          label="Search user or action"
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
              <th scope="col">IP Address</th>
              <th scope="col">Location</th>
              <th scope="col">User Agent</th>
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
              <td><StatusPill :label="log.action" :tone="actionTone(log.action)" icon="login" /></td>
              <td>{{ log.ip_address || '-' }}</td>
              <td>{{ log.location || '-' }}</td>
              <td class="ua-col" :title="log.user_agent">{{ log.user_agent }}</td>
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

.ua-col {
  max-inline-size: 20rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
