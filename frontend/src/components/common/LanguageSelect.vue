<!--
  语言选择下拉框。

  :project: QWeb
  :file: LanguageSelect.vue
  :author: Qintsg
  :date: 2026-05-18 12:15
-->
<script setup lang="ts">
import { useI18n } from "vue-i18n"

const { locale, t } = useI18n()

const languageOptions = [
  { value: "zh-CN", label: "简体中文" },
  { value: "en-US", label: "English" },
]

function handleLanguageChange(event: Event): void {
  locale.value = (event.target as HTMLSelectElement).value
}
</script>

<template>
  <label class="language-select">
    <span class="material-symbols-rounded" aria-hidden="true">translate</span>
    <span class="language-select__label">{{ t('common.language') }}</span>
    <select :value="locale" :aria-label="t('common.language')" @change="handleLanguageChange">
      <option v-for="option in languageOptions" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>

<style scoped>
.language-select {
  min-block-size: 2.75rem;
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding-inline: var(--space-sm);
  border: 0.0625rem solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  background: var(--md-sys-color-surface-container);
}

.language-select__label {
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-label-medium-font);
  font-size: var(--md-sys-typescale-label-medium-size);
  font-weight: var(--md-sys-typescale-label-medium-weight);
  line-height: var(--md-sys-typescale-label-medium-line-height);
}

.language-select select {
  border: none;
  color: var(--md-sys-color-on-surface);
  background: transparent;
  font: inherit;
  outline: none;
}

@media (max-width: 599px) {
  .language-select__label {
    position: absolute;
    inline-size: 1px;
    block-size: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
  }
}
</style>
