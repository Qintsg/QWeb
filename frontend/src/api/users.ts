/**
 * 用户管理 API（管理员使用）。
 *
 * :project: QWeb
 * :file: users.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import apiClient from "./client"
import type { ApiResponse, PaginatedResponse, ListParams } from "@/types/api"
import type { UserInfo } from "@/types/auth"

/** 用户列表查询参数 */
export interface UserListQuery extends ListParams {
  search?: string
  is_active?: boolean
}

/** 获取用户列表（分页） */
export function getUsers(params?: UserListQuery) {
  return apiClient.get<ApiResponse<PaginatedResponse<UserInfo>>>("/users/", { params })
}

/** 获取单个用户详情 */
export function getUser(userId: number | string) {
  return apiClient.get<ApiResponse<UserInfo>>(`/users/${userId}/`)
}

/** 更新用户信息 */
export function updateUser(userId: number | string, payload: Partial<UserInfo>) {
  return apiClient.patch<ApiResponse<UserInfo>>(`/users/${userId}/`, payload)
}

/** 启用或禁用用户 */
export function toggleUserActive(userId: number | string) {
  return apiClient.post<ApiResponse<UserInfo>>(`/users/${userId}/toggle-active/`)
}
