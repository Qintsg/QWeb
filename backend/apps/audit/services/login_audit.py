#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
登录审计服务。
@Project : QWeb
@File : login_audit.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

import logging
from typing import Any

from django.http import HttpRequest

from apps.audit.models import LoginLog
from apps.audit.services.audit_service import _extract_client_info

logger = logging.getLogger(__name__)


def log_login(*, user: Any, request: HttpRequest | None = None) -> LoginLog | None:
    """记录登录成功事件。"""
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=user,
            username=user.username,
            login_type="password",
            action=LoginLog.Action.LOGIN,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
        )
    except Exception:
        logger.exception("登录日志写入失败: user=%s", user)
        return None


def log_oauth_login(
    *,
    user: Any,
    provider: str,
    request: HttpRequest | None = None,
    action: str = LoginLog.Action.LOGIN,
) -> LoginLog | None:
    """记录 OAuth 登录、绑定或自动注册事件。"""
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=user,
            username=user.username,
            login_type="oauth",
            provider=provider,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
        )
    except Exception:
        logger.exception("OAuth 登录日志写入失败: user=%s provider=%s", user, provider)
        return None


def log_logout(*, user: Any, request: HttpRequest | None = None) -> LoginLog | None:
    """记录登出事件。"""
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=user,
            username=user.username,
            login_type="token",
            action=LoginLog.Action.LOGOUT,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
        )
    except Exception:
        logger.exception("登出日志写入失败: user=%s", user)
        return None


def log_login_failed(
    *,
    username: str = "",
    reason: str = "",
    request: HttpRequest | None = None,
    login_type: str = "password",
    provider: str | None = None,
) -> LoginLog | None:
    """
    记录登录失败事件。

    :param username: 尝试登录的用户名
    :param reason: 失败原因（如"密码错误"、"账户已禁用"等）
    :param request: HTTP 请求对象
    """
    ip_address, user_agent = _extract_client_info(request)
    try:
        return LoginLog.objects.create(
            user=None,
            username=username,
            login_type=login_type,
            provider=provider,
            action=LoginLog.Action.FAILED,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            failure_reason=reason,
        )
    except Exception:
        logger.exception("登录失败日志写入失败: username=%s", username)
        return None
