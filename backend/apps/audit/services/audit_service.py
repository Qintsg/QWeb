#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
通用操作审计服务。
@Project : QWeb
@File : audit_service.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

import logging
from typing import Any

from django.http import HttpRequest

from apps.audit.models import AuditLog

logger = logging.getLogger(__name__)


def _extract_client_info(request: HttpRequest | None) -> tuple[str | None, str]:
    """从请求中提取客户端 IP 和 User-Agent。"""
    if request is None:
        return None, ""

    # 优先从 X-Forwarded-For 获取真实 IP（反向代理场景）
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        ip_address = xff.split(",")[0].strip()
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    return ip_address, user_agent


def log_action(
    *,
    user: Any,
    action: str,
    module: str,
    resource: str,
    resource_id: str = "",
    detail: dict[str, Any] | None = None,
    request: HttpRequest | None = None,
) -> AuditLog | None:
    """
    写入一条操作审计日志。

    这是审计模块的统一写入入口，所有业务模块通过此函数记录操作日志。

    :param user: 操作人（User 实例或 None）
    :param action: 操作类型（create/update/delete 等）
    :param module: 模块名称（accounts/iam/blog 等）
    :param resource: 资源类型（user/role/permission 等）
    :param resource_id: 资源标识符
    :param detail: 变更详情（JSON 格式）
    :param request: HTTP 请求对象（用于提取 IP 和 User-Agent）
    """
    ip_address, user_agent = _extract_client_info(request)

    try:
        return AuditLog.objects.create(
            user=user,
            action=action,
            module=module,
            resource=resource,
            resource_id=str(resource_id) if resource_id else "",
            detail=detail or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception:
        # 审计写入失败不应影响主业务流程，仅记录日志
        logger.exception("审计日志写入失败: action=%s module=%s resource=%s", action, module, resource)
        return None
