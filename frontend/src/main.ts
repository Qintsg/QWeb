/**
 * 定义 main 前端源码。
 *
 * :project: QWeb
 * :file: main.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { setupMaterialDesignSystem } from './styles/material-setup'
import { useSiteStore } from './stores/site'

// 全局样式：Material 3 设计令牌 + 基础重置
import './styles/tokens.css'
import './style.css'

// 初始化 Material 3 Web Components
setupMaterialDesignSystem()

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)
app.mount('#app')

useSiteStore(pinia).fetchPublicMetadata().catch(() => {
  useSiteStore(pinia).applyBrowserMetadata()
})
