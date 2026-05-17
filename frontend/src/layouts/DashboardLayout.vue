<!--
  仪表盘布局 - Material 3 自适应 App Shell。

  :project: QWeb
  :file: DashboardLayout.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <div class="dashboard-layout" :data-size="sizeClass">
    <AppSidebar />
    <div class="dashboard-layout__main">
      <AppHeader />
      <main id="main-content" class="dashboard-layout__content" tabindex="-1">
        <router-view v-slot="{ Component }">
          <Transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from "@/components/common/AppSidebar.vue"
import AppHeader from "@/components/common/AppHeader.vue"
import { useWindowSizeClass } from "@/composables/useWindowSizeClass"

const { sizeClass } = useWindowSizeClass()
</script>

<style scoped>
.dashboard-layout {
  min-block-size: 100dvh;
  display: grid;
  grid-template-columns: var(--q-layout-drawer-width) minmax(0, 1fr);
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface);
}

.dashboard-layout[data-size="medium"],
.dashboard-layout[data-size="expanded"] {
  grid-template-columns: var(--q-layout-rail-width) minmax(0, 1fr);
}

.dashboard-layout[data-size="compact"] {
  grid-template-columns: minmax(0, 1fr);
}

.dashboard-layout__main {
  min-inline-size: 0;
  display: flex;
  flex-direction: column;
}

.dashboard-layout__content {
  inline-size: min(100%, var(--q-layout-content-max));
  margin-inline: auto;
  padding-block: 0 calc(var(--space-xxl) + env(safe-area-inset-bottom));
  padding-inline: clamp(var(--space-md), 3vw, var(--space-xxl));
}

.dashboard-layout[data-size="compact"] .dashboard-layout__content {
  padding-block-end: calc(var(--q-layout-bottom-nav-height) + var(--space-xl));
}
</style>
