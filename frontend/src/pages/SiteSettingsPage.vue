<!--
  站点设置页面视图。

  :project: QWeb
  :file: SiteSettingsPage.vue
  :author: Qintsg
  :date: 2026-05-18 12:20
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import PageHeader from "@/components/common/PageHeader.vue"
import { useSiteStore } from "@/stores/site"
import type { SiteMetadataUpdatePayload } from "@/api/homepage"

const { t } = useI18n()
const siteStore = useSiteStore()
const savedMessage = ref("")
const errorMessage = ref("")

const form = ref<Required<SiteMetadataUpdatePayload>>({
  site_name: "",
  site_title: "",
  subtitle: "",
  logo_url: "",
  favicon_url: "",
  brand_initial: "",
})

function syncForm(): void {
  form.value = {
    site_name: siteStore.metadata.site_name,
    site_title: siteStore.metadata.site_title,
    subtitle: siteStore.metadata.subtitle,
    logo_url: siteStore.metadata.logo_url,
    favicon_url: siteStore.metadata.favicon_url,
    brand_initial: siteStore.metadata.brand_initial,
  }
}

async function handleSave(): Promise<void> {
  savedMessage.value = ""
  errorMessage.value = ""
  try {
    await siteStore.saveMetadata({ ...form.value })
    syncForm()
    savedMessage.value = t("siteSettings.saved")
  } catch (err: unknown) {
    errorMessage.value = (err as Error).message || t("siteSettings.saveFailed")
  }
}

onMounted(async () => {
  await siteStore.fetchAdminMetadata()
  syncForm()
})
</script>

<template>
  <div class="settings-page">
    <PageHeader
      :title="t('siteSettings.title')"
      :description="t('siteSettings.subtitle')"
      eyebrow="站点配置"
    />

    <section class="settings-layout" aria-labelledby="site-settings-form-title">
      <form class="settings-form" @submit.prevent="handleSave">
        <div class="settings-form__header">
          <h2 id="site-settings-form-title">{{ t('siteSettings.basicInfo') }}</h2>
          <p>{{ t('siteSettings.basicInfoHint') }}</p>
        </div>

        <div v-if="savedMessage" class="settings-alert settings-alert--success" role="status">
          <span class="material-symbols-rounded" aria-hidden="true">check_circle</span>
          <span>{{ savedMessage }}</span>
        </div>
        <div v-if="errorMessage" class="settings-alert settings-alert--error" role="alert">
          <span class="material-symbols-rounded" aria-hidden="true">error</span>
          <span>{{ errorMessage }}</span>
        </div>

        <md-outlined-text-field
          :value="form.site_name"
          :label="t('siteSettings.siteName')"
          required
          @input="form.site_name = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>
        <md-outlined-text-field
          :value="form.site_title"
          :label="t('siteSettings.siteTitle')"
          required
          @input="form.site_title = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>
        <md-outlined-text-field
          :value="form.subtitle"
          :label="t('siteSettings.siteSubtitle')"
          @input="form.subtitle = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>
        <md-outlined-text-field
          :value="form.logo_url"
          :label="t('siteSettings.logoUrl')"
          @input="form.logo_url = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>
        <md-outlined-text-field
          :value="form.favicon_url"
          :label="t('siteSettings.faviconUrl')"
          @input="form.favicon_url = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>
        <md-outlined-text-field
          :value="form.brand_initial"
          :label="t('siteSettings.brandInitial')"
          maxlength="4"
          @input="form.brand_initial = ($event.target as HTMLInputElement).value"
        ></md-outlined-text-field>

        <div class="settings-form__actions">
          <md-filled-button type="submit" :disabled="siteStore.loading" :aria-busy="siteStore.loading">
            <md-circular-progress v-if="siteStore.loading" slot="icon" indeterminate></md-circular-progress>
            {{ siteStore.loading ? t('common.loading') : t('common.save') }}
          </md-filled-button>
        </div>
      </form>

      <aside class="brand-preview" aria-labelledby="brand-preview-title">
        <p>{{ t('siteSettings.preview') }}</p>
        <div class="brand-preview__logo">
          <img v-if="form.logo_url" :src="form.logo_url" alt="" />
          <span v-else>{{ form.brand_initial || siteStore.brandInitial }}</span>
        </div>
        <h2 id="brand-preview-title">{{ form.site_name || siteStore.siteName }}</h2>
        <span>{{ form.site_title || siteStore.siteTitle }}</span>
        <small>{{ form.subtitle || siteStore.metadata.subtitle }}</small>
      </aside>
    </section>
  </div>
</template>

<style scoped>
.settings-page,
.settings-form {
  display: grid;
  gap: var(--space-lg);
}

.settings-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(18rem, 24rem);
  gap: var(--space-xl);
  align-items: start;
}

.settings-form,
.brand-preview {
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
}

.settings-form__header {
  display: grid;
  gap: var(--space-xs);
}

.settings-form__header h2,
.brand-preview h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-small-font);
  font-size: var(--md-sys-typescale-headline-small-size);
  font-weight: var(--md-sys-typescale-headline-small-weight);
  line-height: var(--md-sys-typescale-headline-small-line-height);
}

.settings-form__header p,
.brand-preview p,
.brand-preview span,
.brand-preview small {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.settings-alert {
  min-block-size: 3rem;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding-inline: var(--space-md);
  border-radius: var(--md-sys-shape-corner-medium);
  font-family: var(--md-sys-typescale-body-medium-font);
}

.settings-alert--success {
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
}

.settings-alert--error {
  color: var(--md-sys-color-on-error-container);
  background: var(--md-sys-color-error-container);
}

.settings-form__actions {
  display: flex;
  justify-content: flex-end;
}

.brand-preview {
  position: sticky;
  inset-block-start: 6rem;
  display: grid;
  gap: var(--space-sm);
}

.brand-preview__logo {
  inline-size: 5rem;
  block-size: 5rem;
  display: grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  overflow: hidden;
  font-family: var(--md-sys-typescale-headline-medium-font);
  font-size: var(--md-sys-typescale-headline-medium-size);
  font-weight: var(--md-sys-typescale-headline-medium-weight);
}

.brand-preview__logo img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}

@media (max-width: 839px) {
  .settings-layout {
    grid-template-columns: 1fr;
  }

  .brand-preview {
    position: static;
  }
}
</style>
