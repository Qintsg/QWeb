/**
 * 站点元数据状态管理。
 *
 * :project: QWeb
 * :file: site.ts
 * :author: Qintsg
 * :date: 2026-05-18 12:15
 */
import { computed, ref } from "vue"
import { defineStore } from "pinia"
import {
  getAdminSiteMetadata,
  getPublicSiteMetadata,
  updateSiteMetadata,
  type SiteMetadata,
  type SiteMetadataUpdatePayload,
} from "@/api/homepage"
import { DEFAULT_SITE_METADATA } from "@/constants/site"

export const useSiteStore = defineStore("site", () => {
  const metadata = ref<SiteMetadata>({ ...DEFAULT_SITE_METADATA })
  const loading = ref(false)
  const initialized = ref(false)

  const siteName = computed(() => metadata.value.site_name || DEFAULT_SITE_METADATA.site_name)
  const siteTitle = computed(() => metadata.value.site_title || siteName.value)
  const brandInitial = computed(() => (metadata.value.brand_initial || siteName.value.charAt(0) || "Q").slice(0, 4))

  async function fetchPublicMetadata(force = false): Promise<SiteMetadata> {
    if (initialized.value && !force) return metadata.value
    loading.value = true
    try {
      const response = await getPublicSiteMetadata()
      metadata.value = response.data.data ?? { ...DEFAULT_SITE_METADATA }
      initialized.value = true
      applyBrowserMetadata()
      return metadata.value
    } finally {
      loading.value = false
    }
  }

  async function fetchAdminMetadata(): Promise<SiteMetadata> {
    loading.value = true
    try {
      const response = await getAdminSiteMetadata()
      metadata.value = response.data.data ?? { ...DEFAULT_SITE_METADATA }
      initialized.value = true
      applyBrowserMetadata()
      return metadata.value
    } finally {
      loading.value = false
    }
  }

  async function saveMetadata(payload: SiteMetadataUpdatePayload): Promise<SiteMetadata> {
    loading.value = true
    try {
      const response = await updateSiteMetadata(payload)
      metadata.value = response.data.data
      initialized.value = true
      applyBrowserMetadata()
      return metadata.value
    } finally {
      loading.value = false
    }
  }

  function applyBrowserMetadata(pageTitle?: string): void {
    const nextTitle = pageTitle ? `${pageTitle} - ${siteTitle.value}` : siteTitle.value
    document.title = nextTitle
    applyFavicon(metadata.value.favicon_url)
  }

  function applyFavicon(faviconUrl: string): void {
    const existingLink = document.querySelector<HTMLLinkElement>('link[rel="icon"]')
    const iconLink = existingLink ?? document.createElement("link")
    iconLink.rel = "icon"
    iconLink.href = faviconUrl || "/favicon.ico"
    if (!existingLink) document.head.appendChild(iconLink)
  }

  return {
    metadata,
    loading,
    initialized,
    siteName,
    siteTitle,
    brandInitial,
    fetchPublicMetadata,
    fetchAdminMetadata,
    saveMetadata,
    applyBrowserMetadata,
  }
})
