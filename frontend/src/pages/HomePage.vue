<!--
  实现 HomePage 页面视图。

  :project: QWeb
  :file: HomePage.vue
  :author: Qintsg
  :date: 2026-05-12 00:00
-->
<script setup lang="ts">
/**
 * 公开首页
 * 展示个人介绍 Hero 区 + 服务链接卡片网格 + Footer
 */
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { getPublicServiceLinks, type ServiceLink } from '@/api/homepage'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const authStore = useAuthStore()

// 页面加载时恢复登录状态
onMounted(() => authStore.initialize())

const serviceLinks = ref<ServiceLink[]>([])
const loading = ref(true)
const error = ref('')

const categoryConfig: Record<string, { label: string; color: string; icon: string }> = {
  project: { label: '项目展示', color: '#0e9aa7', icon: '🎓' },
  server: { label: '服务器管理', color: '#f28a2e', icon: '🖥️' },
  tool: { label: '工具', color: '#7b68ee', icon: '🔧' },
  other: { label: '其他', color: '#6b7280', icon: '🔗' },
}

function getCategoryStyle(category: string) {
  const config = categoryConfig[category] || categoryConfig.other
  return config
}

function getIconForLink(link: ServiceLink): string {
  if (link.icon) return link.icon
  return getCategoryStyle(link.category).icon
}

function getColorForLink(link: ServiceLink): string {
  if (link.color) return link.color
  return getCategoryStyle(link.category).color
}

const currentYear = computed(() => new Date().getFullYear())

async function fetchLinks() {
  loading.value = true
  error.value = ''
  try {
    const response = await getPublicServiceLinks()
    serviceLinks.value = response.data.data ?? []
  } catch {
    error.value = '加载服务链接失败'
  } finally {
    loading.value = false
  }
}

onMounted(fetchLinks)
</script>

<template>
  <div class="home-page">
    <!-- Hero -->
    <header class="hero">
      <div class="hero__bg-orb hero__bg-orb--1"></div>
      <div class="hero__bg-orb hero__bg-orb--2"></div>
      <div class="hero__content">
        <h1 class="hero__title">Qintsg</h1>
        <p class="hero__subtitle">个人基础设施门户 · Personal Infrastructure Portal</p>
        <div class="hero__links">
          <a
            href="https://github.com/qintsg"
            target="_blank"
            rel="noopener noreferrer"
            class="hero__social-link"
            title="GitHub"
          >
            <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            <span>GitHub</span>
          </a>
          <!-- 已登录：进入管理后台 -->
          <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="hero__social-link hero__social-link--login">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            <span>管理后台</span>
          </router-link>
          <!-- 未登录：登录 -->
          <router-link v-else to="/login" class="hero__social-link hero__social-link--login">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
            </svg>
            <span>{{ t('auth.login') }}</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Service Links -->
    <main class="services">
      <h2 class="services__title">服务与项目</h2>
      <p class="services__subtitle">以下是部署在此基础设施上的服务和项目</p>

      <div v-if="loading" class="services__loading">
        <div class="spinner"></div>
        <span>{{ t('common.loading') }}</span>
      </div>

      <div v-else-if="error" class="services__error">
        <p>{{ error }}</p>
        <fluent-button appearance="accent" @click="fetchLinks">重试</fluent-button>
      </div>

      <div v-else-if="serviceLinks.length === 0" class="services__empty">
        <p>暂无服务链接</p>
      </div>

      <div v-else class="services__grid">
        <a
          v-for="(link, index) in serviceLinks"
          :key="link.id"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="service-card"
          :style="{
            '--card-color': getColorForLink(link),
            '--card-delay': `${index * 60}ms`,
          }"
        >
          <div class="service-card__icon">
            {{ getIconForLink(link) }}
          </div>
          <div class="service-card__body">
            <h3 class="service-card__title">{{ link.title }}</h3>
            <p v-if="link.description" class="service-card__desc">{{ link.description }}</p>
            <p v-if="link.remark" class="service-card__remark">{{ link.remark }}</p>
          </div>
          <div class="service-card__category">
            <span
              class="service-card__badge"
              :style="{ background: `${getColorForLink(link)}18`, color: getColorForLink(link) }"
            >
              {{ categoryConfig[link.category]?.label || '其他' }}
            </span>
          </div>
          <div class="service-card__arrow">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M7 17L17 7M17 7H7M17 7v10"/>
            </svg>
          </div>
        </a>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer__content">
        <p class="footer__copyright">Copyright &copy; {{ currentYear }} Qintsg. All rights reserved.</p>
        <p class="footer__icp">
          <a
            href="https://beian.miit.gov.cn/"
            target="_blank"
            rel="noopener noreferrer"
            class="footer__icp-link"
          >
            沪ICP备2026000797号-2
          </a>
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--q-color-canvas);
  color: var(--q-color-text-primary);
}

/* ── Hero ────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  padding: 80px var(--q-space-32) 60px;
  text-align: center;
  background:
    radial-gradient(ellipse at 30% 0%, rgba(14, 154, 167, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 100%, rgba(242, 138, 46, 0.08) 0%, transparent 60%),
    var(--q-color-canvas);
}

.hero__bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  animation: float 20s ease-in-out infinite;
  pointer-events: none;
}

.hero__bg-orb--1 {
  width: 400px;
  height: 400px;
  background: var(--q-color-brand);
  top: -120px;
  left: -80px;
}

.hero__bg-orb--2 {
  width: 300px;
  height: 300px;
  background: var(--q-color-accent);
  bottom: -80px;
  right: -60px;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.05); }
  66% { transform: translate(-20px, 15px) scale(0.95); }
}

.hero__content {
  position: relative;
  z-index: 1;
  max-width: 600px;
  margin: 0 auto;
}

.hero__title {
  margin: 0 0 var(--q-space-12);
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--q-color-brand) 0%, var(--q-color-accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeInUp 0.6s ease-out;
}

.hero__subtitle {
  margin: 0 0 var(--q-space-24);
  font-size: 1.05rem;
  color: var(--q-color-text-secondary);
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.hero__links {
  display: flex;
  justify-content: center;
  gap: var(--q-space-16);
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.hero__social-link {
  display: inline-flex;
  align-items: center;
  gap: var(--q-space-8);
  padding: 10px 20px;
  border-radius: var(--q-radius-md);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all var(--q-duration-normal) var(--q-easing-ease);
  background: var(--q-color-surface);
  color: var(--q-color-text-primary);
  border: 1px solid var(--q-color-stroke);
  box-shadow: var(--q-shadow-sm);
}

.hero__social-link:hover {
  border-color: var(--q-color-brand);
  box-shadow: var(--q-shadow-md);
  transform: translateY(-1px);
}

.hero__social-link--login {
  background: var(--q-color-brand);
  color: #fff;
  border-color: var(--q-color-brand);
}

.hero__social-link--login:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(14, 154, 167, 0.3);
}

/* ── Services ────────────────────────────────── */
.services {
  flex: 1;
  max-width: var(--q-layout-max-width, 1200px);
  width: 100%;
  margin: 0 auto;
  padding: var(--q-space-40) var(--q-space-32);
}

.services__title {
  margin: 0 0 var(--q-space-8);
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  animation: fadeInUp 0.6s ease-out 0.3s both;
}

.services__subtitle {
  margin: 0 0 var(--q-space-32);
  text-align: center;
  color: var(--q-color-text-secondary);
  font-size: 0.9rem;
  animation: fadeInUp 0.6s ease-out 0.35s both;
}

.services__loading,
.services__error,
.services__empty {
  text-align: center;
  padding: var(--q-space-40);
  color: var(--q-color-text-secondary);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--q-color-stroke);
  border-top-color: var(--q-color-brand);
  border-radius: 50%;
  margin: 0 auto var(--q-space-12);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.services__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--q-space-16);
}

/* ── Service Card ────────────────────────────── */
.service-card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: var(--q-space-24);
  background: var(--q-color-surface);
  border: 1px solid var(--q-color-stroke);
  border-radius: var(--q-radius-lg);
  text-decoration: none;
  color: var(--q-color-text-primary);
  transition:
    border-color var(--q-duration-normal) var(--q-easing-ease),
    box-shadow var(--q-duration-normal) var(--q-easing-ease),
    transform var(--q-duration-normal) var(--q-easing-ease);
  animation: cardIn 0.5s ease-out var(--card-delay, 0ms) both;
}

.service-card:hover {
  border-color: var(--card-color, var(--q-color-brand));
  box-shadow: 0 4px 20px color-mix(in srgb, var(--card-color, var(--q-color-brand)) 15%, transparent);
  transform: translateY(-3px);
}

.service-card__icon {
  font-size: 1.75rem;
  margin-bottom: var(--q-space-12);
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--q-radius-md);
  background: color-mix(in srgb, var(--card-color, var(--q-color-brand)) 10%, transparent);
}

.service-card__body {
  flex: 1;
}

.service-card__title {
  margin: 0 0 var(--q-space-8);
  font-size: 1rem;
  font-weight: 600;
}

.service-card__desc {
  margin: 0 0 var(--q-space-4);
  font-size: 0.8125rem;
  color: var(--q-color-text-secondary);
  line-height: 1.5;
}

.service-card__remark {
  margin: var(--q-space-8) 0 0;
  font-size: 0.75rem;
  color: var(--q-color-text-tertiary, #9ca3af);
  font-style: italic;
  line-height: 1.4;
}

.service-card__category {
  margin-top: var(--q-space-12);
}

.service-card__badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--q-radius-full);
  font-size: 0.6875rem;
  font-weight: 600;
}

.service-card__arrow {
  position: absolute;
  top: var(--q-space-16);
  right: var(--q-space-16);
  color: var(--q-color-text-tertiary, #9ca3af);
  opacity: 0;
  transform: translate(-4px, 4px);
  transition:
    opacity var(--q-duration-normal) var(--q-easing-ease),
    transform var(--q-duration-normal) var(--q-easing-ease);
}

.service-card:hover .service-card__arrow {
  opacity: 1;
  transform: translate(0, 0);
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ── Footer ──────────────────────────────────── */
.footer {
  border-top: 1px solid var(--q-color-stroke);
  padding: var(--q-space-24) var(--q-space-32);
  text-align: center;
}

.footer__content {
  max-width: var(--q-layout-max-width, 1200px);
  margin: 0 auto;
}

.footer__copyright {
  margin: 0 0 var(--q-space-4);
  font-size: 0.8125rem;
  color: var(--q-color-text-secondary);
}

.footer__icp {
  margin: 0;
  font-size: 0.75rem;
}

.footer__icp-link {
  color: var(--q-color-text-tertiary, #9ca3af);
  text-decoration: none;
  transition: color var(--q-duration-fast) var(--q-easing-ease);
}

.footer__icp-link:hover {
  color: var(--q-color-brand);
}

/* ── Responsive ──────────────────────────────── */
@media (max-width: 768px) {
  .hero {
    padding: 60px var(--q-space-16) 40px;
  }

  .hero__title {
    font-size: 2rem;
  }

  .services {
    padding: var(--q-space-24) var(--q-space-16);
  }

  .services__grid {
    grid-template-columns: 1fr;
  }

  .hero__links {
    flex-direction: column;
    align-items: center;
  }
}
</style>
