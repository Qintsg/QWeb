/**
 * 认证状态管理。
 *
 * :project: QWeb
 * :file: auth.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { useRouter } from "vue-router"
import {
  bindOAuthAccount,
  completeOAuthLogin,
  createBootstrapOwner,
  getBootstrapStatus,
  getOAuthAuthorizeUrl,
  login as apiLogin,
  logout as apiLogout,
  getMe,
  registerWithOAuth,
} from "@/api/auth"
import { setTokens, clearTokens, getAccessToken, getRefreshToken } from "@/api/client"
import { usePermissionStore } from "./permission"
import type {
  UserInfo,
  LoginRequest,
  OAuthBindRequest,
  OAuthCallbackRequest,
  OAuthRegisterRequest,
  RegisterRequest,
} from "@/types/auth"

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter()

  /* ── 状态 ── */
  const user = ref<UserInfo | null>(null)
  const loading = ref(false)
  const initialized = ref(false)
  const ownerBootstrapRequired = ref(false)
  const bootstrapChecked = ref(false)

  /* ── 计算属性 ── */
  const isAuthenticated = computed(() => !!user.value && !!getAccessToken())
  const displayName = computed(() => user.value?.nickname || user.value?.username || "")
  const userGroup = computed(() => {
    if (user.value?.user_type === "admin" || user.value?.is_staff) return "admin"
    return "user"
  })

  /* ── 首次部署状态 ── */
  async function checkBootstrapStatus(): Promise<boolean> {
    if (bootstrapChecked.value) return ownerBootstrapRequired.value
    const { data } = await getBootstrapStatus()
    ownerBootstrapRequired.value = data.data.owner_required
    bootstrapChecked.value = true
    return ownerBootstrapRequired.value
  }

  async function createOwnerAccount(payload: RegisterRequest) {
    loading.value = true
    try {
      const { data } = await createBootstrapOwner(payload)
      const result = data.data
      setTokens(result.access, result.refresh)
      ownerBootstrapRequired.value = false
      bootstrapChecked.value = true
      await fetchUser()
      return result
    } finally {
      loading.value = false
    }
  }

  /* ── 登录 ── */
  async function login(credentials: LoginRequest) {
    loading.value = true
    try {
      const { data } = await apiLogin(credentials)
      const result = data.data
      setTokens(result.access, result.refresh)
      await fetchUser()
      return result
    } finally {
      loading.value = false
    }
  }

  /* ── GitHub 登录 ── */
  async function startGitHubLogin(redirect?: string) {
    const { data } = await getOAuthAuthorizeUrl("github", redirect)
    window.location.assign(data.data.authorization_url)
  }

  async function completeGitHubOAuth(payload: OAuthCallbackRequest) {
    loading.value = true
    try {
      const { data } = await completeOAuthLogin("github", payload)
      const result = data.data
      if (result.status === "requires_account_choice") {
        return result
      }
      setTokens(result.access, result.refresh)
      await fetchUser()
      return result
    } finally {
      loading.value = false
    }
  }

  async function bindGitHubOAuth(payload: OAuthBindRequest) {
    loading.value = true
    try {
      const { data } = await bindOAuthAccount("github", payload)
      const result = data.data
      setTokens(result.access, result.refresh)
      await fetchUser()
      return result
    } finally {
      loading.value = false
    }
  }

  async function registerGitHubOAuth(payload: OAuthRegisterRequest) {
    loading.value = true
    try {
      const { data } = await registerWithOAuth("github", payload)
      const result = data.data
      setTokens(result.access, result.refresh)
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
      bootstrapChecked.value = false
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
    ownerBootstrapRequired,
    bootstrapChecked,
    isAuthenticated,
    displayName,
    userGroup,
    checkBootstrapStatus,
    createOwnerAccount,
    login,
    startGitHubLogin,
    completeGitHubOAuth,
    bindGitHubOAuth,
    registerGitHubOAuth,
    logout,
    fetchUser,
    initialize,
  }
})
