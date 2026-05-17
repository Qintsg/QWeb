<!--
  服务链接管理页面视图。

  :project: QWeb
  :file: ServiceLinksPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import {
  createServiceLink,
  deleteServiceLink,
  getAdminServiceLinks,
  updateServiceLink,
  type ServiceLinkAdmin,
  type ServiceLinkCreatePayload,
} from "@/api/homepage"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()

const links = ref<ServiceLinkAdmin[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editingLink = ref<ServiceLinkAdmin | null>(null)
const deleteConfirmId = ref<string | null>(null)

const categoryOptions: Array<{ value: ServiceLinkCreatePayload["category"]; label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" }> = [
  { value: "project", label: "项目展示", icon: "school", tone: "primary" },
  { value: "server", label: "服务器管理", icon: "dns", tone: "warning" },
  { value: "tool", label: "工具", icon: "construction", tone: "success" },
  { value: "other", label: "其他", icon: "hub", tone: "neutral" },
]

const form = ref<ServiceLinkCreatePayload>({
  title: "",
  url: "",
  description: "",
  remark: "",
  icon: "",
  color: "",
  category: "other",
  sort_order: 0,
  is_visible: true,
})

function resetForm(): void {
  form.value = {
    title: "",
    url: "",
    description: "",
    remark: "",
    icon: "",
    color: "",
    category: "other",
    sort_order: 0,
    is_visible: true,
  }
}

async function fetchLinks(): Promise<void> {
  loading.value = true
  try {
    const response = await getAdminServiceLinks()
    links.value = response.data.data ?? []
  } catch (err) {
    console.error("Fetch service links failed", err)
  } finally {
    loading.value = false
  }
}

function openCreateDialog(): void {
  editingLink.value = null
  resetForm()
  showDialog.value = true
}

function openEditDialog(link: ServiceLinkAdmin): void {
  editingLink.value = link
  form.value = {
    title: link.title,
    url: link.url,
    description: link.description,
    remark: link.remark,
    icon: link.icon,
    color: link.color,
    category: link.category,
    sort_order: link.sort_order,
    is_visible: link.is_visible,
  }
  showDialog.value = true
}

function closeDialog(): void {
  showDialog.value = false
}

async function handleSave(): Promise<void> {
  try {
    if (editingLink.value) await updateServiceLink(editingLink.value.id, form.value)
    else await createServiceLink(form.value)
    showDialog.value = false
    await fetchLinks()
  } catch (err) {
    console.error("Save service link failed", err)
  }
}

async function handleDelete(id: string): Promise<void> {
  try {
    await deleteServiceLink(id)
    deleteConfirmId.value = null
    await fetchLinks()
  } catch (err) {
    console.error("Delete service link failed", err)
  }
}

async function handleToggleVisibility(link: ServiceLinkAdmin): Promise<void> {
  try {
    await updateServiceLink(link.id, { is_visible: !link.is_visible })
    await fetchLinks()
  } catch (err) {
    console.error("Toggle service link visibility failed", err)
  }
}

function getCategoryOption(category: string): { value: ServiceLinkCreatePayload["category"]; label: string; icon: string; tone: "primary" | "success" | "warning" | "neutral" } {
  return categoryOptions.find((option) => option.value === category) ?? categoryOptions[3]
}

function handleCategoryChange(event: Event): void {
  form.value.category = (event.target as HTMLSelectElement).value as ServiceLinkCreatePayload["category"]
}

function handleSortOrderInput(event: Event): void {
  form.value.sort_order = Number((event.target as HTMLInputElement).value || 0)
}

function handleVisibilityChange(): void {
  form.value.is_visible = !form.value.is_visible
}

onMounted(fetchLinks)
</script>

<template>
  <div class="data-page">
    <PageHeader
      :title="t('serviceLinks.title')"
      :description="t('serviceLinks.subtitle')"
      eyebrow="Homepage"
    >
      <template #actions>
        <StatusPill :label="`${links.length} links`" tone="primary" icon="hub" />
        <md-filled-button type="button" @click="openCreateDialog">
          <span slot="icon" class="material-symbols-rounded" aria-hidden="true">add_link</span>
          {{ t('common.create') }}
        </md-filled-button>
      </template>
    </PageHeader>

    <section class="data-surface" aria-labelledby="links-table-title">
      <div class="data-toolbar">
        <h2 id="links-table-title">服务入口</h2>
        <p>首页公开入口会读取这里标记为可见的记录。</p>
      </div>

      <div v-if="loading" class="state-panel" role="status" aria-live="polite">
        <md-circular-progress indeterminate aria-label="正在加载服务链接"></md-circular-progress>
        <span>{{ t('common.loading') }}</span>
      </div>

      <div v-else-if="links.length === 0" class="state-panel">
        <span class="material-symbols-rounded" aria-hidden="true">inventory_2</span>
        <p>{{ t('common.noData') }}</p>
      </div>

      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">{{ t('serviceLinks.titleField') }}</th>
              <th scope="col">{{ t('serviceLinks.url') }}</th>
              <th scope="col">{{ t('serviceLinks.category') }}</th>
              <th scope="col">{{ t('serviceLinks.sortOrder') }}</th>
              <th scope="col">{{ t('serviceLinks.visible') }}</th>
              <th scope="col">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="link in links" :key="link.id">
              <td>
                <span class="link-title-cell">
                  <span class="material-symbols-rounded" aria-hidden="true">{{ getCategoryOption(link.category).icon }}</span>
                  <span>{{ link.title }}</span>
                </span>
              </td>
              <td>
                <a :href="link.url" target="_blank" rel="noopener noreferrer" class="link-url">{{ link.url }}</a>
              </td>
              <td>
                <StatusPill
                  :label="getCategoryOption(link.category).label"
                  :tone="getCategoryOption(link.category).tone"
                  :icon="getCategoryOption(link.category).icon"
                />
              </td>
              <td>{{ link.sort_order }}</td>
              <td>
                <md-outlined-button type="button" @click="handleToggleVisibility(link)">
                  {{ link.is_visible ? t('common.enable') : t('common.disable') }}
                </md-outlined-button>
              </td>
              <td>
                <div class="row-actions">
                  <md-text-button type="button" @click="openEditDialog(link)">{{ t('common.edit') }}</md-text-button>
                  <md-text-button v-if="deleteConfirmId !== link.id" type="button" @click="deleteConfirmId = link.id">
                    {{ t('common.delete') }}
                  </md-text-button>
                  <md-filled-button v-else type="button" @click="handleDelete(link.id)">
                    {{ t('common.confirm') }}?
                  </md-filled-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <md-dialog :open="showDialog" @closed="closeDialog">
      <div slot="headline">{{ editingLink ? t('serviceLinks.editLink') : t('serviceLinks.createLink') }}</div>
      <form slot="content" class="dialog-form" method="dialog" @submit.prevent="handleSave">
        <md-outlined-text-field :value="form.title" :label="`${t('serviceLinks.titleField')} *`" required @input="form.title = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="form.url" :label="`${t('serviceLinks.url')} *`" required @input="form.url = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="form.description" :label="t('serviceLinks.description')" @input="form.description = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="form.remark" :label="t('serviceLinks.remark')" @input="form.remark = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="form.icon" :label="t('serviceLinks.icon')" @input="form.icon = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-text-field :value="form.color" :label="t('serviceLinks.color')" @input="form.color = ($event.target as HTMLInputElement).value"></md-outlined-text-field>
        <md-outlined-select :value="form.category" :label="t('serviceLinks.category')" @change="handleCategoryChange">
          <md-select-option v-for="option in categoryOptions" :key="option.value" :value="option.value">{{ option.label }}</md-select-option>
        </md-outlined-select>
        <md-outlined-text-field :value="String(form.sort_order)" type="number" :label="t('serviceLinks.sortOrder')" @input="handleSortOrderInput"></md-outlined-text-field>
        <label class="checkbox-label">
          <md-checkbox :checked="form.is_visible" @change="handleVisibilityChange"></md-checkbox>
          <span>{{ t('serviceLinks.visible') }}</span>
        </label>
      </form>
      <div slot="actions">
        <md-text-button type="button" @click="showDialog = false">{{ t('common.cancel') }}</md-text-button>
        <md-filled-button type="button" @click="handleSave">{{ t('common.save') }}</md-filled-button>
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
  align-items: end;
  justify-content: space-between;
  gap: var(--space-md);
}

.data-toolbar h2 {
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
}

.data-toolbar p,
td,
.state-panel,
.checkbox-label {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.state-panel {
  min-block-size: 14rem;
  display: grid;
  place-items: center;
  align-content: center;
  gap: var(--space-md);
  border: 0.0625rem dashed var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
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

.link-title-cell,
.row-actions,
.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.link-title-cell {
  color: var(--md-sys-color-on-surface);
  font-weight: var(--md-sys-typescale-label-large-weight);
}

.link-url {
  color: var(--md-sys-color-primary);
  word-break: break-all;
}

.dialog-form {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  inline-size: min(100%, 40rem);
}

.dialog-form md-outlined-text-field,
.dialog-form md-outlined-select,
.checkbox-label {
  inline-size: 100%;
}

.dialog-form md-outlined-text-field:nth-child(-n + 4),
.checkbox-label {
  grid-column: 1 / -1;
}

@media (max-width: 760px) {
  .data-toolbar {
    align-items: start;
    flex-direction: column;
  }

  .dialog-form {
    grid-template-columns: 1fr;
  }
}
</style>
