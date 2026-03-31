/**
 * 认证与用户相关类型定义
 */

export interface UserInfo {
  id: string
  username: string
  email: string
  display_name: string
  user_group: UserGroup
  is_active: boolean
  date_joined: string
  last_login: string | null
  profile?: UserProfile
}

export interface UserProfile {
  avatar: string | null
  bio: string
  phone: string
  timezone: string
  language: string
  theme_preference: string
  website?: string
  location?: string
}

export type UserGroup = "owner" | "admin" | "trusted" | "user" | "guest"

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  password_confirm: string
}

export interface LoginResponse {
  user: UserInfo
  tokens: TokenPair
}

export interface TokenPair {
  access: string
  refresh: string
}

export interface RefreshRequest {
  refresh: string
}

export interface RefreshResponse {
  access: string
  refresh: string
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
  new_password_confirm: string
}

export interface Permission {
  id: string
  codename: string
  name: string
  display_name?: string
  description: string
  module: string
  category: string
  is_risk?: boolean
  code?: string
}

export interface Role {
  id: string
  name: string
  display_name: string
  description: string
  is_system: boolean
  created_at?: string
  permissions: Permission[]
}

export interface PermissionOverride {
  id: string
  permission: Permission
  override_type: "allow" | "deny"
}

export interface ResolvedPermissions {
  permissions: string[]
  roles: string[]
  user_group: UserGroup
}
