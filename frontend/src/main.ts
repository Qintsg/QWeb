import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { setupFluentDesignSystem } from './styles/fluent-setup'

// 全局样式：设计令牌 + 基础重置
import './styles/tokens.css'
import './style.css'

// 初始化 Fluent 2 设计系统
setupFluentDesignSystem()

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
