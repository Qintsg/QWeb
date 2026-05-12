/**
 * 权限组合式函数。
 *
 * :project: QWeb
 * :file: usePermission.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import { computed } from "vue"
import { usePermissionStore } from "@/stores/permission"

export function usePermission() {
  const store = usePermissionStore()

  return {
    /** 权限加载中 */
    loading: computed(() => store.loading),
    /** 权限码集合 */
    permissionCodes: computed(() => store.permissionCodes),
    /** 检查是否拥有指定权限 */
    hasPermission: store.hasPermission,
    /** 检查是否拥有任一权限 */
    hasAnyPermission: store.hasAnyPermission,
    /** 检查是否拥有全部权限 */
    hasAllPermissions: store.hasAllPermissions,
  }
}
