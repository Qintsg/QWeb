<!--
  公开布局 - 用于登录、注册等未认证页面
  居中卡片式布局，背景使用品牌色渐变
-->
<template>
  <div class="public-layout">
    <div class="public-layout__card">
      <div class="public-layout__brand">
        <h1 class="public-layout__title">Qintsg's Web</h1>
        <p class="public-layout__subtitle">{{ t('common.appName') }}</p>
      </div>
      <router-view />
    </div>
    <!-- 语言切换 -->
    <div class="public-layout__footer">
      <button class="lang-switch" @click="toggleLocale">
        {{ locale === 'zh-CN' ? 'EN' : '中' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

function toggleLocale() {
  locale.value = locale.value === 'zh-CN' ? 'en-US' : 'zh-CN'
}
</script>

<style scoped>
.public-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background:
    radial-gradient(circle at 20% 20%, var(--q-color-brand-light) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, var(--q-color-accent-light) 0%, transparent 50%),
    var(--q-color-canvas);
  padding: var(--q-space-24);
}

.public-layout__card {
  width: 100%;
  max-width: min(860px, 100%);
  background: var(--q-color-surface);
  border-radius: var(--q-radius-xl);
  box-shadow: var(--q-shadow-lg);
  padding: var(--q-space-40) var(--q-space-32);
}

.public-layout__brand {
  text-align: center;
  margin-bottom: var(--q-space-32);
}

.public-layout__title {
  margin: 0;
  font-size: var(--q-font-size-2xl);
  font-weight: 700;
  color: var(--q-color-brand);
  letter-spacing: -0.02em;
}

.public-layout__subtitle {
  margin: var(--q-space-8) 0 0;
  font-size: var(--q-font-size-sm);
  color: var(--q-color-text-secondary);
}

.public-layout__footer {
  margin-top: var(--q-space-24);
}

.lang-switch {
  background: transparent;
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-sm);
  padding: var(--q-space-8) var(--q-space-12);
  color: var(--q-color-text-secondary);
  cursor: pointer;
  font-size: var(--q-font-size-sm);
  transition: all 0.15s ease;
}

.lang-switch:hover {
  border-color: var(--q-color-brand);
  color: var(--q-color-brand);
}
</style>
