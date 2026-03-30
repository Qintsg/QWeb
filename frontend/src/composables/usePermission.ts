/**
 * 权限组合式函数
 *
 * 封装权限 store，提供模板层使用的权限检查方法
 * 权限以后端为权威来源，前端仅做 UX 优化
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
