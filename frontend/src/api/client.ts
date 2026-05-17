/**
 * Axios 全局实例。
 *
 * - 自动从本地持久化读取 access token 附加到请求头
 * - 401 时尝试用 refresh token 续签，续签失败则清理令牌并跳转登录
 * - 保持后端 ApiResponse envelope，由调用方读取业务 data
 *
 * :project: QWeb
 * :file: client.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import axios, {
  type AxiosError,
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from "axios"

/** 后端基地址；优先读 Vite 环境变量 */
const BASE_URL: string =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"

/** 创建 axios 实例 */
const apiClient: AxiosInstance = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  timeout: 15_000,
  headers: { "Content-Type": "application/json" },
})

/* ── 令牌持久化辅助（避免循环依赖 store） ───────── */

const TOKEN_KEY = "qweb_access_token"
const REFRESH_KEY = "qweb_refresh_token"

export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}

export function setTokens(access: string, refresh: string): void {
  localStorage.setItem(TOKEN_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

/* ── 请求拦截：附加 Bearer token ────────────────── */

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getAccessToken()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/* ── 响应拦截：401 自动续签 ─────────────────────── */

let isRefreshing = false
let pendingQueue: Array<{
  resolve: (token: string) => void
  reject: (error: unknown) => void
}> = []

function processPendingQueue(token: string | null, error: unknown): void {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (token) resolve(token)
    else reject(error)
  })
  pendingQueue = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    /* 非 401 或已重试过，直接抛出 */
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    /* 无 refresh token，直接跳转登录 */
    const refreshToken = getRefreshToken()
    if (!refreshToken) {
      clearTokens()
      window.location.href = "/login"
      return Promise.reject(error)
    }

    /* 正在续签中，将当前请求排入等待队列 */
    if (isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        pendingQueue.push({ resolve, reject })
      }).then((newToken) => {
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`
        }
        return apiClient(originalRequest)
      })
    }

    /* 发起续签 */
    originalRequest._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(`${BASE_URL}/api/v1/auth/token/refresh/`, {
        refresh: refreshToken,
      })
      const newAccess: string = data.data?.access ?? data.access
      const newRefresh: string = data.data?.refresh ?? data.refresh
      setTokens(newAccess, newRefresh)
      processPendingQueue(newAccess, null)

      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${newAccess}`
      }
      return apiClient(originalRequest)
    } catch (refreshError) {
      processPendingQueue(null, refreshError)
      clearTokens()
      window.location.href = "/login"
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default apiClient
