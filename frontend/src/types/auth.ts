/**
 * 认证与用户相关类型定义
 *
 * 与后端 accounts/serializers.py 及 iam/ 模块对应。
 */

/** 用户基本信息（登录后返回） */
export interface UserInfo {
  id: string
  username: string
  email: string
  display_name: string
  user_group: UserGroup
  is_active: boolean
  date_joined: string
  last_login: string | null
}

/** 用户资料（完整） */
export interface UserProfile {
  avatar: string | null
  bio: string
  phone: string
  location: string
  website: string
  language: string
  timezone: string
}

/** 用户组枚举 */
export type UserGroup = "owner" | "admin" | "trusted" | "user" | "guest"

/** 登录请求 */
export interface LoginRequest {
  username: string
  password: string
}

/** 注册请求 */
export interface RegisterRequest {
  username: string
  email: string
  password: string
  password_confirm: string
}

/** 登录响应 */
export interface LoginResponse {
  user: UserInfo
  tokens: TokenPair
}

/** JWT 令牌对 */
export interface TokenPair {
  access: string
  refresh: string
}

/** 令牌刷新请求 */
export interface RefreshRequest {
  refresh: string
}

/** 令牌刷新响应 */
export interface RefreshResponse {
  access: string
  refresh: string
}

/** 修改密码请求 */
export interface ChangePasswordRequest {
  old_password: string
  new_password: string
  new_password_confirm: string
}

/** IAM 权限项 */
export interface Permission {
  id: string
  codename: string
  name: string
  description: string
  module: string
  category: string
}

/** IAM 角色 */
export interface Role {
  id: string
  name: string
  display_name: string
  description: string
  is_system: boolean
  permissions: Permission[]
}

/** 用户权限覆盖 */
export interface PermissionOverride {
  id: string
  permission: Permission
  override_type: "allow" | "deny"
}

/** 当前用户的解析后权限集合 */
export interface ResolvedPermissions {
  permissions: string[]
  roles: string[]
  user_group: UserGroup
}
