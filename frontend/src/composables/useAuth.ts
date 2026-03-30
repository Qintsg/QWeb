/**
 * 认证组合式函数
 *
 * 封装认证 store 的常用操作，提供便捷的模板层调用接口
 */
import { computed } from "vue"
import { useAuthStore } from "@/stores/auth"

export function useAuth() {
  const store = useAuthStore()

  return {
    /** 当前用户信息 */
    user: computed(() => store.user),
    /** 是否已认证 */
    isAuthenticated: computed(() => store.isAuthenticated),
    /** 显示名称 */
    displayName: computed(() => store.displayName),
    /** 用户组 */
    userGroup: computed(() => store.userGroup),
    /** 是否加载中 */
    loading: computed(() => store.loading),
    /** 登录 */
    login: store.login,
    /** 退出登录 */
    logout: store.logout,
    /** 初始化认证状态 */
    initialize: store.initialize,
  }
}
