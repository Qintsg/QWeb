/**
 * 根据 Material 3 window size class 判断当前窗口级别。
 *
 * :project: QWeb
 * :file: useWindowSizeClass.ts
 * :author: Qintsg
 * :date: 2026-05-17 00:00
 */
import { computed, type ComputedRef } from "vue"
import { useMediaQuery } from "@vueuse/core"

export type WindowSizeClass = "compact" | "medium" | "expanded" | "large" | "extraLarge"

/**
 * 返回当前 Material 3 window size class。
 *
 * :return: 当前窗口尺寸级别。
 */
export function useWindowSizeClass(): { sizeClass: ComputedRef<WindowSizeClass> } {
  const isMedium = useMediaQuery("(min-width: 600px)")
  const isExpanded = useMediaQuery("(min-width: 840px)")
  const isLarge = useMediaQuery("(min-width: 1200px)")
  const isExtraLarge = useMediaQuery("(min-width: 1600px)")

  const sizeClass = computed<WindowSizeClass>(() => {
    if (isExtraLarge.value) return "extraLarge"
    if (isLarge.value) return "large"
    if (isExpanded.value) return "expanded"
    if (isMedium.value) return "medium"
    return "compact"
  })

  return { sizeClass }
}
