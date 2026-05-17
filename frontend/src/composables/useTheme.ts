/**
 * 管理 Material 3 明暗主题模式。
 *
 * :project: QWeb
 * :file: useTheme.ts
 * :author: Qintsg
 * :date: 2026-05-17 00:00
 */
import { ref, watchEffect } from "vue"

export type ThemeMode = "system" | "light" | "dark"

const THEME_STORAGE_KEY = "qweb_theme_mode"

const storedTheme = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode | null
const mode = ref<ThemeMode>(storedTheme ?? "system")

/**
 * 提供主题模式状态，并同步到 html[data-theme]。
 *
 * :return: 主题模式引用。
 */
export function useTheme(): { mode: typeof mode } {
  watchEffect(() => {
    const root = document.documentElement
    if (mode.value === "system") {
      root.removeAttribute("data-theme")
    } else {
      root.setAttribute("data-theme", mode.value)
    }
    localStorage.setItem(THEME_STORAGE_KEY, mode.value)
  })

  return { mode }
}
