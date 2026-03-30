/**
 * 审计日志 API
 *
 * 对应后端 apps/audit/api/views.py
 * 路由前缀：/api/v1/
 */
import apiClient from "./client"
import type { ApiResponse, PaginatedResponse, ListParams } from "@/types/api"

/** 操作审计日志 */
export interface AuditLog {
  id: string
  user: string | null
  username: string
  action: string
  module: string
  target_type: string
  target_id: string | null
  description: string
  ip_address: string | null
  user_agent: string
  extra_data: Record<string, unknown>
  created_at: string
}

/** 登录审计日志 */
export interface LoginLog {
  id: string
  user: string | null
  username: string
  action: "login_success" | "login_failed" | "logout" | "token_refresh"
  ip_address: string | null
  user_agent: string
  location: string
  extra_data: Record<string, unknown>
  created_at: string
}

/** 审计日志查询参数 */
export interface AuditLogQuery extends ListParams {
  search?: string
  action?: string
  module?: string
  user?: string
  created_at_after?: string
  created_at_before?: string
}

/** 登录日志查询参数 */
export interface LoginLogQuery extends ListParams {
  search?: string
  action?: string
  user?: string
  created_at_after?: string
  created_at_before?: string
}

/** 获取操作审计日志列表 */
export function getAuditLogs(params?: AuditLogQuery) {
  return apiClient.get<ApiResponse<PaginatedResponse<AuditLog>>>("/logs/", { params })
}

/** 获取登录审计日志列表 */
export function getLoginLogs(params?: LoginLogQuery) {
  return apiClient.get<ApiResponse<PaginatedResponse<LoginLog>>>("/login-logs/", { params })
}
