/**
 * 用户管理 API（管理员使用）
 *
 * 对应后端 apps/accounts/api/views/user_views.py (UserViewSet)
 * 路由前缀：/api/v1/users/
 */
import apiClient from "./client"
import type { ApiResponse, PaginatedResponse, ListParams } from "@/types/api"
import type { UserInfo, UserGroup } from "@/types/auth"

/** 用户列表查询参数 */
export interface UserListQuery extends ListParams {
  search?: string
  user_group?: UserGroup
  is_active?: boolean
}

/** 创建用户请求 */
export interface CreateUserRequest {
  username: string
  email: string
  password: string
  nickname?: string
  user_group?: UserGroup
}

/** 获取用户列表（分页） */
export function getUsers(params?: UserListQuery) {
  return apiClient.get<ApiResponse<PaginatedResponse<UserInfo>>>("/users/", { params })
}

/** 获取单个用户详情 */
export function getUser(userId: number | string) {
  return apiClient.get<ApiResponse<UserInfo>>(`/users/${userId}/`)
}

/** 创建用户 */
export function createUser(payload: CreateUserRequest) {
  return apiClient.post<ApiResponse<UserInfo>>("/users/", payload)
}

/** 更新用户信息 */
export function updateUser(userId: number | string, payload: Partial<UserInfo>) {
  return apiClient.patch<ApiResponse<UserInfo>>(`/users/${userId}/`, payload)
}

/** 删除用户（软删除） */
export function deleteUser(userId: number | string) {
  return apiClient.delete<ApiResponse<null>>(`/users/${userId}/`)
}
