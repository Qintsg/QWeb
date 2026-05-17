/**
 * IAM 权限管理 API。
 *
 * :project: QWeb
 * :file: iam.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import apiClient from "./client"
import type { ApiResponse, ListParams } from "@/types/api"
import type {
  Permission,
  Role,
  UserRole,
  PermissionOverride,
  ResolvedPermissions,
} from "@/types/auth"

/* ── 权限 ─────────────────────────────────────── */

/** 权限列表查询参数 */
export interface PermissionListQuery extends ListParams {
  search?: string
  module?: string
  category?: string
}

/** 获取权限列表 */
export function getPermissions(params?: PermissionListQuery) {
  return apiClient.get<ApiResponse<Permission[]>>("/iam/permissions/", { params })
}

/* ── 角色 ─────────────────────────────────────── */

/** 角色列表查询参数 */
export interface RoleListQuery extends ListParams {
  search?: string
}

/** 获取角色列表 */
export function getRoles(params?: RoleListQuery) {
  return apiClient.get<ApiResponse<Role[]>>("/iam/roles/", { params })
}

/** 获取角色详情 */
export function getRole(roleId: string) {
  return apiClient.get<ApiResponse<Role>>(`/iam/roles/${roleId}/`)
}

/** 创建角色 */
export interface CreateRoleRequest {
  name: string
  display_name: string
  description?: string
}

export function createRole(payload: CreateRoleRequest) {
  return apiClient.post<ApiResponse<Role>>("/iam/roles/", payload)
}

/** 更新角色 */
export function updateRole(roleId: string, payload: Partial<CreateRoleRequest>) {
  return apiClient.patch<ApiResponse<Role>>(`/iam/roles/${roleId}/`, payload)
}

/** 删除角色 */
export function deleteRole(roleId: string) {
  return apiClient.delete<ApiResponse<null>>(`/iam/roles/${roleId}/`)
}

/** 设置角色权限 */
export function setRolePermissions(roleId: string, permissionIds: string[]) {
  return apiClient.put<ApiResponse<{ count: number }>>(`/iam/roles/${roleId}/permissions/`, {
    permission_ids: permissionIds,
  })
}

/* ── 用户角色 ─────────────────────────────────── */

/** 获取用户角色列表 */
export function getUserRoles(userId: string) {
  return apiClient.get<ApiResponse<UserRole[]>>(`/iam/users/${userId}/roles/`)
}

/** 为用户分配或移除角色 */
export interface UserRoleRequest {
  role_id: string
}

export function assignUserRole(userId: string, payload: UserRoleRequest) {
  return apiClient.post<ApiResponse<UserRole>>(`/iam/users/${userId}/roles/manage/`, payload)
}

export function unassignUserRole(userId: string, payload: UserRoleRequest) {
  return apiClient.delete<ApiResponse<null>>(`/iam/users/${userId}/roles/manage/`, { data: payload })
}

/* ── 用户权限覆盖 ─────────────────────────────── */

/** 获取用户权限覆盖列表 */
export function getUserOverrides(userId: string) {
  return apiClient.get<ApiResponse<PermissionOverride[]>>(`/iam/users/${userId}/overrides/`)
}

/** 添加或移除用户权限覆盖 */
export interface AddOverrideRequest {
  permission_code: string
  effect: "allow" | "deny"
  reason?: string
}

export interface RemoveOverrideRequest {
  permission_code: string
}

export function addUserOverride(userId: string, payload: AddOverrideRequest) {
  return apiClient.post<ApiResponse<PermissionOverride>>(`/iam/users/${userId}/overrides/manage/`, payload)
}

export function removeUserOverride(userId: string, payload: RemoveOverrideRequest) {
  return apiClient.delete<ApiResponse<null>>(`/iam/users/${userId}/overrides/manage/`, { data: payload })
}

/** 获取当前用户的解析后权限 */
export function getMyPermissions() {
  return apiClient.get<ApiResponse<ResolvedPermissions>>("/iam/me/permissions/")
}
