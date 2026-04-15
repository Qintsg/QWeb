/**
 * API 通用类型定义
 *
 * 与后端 apps/core/responses.py 中的响应格式一一对应。
 */

/** 后端统一成功响应体 */
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

/** 后端统一错误响应体 */
export interface ApiErrorResponse {
  code: number
  message: string
  errors?: Record<string, unknown>
}

/** 后端分页响应体 */
export interface PaginatedResponse<T = unknown> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/** 分页查询参数 */
export interface PaginationParams {
  page?: number
  page_size?: number
}

/** 排序查询参数 */
export interface OrderingParams {
  ordering?: string
}

/** 通用列表查询参数 */
export type ListParams = PaginationParams & OrderingParams & Record<string, unknown>
