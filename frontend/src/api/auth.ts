/**
 * 认证相关 API 调用。
 *
 * :project: QWeb
 * :file: auth.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import apiClient from "./client"
import type { ApiResponse } from "@/types/api"
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RefreshResponse,
  BootstrapOwnerRequest,
  BootstrapOwnerResponse,
  BootstrapStatus,
  ChangePasswordRequest,
  UserInfo,
  ResolvedPermissions,
  OAuthAuthorizeResponse,
  OAuthBindRequest,
  OAuthCallbackRequest,
  OAuthCallbackResponse,
  OAuthRegisterRequest,
} from "@/types/auth"

/** 获取首次部署引导状态 */
export function getBootstrapStatus() {
  return apiClient.get<ApiResponse<BootstrapStatus>>("/auth/bootstrap/status/")
}

/** 首次部署创建站长账号 */
export function createBootstrapOwner(payload: BootstrapOwnerRequest) {
  return apiClient.post<ApiResponse<BootstrapOwnerResponse>>("/auth/bootstrap/owner/", payload)
}

/** 用户注册 */
export function register(payload: RegisterRequest) {
  return apiClient.post<ApiResponse<LoginResponse>>("/auth/register/", payload)
}

/** 用户名密码登录 */
export function login(payload: LoginRequest) {
  return apiClient.post<ApiResponse<LoginResponse>>("/auth/login/", payload)
}

/** 获取 OAuth 授权地址 */
export function getOAuthAuthorizeUrl(provider: string, redirect?: string) {
  return apiClient.get<ApiResponse<OAuthAuthorizeResponse>>(
    `/auth/oauth/${provider}/authorize/`,
    { params: { redirect } }
  )
}

/** 完成 OAuth 回调 */
export function completeOAuthLogin(provider: string, payload: OAuthCallbackRequest) {
  return apiClient.post<ApiResponse<OAuthCallbackResponse>>(
    `/auth/oauth/${provider}/callback/`,
    payload
  )
}

/** 绑定 OAuth 到已有账号 */
export function bindOAuthAccount(provider: string, payload: OAuthBindRequest) {
  return apiClient.post<ApiResponse<LoginResponse>>(
    `/auth/oauth/${provider}/bind/`,
    payload
  )
}

/** 使用 OAuth 注册新账号 */
export function registerWithOAuth(provider: string, payload: OAuthRegisterRequest) {
  return apiClient.post<ApiResponse<LoginResponse>>(
    `/auth/oauth/${provider}/register/`,
    payload
  )
}

/** 登出（黑名单 refresh token） */
export function logout(refresh: string) {
  return apiClient.post<ApiResponse<null>>("/auth/logout/", { refresh })
}

/** 刷新 access token */
export function refreshToken(refresh: string) {
  return apiClient.post<ApiResponse<RefreshResponse>>(
    "/auth/token/refresh/",
    { refresh }
  )
}

/** 获取当前用户基本信息 */
export function getMe() {
  return apiClient.get<ApiResponse<UserInfo>>("/me/")
}

/** 更新当前用户资料 */
export function updateMe(payload: Partial<UserInfo>) {
  return apiClient.patch<ApiResponse<UserInfo>>("/me/", payload)
}

/** 修改密码 */
export function changePassword(payload: ChangePasswordRequest) {
  return apiClient.post<ApiResponse<null>>("/me/password/", payload)
}

/** 获取当前用户解析后权限集合（走 IAM 模块） */
export function getMyPermissions() {
  return apiClient.get<ApiResponse<ResolvedPermissions>>("/iam/me/permissions/")
}
