#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
刷新令牌签发、记录与吊销服务。
@Project : QWeb
@File : token_service.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import UserRefreshToken


def issue_token_pair(*, user: Any, request: HttpRequest | None = None) -> dict[str, str]:
    """签发 JWT token 对，并记录项目级 refresh token 哈希。"""
    refresh = RefreshToken.for_user(user)
    refresh_token = str(refresh)
    record_refresh_token(user=user, refresh_token=refresh_token, request=request)
    return {
        "access": str(refresh.access_token),
        "refresh": refresh_token,
    }


def record_refresh_token(*, user: Any, refresh_token: str, request: HttpRequest | None = None) -> UserRefreshToken | None:
    """记录 refresh token 哈希、设备和过期时间，不保存明文令牌。"""
    try:
        token = RefreshToken(refresh_token, verify=False)
        expires_at = _expires_at_from_token(token)
    except TokenError:
        return None

    ip_address, user_agent = _extract_request_client(request)
    device_id = _get_header(request, "HTTP_X_DEVICE_ID")
    device_name = _get_header(request, "HTTP_X_DEVICE_NAME")

    token_record, _ = UserRefreshToken.objects.update_or_create(
        token_hash=hash_refresh_token(refresh_token),
        defaults={
            "user": user,
            "device_id": device_id or None,
            "device_name": device_name or None,
            "ip": ip_address or None,
            "user_agent": user_agent,
            "expires_at": expires_at,
            "revoked_at": None,
        },
    )
    return token_record


def revoke_refresh_token(*, refresh_token: str) -> int:
    """按 refresh token 明文计算哈希并标记吊销。"""
    return UserRefreshToken.objects.filter(
        token_hash=hash_refresh_token(refresh_token),
        revoked_at__isnull=True,
    ).update(revoked_at=timezone.now())


def record_rotated_refresh_token(
    *,
    old_refresh_token: str,
    new_refresh_token: str | None,
    user: Any | None = None,
    request: HttpRequest | None = None,
) -> None:
    """Token refresh 成功后吊销旧记录，并记录轮换后的新 refresh token。"""
    if user is None:
        user = get_user_from_refresh_token(old_refresh_token, verify=False)
    revoke_refresh_token(refresh_token=old_refresh_token)
    if user is not None and new_refresh_token:
        record_refresh_token(user=user, refresh_token=new_refresh_token, request=request)


def get_user_from_refresh_token(refresh_token: str, *, verify: bool = True) -> Any | None:
    """从 refresh token 中解析本地用户。"""
    try:
        token = RefreshToken(refresh_token, verify=verify)
    except TokenError:
        return None

    user_id = token.payload.get("user_id")
    if user_id is None:
        return None

    User = get_user_model()
    return User.objects.filter(pk=user_id).first()


def hash_refresh_token(refresh_token: str) -> str:
    """返回 refresh token 的稳定 SHA-256 哈希。"""
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def _expires_at_from_token(token: RefreshToken) -> datetime:
    """解析令牌过期时间。"""
    expires_at = token.payload.get("exp")
    if not isinstance(expires_at, int):
        return timezone.now()
    return datetime.fromtimestamp(expires_at, tz=UTC)


def _extract_request_client(request: HttpRequest | None) -> tuple[str, str]:
    """提取请求中的客户端上下文。"""
    if request is None:
        return "", ""
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
    if ip_address and "," in ip_address:
        ip_address = ip_address.split(",", 1)[0].strip()
    return ip_address, request.META.get("HTTP_USER_AGENT", "")


def _get_header(request: HttpRequest | None, key: str) -> str:
    """读取当前流程所需的业务对象。"""
    if request is None:
        return ""
    value: Any = request.META.get(key, "")
    return str(value).strip()
