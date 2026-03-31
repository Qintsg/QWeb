<!--
  仪表盘布局 - 用于已认证的管理页面
  左侧导航栏 + 顶部头栏 + 内容区域
-->
<template>
  <div class="dashboard-layout">
    <AppSidebar
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
    />
    <div class="dashboard-layout__main" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <AppHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="dashboard-layout__content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import AppHeader from '@/components/common/AppHeader.vue'

const sidebarCollapsed = ref(false)
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: var(--q-color-canvas);
}

.dashboard-layout__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 260px;
  transition: margin-left 0.2s ease;
}

.dashboard-layout__main.sidebar-collapsed {
  margin-left: 64px;
}

.dashboard-layout__content {
  flex: 1;
  padding: var(--q-space-24);
  overflow-y: auto;
}

@media (max-width: 768px) {
  .dashboard-layout__main {
    margin-left: 0;
  }
}
</style>
