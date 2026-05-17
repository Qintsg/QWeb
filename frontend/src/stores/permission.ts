/**
 * 权限状态管理。
 *
 * :project: QWeb
 * :file: permission.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { getMyPermissions } from "@/api/auth"
import type { ResolvedPermissions } from "@/types/auth"

export const usePermissionStore = defineStore("permission", () => {
  /* ── 状态 ── */
  const permissions = ref<ResolvedPermissions | null>(null)
  const loading = ref(false)

  /* ── 计算属性 ── */

  /** 当前用户拥有的全部权限码集合 */
  const permissionCodes = computed<Set<string>>(() => {
    if (!permissions.value) return new Set()
    return new Set(permissions.value.permissions)
  })

  /* ── 方法 ── */

  /** 从后端获取当前用户权限 */
  async function fetchPermissions() {
    loading.value = true
    try {
      const { data } = await getMyPermissions()
      permissions.value = data.data
    } catch {
      permissions.value = null
    } finally {
      loading.value = false
    }
  }

  /** 检查是否拥有指定权限 */
  function hasPermission(code: string): boolean {
    return permissionCodes.value.has(code)
  }

  /** 检查是否拥有任一权限 */
  function hasAnyPermission(codes: string[]): boolean {
    return codes.some((code) => permissionCodes.value.has(code))
  }

  /** 检查是否拥有全部权限 */
  function hasAllPermissions(codes: string[]): boolean {
    return codes.every((code) => permissionCodes.value.has(code))
  }

  function $reset() {
    permissions.value = null
    loading.value = false
  }

  return {
    permissions,
    loading,
    permissionCodes,
    fetchPermissions,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    $reset,
  }
})
