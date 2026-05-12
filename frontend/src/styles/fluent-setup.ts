/**
 * Fluent 2 Web Components 注册入口。
 *
 * :project: QWeb
 * :file: fluent-setup.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import {
  provideFluentDesignSystem,
  fluentButton,
  fluentTextField,
  fluentTextArea,
  fluentCard,
  fluentCheckbox,
  fluentDialog,
  fluentDivider,
  fluentMenu,
  fluentMenuItem,
  fluentProgress,
  fluentProgressRing,
  fluentRadio,
  fluentRadioGroup,
  fluentSearch,
  fluentSelect,
  fluentOption,
  fluentSwitch,
  fluentTab,
  fluentTabPanel,
  fluentTabs,
  fluentTooltip,
  fluentTreeItem,
  fluentTreeView,
  fluentBadge,
  fluentBreadcrumb,
  fluentBreadcrumbItem,
  fluentToolbar,
  fluentAnchor,
  fluentAnchoredRegion,
  fluentAccordion,
  fluentAccordionItem,
  fluentCombobox,
  fluentDataGrid,
  fluentDataGridCell,
  fluentDataGridRow,
  fluentListbox,
  accentBaseColor,
  SwatchRGB,
  baseLayerLuminance,
  StandardLuminance,
  fillColor,
  neutralBaseColor,
} from "@fluentui/web-components"

/**
 * 将 HEX 颜色解析为 SwatchRGB 实例
 */
function hexToSwatch(hex: string): ReturnType<typeof SwatchRGB.create> {
  const r = parseInt(hex.slice(1, 3), 16) / 255
  const g = parseInt(hex.slice(3, 5), 16) / 255
  const b = parseInt(hex.slice(5, 7), 16) / 255
  return SwatchRGB.create(r, g, b)
}

/**
 * 注册 Fluent 2 设计系统并配置品牌色
 *
 * - 主色: 青色 #0e9aa7
 * - 中性底: 暖灰 #8a8480
 * - 亮色模式
 */
export function setupFluentDesignSystem(): void {
  /* 注册所有需要的 Fluent 组件 */
  provideFluentDesignSystem().register(
    fluentButton(),
    fluentTextField(),
    fluentTextArea(),
    fluentCard(),
    fluentCheckbox(),
    fluentDialog(),
    fluentDivider(),
    fluentMenu(),
    fluentMenuItem(),
    fluentProgress(),
    fluentProgressRing(),
    fluentRadio(),
    fluentRadioGroup(),
    fluentSearch(),
    fluentSelect(),
    fluentOption(),
    fluentSwitch(),
    fluentTab(),
    fluentTabPanel(),
    fluentTabs(),
    fluentTooltip(),
    fluentTreeItem(),
    fluentTreeView(),
    fluentBadge(),
    fluentBreadcrumb(),
    fluentBreadcrumbItem(),
    fluentToolbar(),
    fluentAnchor(),
    fluentAnchoredRegion(),
    fluentAccordion(),
    fluentAccordionItem(),
    fluentCombobox(),
    fluentDataGrid(),
    fluentDataGridCell(),
    fluentDataGridRow(),
    fluentListbox()
  )

  /* 品牌色：青色 */
  accentBaseColor.withDefault(hexToSwatch("#0e9aa7"))

  /* 中性色：暖灰，让自动生成的中性色阶偏暖 */
  neutralBaseColor.withDefault(hexToSwatch("#8a8480"))

  /* 亮色模式 */
  baseLayerLuminance.withDefault(StandardLuminance.LightMode)
}
