/**
 * 认证状态管理
 *
 * 管理用户登录状态、Token 存储与用户信息
 */
import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { useRouter } from "vue-router"
import { login as apiLogin, logout as apiLogout, getMe } from "@/api/auth"
import { setTokens, clearTokens, getAccessToken, getRefreshToken } from "@/api/client"
import { usePermissionStore } from "./permission"
import type { UserInfo, LoginRequest } from "@/types/auth"

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter()

  /* ── 状态 ── */
  const user = ref<UserInfo | null>(null)
  const loading = ref(false)
  const initialized = ref(false)

  /* ── 计算属性 ── */
  const isAuthenticated = computed(() => !!user.value && !!getAccessToken())
  const displayName = computed(() => user.value?.display_name || user.value?.username || "")
  const userGroup = computed(() => user.value?.user_group ?? "guest")

  /* ── 登录 ── */
  async function login(credentials: LoginRequest) {
    loading.value = true
    try {
      const { data } = await apiLogin(credentials)
      const result = data.data
      setTokens(result.tokens.access, result.tokens.refresh)
      await fetchUser()
      return result
    } finally {
      loading.value = false
    }
  }

  /* ── 获取当前用户信息 ── */
  async function fetchUser() {
    try {
      const { data } = await getMe()
      user.value = data.data
      // 同步加载权限
      const permissionStore = usePermissionStore()
      await permissionStore.fetchPermissions()
    } catch {
      user.value = null
    }
  }

  /* ── 退出登录 ── */
  async function logout() {
    try {
      const refresh = getRefreshToken()
      if (refresh) await apiLogout(refresh)
    } catch {
      // 即使后端失败也清理本地状态
    } finally {
      user.value = null
      initialized.value = false
      clearTokens()
      const permissionStore = usePermissionStore()
      permissionStore.$reset()
      router.push({ name: "login" })
    }
  }

  /* ── 初始化（页面刷新时恢复状态） ── */
  async function initialize() {
    if (initialized.value) return
    initialized.value = true
    if (getAccessToken()) {
      await fetchUser()
    }
  }

  return {
    user,
    loading,
    initialized,
    isAuthenticated,
    displayName,
    userGroup,
    login,
    logout,
    fetchUser,
    initialize,
  }
})
