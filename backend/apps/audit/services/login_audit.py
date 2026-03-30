"""登录审计服务。"""

from __future__ import annotations

import logging

from django.http import HttpRequest

from apps.audit.models import LoginLog
from apps.audit.services.audit_service import _extract_client_info

logger = logging.getLogger(__name__)


def log_login(*, user, request: HttpRequest | None = None) -> LoginLog | None:
    """记录登录成功事件。"""
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=user,
            username=user.username,
            action=LoginLog.Action.LOGIN,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception:
        logger.exception("登录日志写入失败: user=%s", user)
        return None


def log_logout(*, user, request: HttpRequest | None = None) -> LoginLog | None:
    """记录登出事件。"""
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=user,
            username=user.username,
            action=LoginLog.Action.LOGOUT,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception:
        logger.exception("登出日志写入失败: user=%s", user)
        return None


def log_login_failed(
    *,
    username: str = "",
    reason: str = "",
    request: HttpRequest | None = None,
) -> LoginLog | None:
    """
    记录登录失败事件。

    Args:
        username: 尝试登录的用户名
        reason: 失败原因（如"密码错误"、"账户已禁用"等）
        request: HTTP 请求对象
    """
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=None,
            username=username,
            action=LoginLog.Action.FAILED,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=reason,
        )
    except Exception:
        logger.exception("登录失败日志写入失败: username=%s", username)
        return None
