/**
 * 首页服务链接 API。
 *
 * :project: QWeb
 * :file: homepage.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import apiClient from './client'
import type { ApiResponse } from '@/types/api'
import type { AxiosResponse } from 'axios'

export interface ServiceLink {
  id: string
  title: string
  url: string
  description: string
  remark: string
  icon: string
  color: string
  category: 'project' | 'server' | 'tool' | 'other'
  sort_order: number
}

export interface ServiceLinkAdmin extends ServiceLink {
  is_visible: boolean
  created_at: string
  updated_at: string
}

export type ServiceLinkCreatePayload = Omit<ServiceLinkAdmin, 'id' | 'created_at' | 'updated_at'>

/** 公开接口：获取可见的服务链接列表 */
export function getPublicServiceLinks(): Promise<AxiosResponse<ApiResponse<ServiceLink[]>>> {
  return apiClient.get('/homepage/links/')
}

/** 管理接口：获取全部服务链接 */
export function getAdminServiceLinks(): Promise<AxiosResponse<ApiResponse<ServiceLinkAdmin[]>>> {
  return apiClient.get('/homepage/admin/links/')
}

/** 管理接口：创建服务链接 */
export function createServiceLink(data: ServiceLinkCreatePayload): Promise<AxiosResponse<ApiResponse<ServiceLinkAdmin>>> {
  return apiClient.post('/homepage/admin/links/', data)
}

/** 管理接口：更新服务链接 */
export function updateServiceLink(id: string, data: Partial<ServiceLinkCreatePayload>): Promise<AxiosResponse<ApiResponse<ServiceLinkAdmin>>> {
  return apiClient.patch(`/homepage/admin/links/${id}/`, data)
}

/** 管理接口：删除服务链接 */
export function deleteServiceLink(id: string): Promise<AxiosResponse<ApiResponse<null>>> {
  return apiClient.delete(`/homepage/admin/links/${id}/`)
}
