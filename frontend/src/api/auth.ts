/**
 * 认证相关 API 调用
 *
 * 对应后端 apps/accounts/views/auth_views.py
 */
import apiClient from "./client"
import type { ApiResponse } from "@/types/api"
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RefreshResponse,
  ChangePasswordRequest,
  UserInfo,
  ResolvedPermissions,
} from "@/types/auth"

/** 用户注册 */
export function register(payload: RegisterRequest) {
  return apiClient.post<ApiResponse<UserInfo>>("/auth/register/", payload)
}

/** 用户名密码登录 */
export function login(payload: LoginRequest) {
  return apiClient.post<ApiResponse<LoginResponse>>("/auth/login/", payload)
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
