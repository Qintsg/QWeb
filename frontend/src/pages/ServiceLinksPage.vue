<script setup lang="ts">
/**
 * 服务链接管理页面
 * 管理后台中对首页服务链接的增删改查
 */
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  getAdminServiceLinks,
  createServiceLink,
  updateServiceLink,
  deleteServiceLink,
  type ServiceLinkAdmin,
  type ServiceLinkCreatePayload,
} from '@/api/homepage'

const { t } = useI18n()

const links = ref<ServiceLinkAdmin[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editingLink = ref<ServiceLinkAdmin | null>(null)
const deleteConfirmId = ref<string | null>(null)

const categoryOptions = [
  { value: 'project', label: '项目展示' },
  { value: 'server', label: '服务器管理' },
  { value: 'tool', label: '工具' },
  { value: 'other', label: '其他' },
]

const form = ref<ServiceLinkCreatePayload>({
  title: '',
  url: '',
  description: '',
  remark: '',
  icon: '',
  color: '',
  category: 'other',
  sort_order: 0,
  is_visible: true,
})

function resetForm() {
  form.value = {
    title: '',
    url: '',
    description: '',
    remark: '',
    icon: '',
    color: '',
    category: 'other',
    sort_order: 0,
    is_visible: true,
  }
}

async function fetchLinks() {
  loading.value = true
  try {
    const response = await getAdminServiceLinks()
    links.value = response.data ?? []
  } catch {
    // 错误处理：静默
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingLink.value = null
  resetForm()
  showDialog.value = true
}

function openEditDialog(link: ServiceLinkAdmin) {
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

async function handleSave() {
  try {
    if (editingLink.value) {
      await updateServiceLink(editingLink.value.id, form.value)
    } else {
      await createServiceLink(form.value)
    }
    showDialog.value = false
    await fetchLinks()
  } catch {
    // 错误处理：静默
  }
}

async function handleDelete(id: string) {
  try {
    await deleteServiceLink(id)
    deleteConfirmId.value = null
    await fetchLinks()
  } catch {
    // 错误处理：静默
  }
}

async function handleToggleVisibility(link: ServiceLinkAdmin) {
  try {
    await updateServiceLink(link.id, { is_visible: !link.is_visible })
    await fetchLinks()
  } catch {
    // 错误处理：静默
  }
}

function getCategoryLabel(category: string): string {
  return categoryOptions.find((o) => o.value === category)?.label || '其他'
}

onMounted(fetchLinks)
</script>

<template>
  <div class="page-container">
    <section class="page-header">
      <div>
        <h1 class="page-title">{{ t('serviceLinks.title') }}</h1>
        <p class="page-subtitle">{{ t('serviceLinks.subtitle') }}</p>
      </div>
      <fluent-button appearance="accent" @click="openCreateDialog">
        {{ t('common.create') }}
      </fluent-button>
    </section>

    <!-- 列表 -->
    <div v-if="loading" class="page-loading">
      <span>{{ t('common.loading') }}</span>
    </div>

    <div v-else-if="links.length === 0" class="page-empty">
      <p>{{ t('common.noData') }}</p>
    </div>

    <div v-else class="links-table-wrap">
      <table class="links-table">
        <thead>
          <tr>
            <th>{{ t('serviceLinks.titleField') }}</th>
            <th>{{ t('serviceLinks.url') }}</th>
            <th>{{ t('serviceLinks.category') }}</th>
            <th>{{ t('serviceLinks.sortOrder') }}</th>
            <th>{{ t('serviceLinks.visible') }}</th>
            <th>{{ t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="link in links" :key="link.id">
            <td>
              <div class="link-title-cell">
                <span v-if="link.icon" class="link-icon">{{ link.icon }}</span>
                <span>{{ link.title }}</span>
              </div>
            </td>
            <td>
              <a :href="link.url" target="_blank" rel="noopener noreferrer" class="link-url">
                {{ link.url }}
              </a>
            </td>
            <td>
              <span
                class="category-badge"
                :style="{ background: link.color ? `${link.color}18` : '#0e9aa718', color: link.color || '#0e9aa7' }"
              >
                {{ getCategoryLabel(link.category) }}
              </span>
            </td>
            <td>{{ link.sort_order }}</td>
            <td>
              <fluent-button size="small" :appearance="link.is_visible ? 'accent' : 'outline'" @click="handleToggleVisibility(link)">
                {{ link.is_visible ? t('common.enable') : t('common.disable') }}
              </fluent-button>
            </td>
            <td>
              <div class="action-buttons">
                <fluent-button size="small" appearance="outline" @click="openEditDialog(link)">
                  {{ t('common.edit') }}
                </fluent-button>
                <fluent-button
                  v-if="deleteConfirmId !== link.id"
                  size="small"
                  appearance="outline"
                  @click="deleteConfirmId = link.id"
                >
                  {{ t('common.delete') }}
                </fluent-button>
                <fluent-button
                  v-else
                  size="small"
                  appearance="accent"
                  @click="handleDelete(link.id)"
                >
                  {{ t('common.confirm') }}?
                </fluent-button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 创建/编辑弹窗 -->
    <fluent-dialog :hidden="!showDialog" trap-focus modal @close="showDialog = false">
      <div class="dialog-content">
        <h2 class="dialog-title">
          {{ editingLink ? t('serviceLinks.editLink') : t('serviceLinks.createLink') }}
        </h2>

        <div class="form-grid">
          <div class="form-field">
            <label>{{ t('serviceLinks.titleField') }} *</label>
            <fluent-text-field v-model="form.title" :placeholder="t('serviceLinks.titlePlaceholder')" />
          </div>

          <div class="form-field">
            <label>{{ t('serviceLinks.url') }} *</label>
            <fluent-text-field v-model="form.url" placeholder="https://..." />
          </div>

          <div class="form-field">
            <label>{{ t('serviceLinks.description') }}</label>
            <fluent-text-field v-model="form.description" :placeholder="t('serviceLinks.descPlaceholder')" />
          </div>

          <div class="form-field">
            <label>{{ t('serviceLinks.remark') }}</label>
            <fluent-text-field v-model="form.remark" :placeholder="t('serviceLinks.remarkPlaceholder')" />
          </div>

          <div class="form-field form-field--half">
            <label>{{ t('serviceLinks.icon') }}</label>
            <fluent-text-field v-model="form.icon" placeholder="🎓" />
          </div>

          <div class="form-field form-field--half">
            <label>{{ t('serviceLinks.color') }}</label>
            <fluent-text-field v-model="form.color" placeholder="#0e9aa7" />
          </div>

          <div class="form-field form-field--half">
            <label>{{ t('serviceLinks.category') }}</label>
            <fluent-select v-model="form.category">
              <fluent-option v-for="opt in categoryOptions" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </fluent-option>
            </fluent-select>
          </div>

          <div class="form-field form-field--half">
            <label>{{ t('serviceLinks.sortOrder') }}</label>
            <fluent-number-field v-model="form.sort_order" min="0" />
          </div>

          <div class="form-field">
            <label class="checkbox-label">
              <fluent-checkbox :checked="form.is_visible" @change="form.is_visible = !form.is_visible" />
              {{ t('serviceLinks.visible') }}
            </label>
          </div>
        </div>

        <div class="dialog-actions">
          <fluent-button appearance="outline" @click="showDialog = false">
            {{ t('common.cancel') }}
          </fluent-button>
          <fluent-button appearance="accent" @click="handleSave">
            {{ t('common.save') }}
          </fluent-button>
        </div>
      </div>
    </fluent-dialog>
  </div>
</template>

<style scoped>
.page-container {
  padding: var(--q-space-32);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--q-space-24);
}

.page-title {
  margin: 0 0 var(--q-space-4);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--q-color-text-primary);
}

.page-subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: var(--q-color-text-secondary);
}

.page-loading,
.page-empty {
  text-align: center;
  padding: var(--q-space-40);
  color: var(--q-color-text-secondary);
}

.links-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-md);
  background: var(--q-color-surface);
}

.links-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.links-table th,
.links-table td {
  padding: var(--q-space-12) var(--q-space-16);
  text-align: left;
  border-bottom: 1px solid var(--q-color-stroke);
}

.links-table th {
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--q-color-text-secondary);
  background: var(--q-color-canvas);
}

.links-table tr:last-child td {
  border-bottom: none;
}

.link-title-cell {
  display: flex;
  align-items: center;
  gap: var(--q-space-8);
  font-weight: 500;
}

.link-icon {
  font-size: 1.25rem;
}

.link-url {
  color: var(--q-color-brand);
  text-decoration: none;
  font-size: 0.8125rem;
  word-break: break-all;
}

.link-url:hover {
  text-decoration: underline;
}

.category-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--q-radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: var(--q-space-8);
}

/* Dialog */
.dialog-content {
  padding: var(--q-space-24);
  min-width: 480px;
}

.dialog-title {
  margin: 0 0 var(--q-space-24);
  font-size: 1.25rem;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--q-space-16);
}

.form-field {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: var(--q-space-4);
}

.form-field--half {
  grid-column: auto;
}

.form-field label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--q-color-text-secondary);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--q-space-8);
  cursor: pointer;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--q-space-12);
  margin-top: var(--q-space-24);
  padding-top: var(--q-space-16);
  border-top: 1px solid var(--q-color-stroke);
}
</style>
