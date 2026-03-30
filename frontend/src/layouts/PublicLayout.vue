<!--
  公开布局 - 用于登录、注册等未认证页面
  居中卡片式布局，背景使用品牌色渐变
-->
<template>
  <div class="public-layout">
    <div class="public-layout__card">
      <div class="public-layout__brand">
        <h1 class="public-layout__title">QWeb</h1>
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
    radial-gradient(circle at 20% 20%, var(--qweb-primary-light) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, var(--qweb-accent-light) 0%, transparent 50%),
    var(--qweb-neutral-2);
  padding: var(--qweb-spacing-lg);
}

.public-layout__card {
  width: 100%;
  max-width: 420px;
  background: var(--qweb-neutral-1);
  border-radius: var(--qweb-radius-xl);
  box-shadow: var(--qweb-shadow-lg);
  padding: var(--qweb-spacing-2xl) var(--qweb-spacing-xl);
}

.public-layout__brand {
  text-align: center;
  margin-bottom: var(--qweb-spacing-xl);
}

.public-layout__title {
  margin: 0;
  font-size: var(--qweb-font-2xl);
  font-weight: 700;
  color: var(--qweb-primary);
  letter-spacing: -0.02em;
}

.public-layout__subtitle {
  margin: var(--qweb-spacing-xs) 0 0;
  font-size: var(--qweb-font-sm);
  color: var(--qweb-text-secondary);
}

.public-layout__footer {
  margin-top: var(--qweb-spacing-lg);
}

.lang-switch {
  background: transparent;
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-sm);
  padding: var(--qweb-spacing-xs) var(--qweb-spacing-sm);
  color: var(--qweb-text-secondary);
  cursor: pointer;
  font-size: var(--qweb-font-sm);
  transition: all 0.15s ease;
}

.lang-switch:hover {
  border-color: var(--qweb-primary);
  color: var(--qweb-primary);
}
</style>
