/**
 * 认证与用户相关类型定义。
 *
 * :project: QWeb
 * :file: auth.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
export interface UserContact {
  email: string | null
  phone: string | null
  email_verified_at: string | null
  phone_verified_at: string | null
}

export interface UserProfile {
  real_name: string | null
  gender: "male" | "female" | "other" | "unknown" | null
  birthday: string | null
  bio: string | null
  country: string | null
  province: string | null
  city: string | null
  website: string | null
  github: string | null
  extra: Record<string, unknown>
}

export interface UserSettings {
  language: string
  timezone: string
  theme: "light" | "dark" | "system"
  notification_settings: Record<string, unknown>
  privacy_settings: Record<string, unknown>
  preferences: Record<string, unknown>
}

export interface UserInfo {
  uid: number
  username: string
  nickname: string | null
  avatar_url: string | null
  status: "active" | "inactive" | "banned" | "deleted" | "pending"
  user_type: "normal" | "admin" | "system"
  is_active: boolean
  is_staff?: boolean
  is_superuser?: boolean
  created_at: string
  updated_at: string
  deleted_at?: string | null
  last_login: string | null
  contact?: UserContact
  profile?: UserProfile
  settings?: UserSettings
}

export type UserGroup = "owner" | "admin" | "trusted" | "user" | "guest"

export interface LoginRequest {
  login: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  password_confirm: string
}

export interface LoginResponse {
  status?: "authenticated"
  user: UserInfo
  access: string
  refresh: string
  redirect?: string
}

export interface OAuthAuthorizeResponse {
  authorization_url: string
  state: string
  provider: string
}

export interface OAuthCallbackRequest {
  code: string
  state: string
}

export interface OAuthChoiceResponse {
  status: "requires_account_choice"
  provider: string
  pending_token: string
  suggested_username: string
  suggested_nickname: string
  provider_email: string
  provider_email_verified: boolean | null
  provider_avatar_url: string
  email_matches_existing_account: boolean
  redirect: string
}

export interface OAuthBindRequest {
  pending_token: string
  login: string
  password: string
}

export interface OAuthRegisterRequest {
  pending_token: string
  username: string
  nickname?: string
}

export type OAuthCallbackResponse = LoginResponse | OAuthChoiceResponse

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
  code?: string
  name: string
  description: string
  module: string
  resource?: string
  action?: string
  is_active?: boolean
}

export interface Role {
  id: string
  name: string
  display_name: string
  description: string
  is_system: boolean
  level?: number
  created_at?: string
  permissions?: Permission[]
}

export interface UserRole {
  id: string
  role: Role
  created_at: string
}

export interface PermissionOverride {
  id: string
  permission: Permission
  effect: "allow" | "deny"
  reason?: string
  created_at?: string
}

export interface ResolvedPermissions {
  permissions: string[]
  roles: string[]
  user_group?: UserGroup
}
