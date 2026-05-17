<!--
  根组件，提供跳转主内容入口。

  :project: QWeb
  :file: App.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<template>
  <a class="skip-link" href="#main-content">跳转到主内容</a>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from "vue-router"
</script>
