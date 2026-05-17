<!--
  仪表盘首页视图。

  :project: QWeb
  :file: DashboardPage.vue
  :author: Qintsg
  :date: 2026-05-17 00:00
-->
<script setup lang="ts">
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useAuth } from "@/composables/useAuth"
import { usePermission } from "@/composables/usePermission"
import PageHeader from "@/components/common/PageHeader.vue"
import StatusPill from "@/components/common/StatusPill.vue"

const { t } = useI18n()
const { displayName, userGroup } = useAuth()
const { hasPermission } = usePermission()

const quickNavItems = computed(() => [
  { to: "/profile", icon: "person", label: t("nav.profile"), visible: true },
  { to: "/users", icon: "group", label: t("nav.userManagement"), visible: hasPermission("accounts.user.view") },
  { to: "/roles", icon: "admin_panel_settings", label: t("nav.roleManagement"), visible: hasPermission("iam.role.view") },
  { to: "/audit-logs", icon: "assignment", label: t("nav.auditLogs"), visible: hasPermission("audit.log.view") },
].filter((item) => item.visible))
</script>

<template>
  <div class="dashboard-page">
    <PageHeader
      :title="t('dashboard.welcome', { name: displayName })"
      :description="t('dashboard.subtitle')"
      eyebrow="Workspace"
    >
      <template #actions>
        <StatusPill :label="userGroup" tone="primary" icon="verified_user" />
      </template>
    </PageHeader>

    <section class="dashboard-hero" aria-labelledby="dashboard-overview-title">
      <div>
        <p class="dashboard-hero__eyebrow">Control Plane</p>
        <h2 id="dashboard-overview-title">把身份、权限和审计放在同一个工作面。</h2>
        <p>当前工作区优先展示可执行入口；没有权限的模块不会出现在导航与快捷操作里。</p>
      </div>
      <div class="dashboard-hero__metrics" aria-label="当前状态摘要">
        <span>
          <strong>{{ quickNavItems.length }}</strong>
          <small>available actions</small>
        </span>
        <span>
          <strong>{{ userGroup }}</strong>
          <small>current group</small>
        </span>
      </div>
    </section>

    <section class="dashboard-section" aria-labelledby="quick-nav-title">
      <div class="dashboard-section__header">
        <h2 id="quick-nav-title">{{ t('dashboard.quickNav') }}</h2>
        <p>按当前 IAM 权限过滤后的高频入口。</p>
      </div>
      <div class="quick-nav">
        <router-link v-for="item in quickNavItems" :key="item.to" :to="item.to" class="quick-nav__item">
          <span class="material-symbols-rounded" aria-hidden="true">{{ item.icon }}</span>
          <strong>{{ item.label }}</strong>
          <span class="material-symbols-rounded quick-nav__arrow" aria-hidden="true">arrow_forward</span>
        </router-link>
      </div>
    </section>

    <section class="dashboard-section dashboard-section--status" aria-labelledby="status-title">
      <div class="dashboard-section__header">
        <h2 id="status-title">{{ t('dashboard.systemStatus') }}</h2>
        <p>服务健康、任务队列和实时通道将在后续模块接入后显示。</p>
      </div>
      <div class="status-grid">
        <StatusPill label="API online" tone="success" icon="cloud_done" />
        <StatusPill label="JWT enabled" tone="primary" icon="key" />
        <StatusPill label="Audit ready" tone="warning" icon="history" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard-page {
  display: grid;
  gap: var(--space-xl);
}

.dashboard-hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: var(--space-xl);
  padding: clamp(var(--space-lg), 4vw, var(--space-xxl));
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background:
    radial-gradient(circle at 85% 20%, color-mix(in srgb, var(--md-sys-color-primary) 18%, transparent), transparent 18rem),
    var(--md-sys-color-surface-container-low);
  overflow: hidden;
}

.dashboard-hero__eyebrow {
  margin-block-end: var(--space-sm);
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  line-height: var(--md-sys-typescale-label-large-line-height);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.dashboard-hero h2,
.dashboard-section__header h2 {
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-headline-medium-font);
  font-size: var(--md-sys-typescale-headline-medium-size);
  font-weight: var(--md-sys-typescale-headline-medium-weight);
  line-height: var(--md-sys-typescale-headline-medium-line-height);
}

.dashboard-hero p:last-child,
.dashboard-section__header p {
  max-inline-size: 60ch;
  margin-block-start: var(--space-sm);
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-weight: var(--md-sys-typescale-body-medium-weight);
  line-height: var(--md-sys-typescale-body-medium-line-height);
}

.dashboard-hero__metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(8rem, 1fr));
  gap: var(--space-sm);
}

.dashboard-hero__metrics span {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-md);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-large);
  background: var(--md-sys-color-surface-container);
}

.dashboard-hero__metrics strong {
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-headline-small-font);
  font-size: var(--md-sys-typescale-headline-small-size);
  font-weight: var(--md-sys-typescale-headline-small-weight);
  line-height: var(--md-sys-typescale-headline-small-line-height);
}

.dashboard-hero__metrics small {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-small-font);
  font-size: var(--md-sys-typescale-label-small-size);
  font-weight: var(--md-sys-typescale-label-small-weight);
  line-height: var(--md-sys-typescale-label-small-line-height);
}

.dashboard-section {
  display: grid;
  gap: var(--space-md);
}

.quick-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 13rem), 1fr));
  gap: var(--space-md);
}

.quick-nav__item {
  min-block-size: 7rem;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-container-low);
  transition:
    border-color var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    box-shadow var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
    transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard);
}

.quick-nav__item:hover {
  border-color: var(--md-sys-color-primary);
  box-shadow: var(--md-sys-elevation-level2);
  transform: translateY(calc(var(--space-xs) * -1));
}

.quick-nav__item > .material-symbols-rounded:first-child {
  inline-size: 3rem;
  block-size: 3rem;
  display: grid;
  place-items: center;
  border-radius: var(--md-sys-shape-corner-large);
  color: var(--md-sys-color-on-primary-container);
  background: var(--md-sys-color-primary-container);
}

.quick-nav__item strong {
  font-family: var(--md-sys-typescale-title-medium-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  line-height: var(--md-sys-typescale-title-medium-line-height);
}

.quick-nav__arrow {
  color: var(--md-sys-color-on-surface-variant);
}

.status-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  padding: var(--space-lg);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
}

@media (max-width: 839px) {
  .dashboard-hero {
    grid-template-columns: 1fr;
  }

  .dashboard-hero__metrics {
    grid-template-columns: 1fr;
  }
}
</style>
