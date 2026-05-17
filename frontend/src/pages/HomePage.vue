<!--
  公开首页页面视图。

  :project: QWeb
  :file: HomePage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { getPublicServiceLinks, type ServiceLink } from "@/api/homepage"
import { useAuthStore } from "@/stores/auth"
import HomeFooter from "@/components/home/HomeFooter.vue"
import HomeHero from "@/components/home/HomeHero.vue"
import ServiceDirectory from "@/components/home/ServiceDirectory.vue"

const authStore = useAuthStore()

const serviceLinks = ref<ServiceLink[]>([])
const loading = ref(true)
const error = ref("")

async function fetchLinks(): Promise<void> {
  loading.value = true
  error.value = ""
  try {
    const response = await getPublicServiceLinks()
    serviceLinks.value = response.data.data ?? []
  } catch {
    error.value = "加载服务链接失败"
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  authStore.initialize()
  fetchLinks()
})
</script>

<template>
  <div class="home-page">
    <HomeHero :is-authenticated="authStore.isAuthenticated" :service-links="serviceLinks" />
    <ServiceDirectory
      :service-links="serviceLinks"
      :loading="loading"
      :error="error"
      @retry="fetchLinks"
    />
    <HomeFooter />
  </div>
</template>

<style scoped>
.home-page {
  min-block-size: 100dvh;
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface);
}
</style>
