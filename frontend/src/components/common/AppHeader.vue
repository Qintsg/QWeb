<!--
  顶部头栏
  显示面包屑/页面标题、用户菜单、语言切换
-->
<template>
  <header class="header">
    <!-- 移动端菜单按钮 -->
    <button class="header__menu-btn" @click="$emit('toggleSidebar')">
      ☰
    </button>

    <div class="header__spacer" />

    <!-- 语言切换 -->
    <button class="header__action" @click="toggleLocale" :title="t('common.switchLang')">
      {{ locale === 'zh-CN' ? 'EN' : '中' }}
    </button>

    <!-- 用户菜单 -->
    <div class="header__user" @click="userMenuOpen = !userMenuOpen">
      <span class="header__avatar">
        {{ displayName.charAt(0).toUpperCase() }}
      </span>
      <span class="header__username">{{ displayName }}</span>

      <!-- 下拉菜单 -->
      <div v-if="userMenuOpen" class="header__dropdown">
        <router-link to="/profile" class="header__dropdown-item" @click="userMenuOpen = false">
          {{ t('nav.profile') }}
        </router-link>
        <button class="header__dropdown-item header__dropdown-item--danger" @click="handleLogout">
          {{ t('auth.logout') }}
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'

defineEmits<{
  toggleSidebar: []
}>()

const router = useRouter()
const { t, locale } = useI18n()
const { displayName, logout } = useAuth()

const userMenuOpen = ref(false)

function toggleLocale() {
  locale.value = locale.value === 'zh-CN' ? 'en-US' : 'zh-CN'
}

async function handleLogout() {
  userMenuOpen.value = false
  await logout()
  router.push('/login')
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 var(--qweb-spacing-lg);
  background: var(--qweb-neutral-1);
  border-bottom: 1px solid var(--qweb-border);
  gap: var(--qweb-spacing-sm);
}

.header__menu-btn {
  display: none;
  background: transparent;
  border: none;
  font-size: var(--qweb-font-xl);
  cursor: pointer;
  color: var(--qweb-text-secondary);
  padding: var(--qweb-spacing-xs);
}

.header__spacer {
  flex: 1;
}

.header__action {
  background: transparent;
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-sm);
  padding: var(--qweb-spacing-xs) var(--qweb-spacing-sm);
  color: var(--qweb-text-secondary);
  cursor: pointer;
  font-size: var(--qweb-font-sm);
  transition: all 0.15s ease;
}

.header__action:hover {
  border-color: var(--qweb-primary);
  color: var(--qweb-primary);
}

.header__user {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--qweb-spacing-xs);
  cursor: pointer;
  padding: var(--qweb-spacing-xs) var(--qweb-spacing-sm);
  border-radius: var(--qweb-radius-md);
  transition: background 0.15s ease;
}

.header__user:hover {
  background: var(--qweb-neutral-2);
}

.header__avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--qweb-primary);
  color: white;
  font-weight: 600;
  font-size: var(--qweb-font-sm);
}

.header__username {
  font-size: var(--qweb-font-sm);
  color: var(--qweb-text-primary);
  font-weight: 500;
}

.header__dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: var(--qweb-spacing-xs);
  min-width: 160px;
  background: var(--qweb-neutral-1);
  border: 1px solid var(--qweb-border);
  border-radius: var(--qweb-radius-md);
  box-shadow: var(--qweb-shadow-lg);
  z-index: var(--qweb-z-dropdown);
  overflow: hidden;
}

.header__dropdown-item {
  display: block;
  width: 100%;
  padding: var(--qweb-spacing-sm) var(--qweb-spacing-md);
  background: transparent;
  border: none;
  text-align: left;
  text-decoration: none;
  color: var(--qweb-text-primary);
  font-size: var(--qweb-font-sm);
  cursor: pointer;
  transition: background 0.15s ease;
}

.header__dropdown-item:hover {
  background: var(--qweb-neutral-2);
}

.header__dropdown-item--danger {
  color: var(--qweb-error);
}

.header__dropdown-item--danger:hover {
  background: #fef2f2;
}

@media (max-width: 768px) {
  .header__menu-btn {
    display: block;
  }

  .header__username {
    display: none;
  }
}
</style>
