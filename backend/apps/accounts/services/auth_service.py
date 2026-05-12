"""认证服务层。

包含用户注册、认证等核心业务逻辑，
与视图层解耦，便于测试和复用。
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.accounts.models import UserContact, UserSecurity
from apps.accounts.services.account_bootstrap import ensure_user_related_records
from apps.accounts.services.token_service import issue_token_pair
from apps.accounts.services.username_policy import validate_username_policy
from apps.audit.services.audit_service import log_action
from apps.audit.services.login_audit import log_login, log_login_failed
from apps.core.exceptions import (
    AuthenticationFailedException,
    ValidationException,
)

User = get_user_model()


@transaction.atomic
def register_user(
    *,
    username: str,
    email: str,
    password: str,
    request=None,
) -> dict[str, Any]:
    """注册新用户并生成 JWT Token。

    流程：
    1. 创建 User 记录
    2. 自动创建 UserProfile
    3. 生成 JWT Token 对

    Args:
        username: 用户名
        email: 邮箱
        password: 明文密码（将被哈希存储）
        request: HTTP 请求对象（用于审计）

    Returns:
        包含 user、access、refresh 的字典
    """
    username = validate_username_policy(username)
    email = email.strip() if email else ""
    if email and UserContact.objects.filter(email__iexact=email).exists():
        raise ValidationException(message="该邮箱已被注册", errors={"email": ["该邮箱已被注册"]})

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    ensure_user_related_records(user=user, email=email)

    # 审计：记录注册
    log_action(
        user=user,
        action="create",
        module="accounts",
        resource="user",
        resource_id=str(user.uid),
        detail={"username": username, "email": email},
        request=request,
    )

    tokens = issue_token_pair(user=user, request=request)
    return {
        "user": user,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


def authenticate_user(
    *,
    login: str,
    password: str,
    request=None,
) -> dict[str, Any]:
    """认证用户并返回 JWT Token。

    支持用户名或邮箱登录。

    Args:
        login: 用户名或邮箱
        password: 密码
        request: HTTP 请求对象（用于审计）

    Returns:
        包含 user、access、refresh 的字典

    Raises:
        AuthenticationFailedException: 凭据无效或账号被禁用
    """
    login_identifier = login.strip()
    user = (
        User.objects.filter(
            Q(username__iexact=login_identifier)
            | Q(contact__email__iexact=login_identifier)
            | Q(contact__phone=login_identifier)
        )
        .select_related("contact", "security")
        .first()
    )

    if user is None or not user.check_password(password):
        log_login_failed(username=login_identifier, reason="账号或密码错误", request=request)
        raise AuthenticationFailedException(message="账号或密码错误")

    _ensure_user_can_login(user=user, login_identifier=login_identifier, request=request)

    # 审计：记录登录成功
    log_login(user=user, request=request)
    _record_login_success(user=user, request=request)

    tokens = issue_token_pair(user=user, request=request)
    return {
        "user": user,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


def change_password(
    *,
    user,
    old_password: str,
    new_password: str,
    request=None,
) -> None:
    """修改用户密码。

    Args:
        user: 当前用户实例
        old_password: 旧密码
        new_password: 新密码
        request: HTTP 请求对象（用于审计）

    Raises:
        ValidationException: 旧密码不正确
    """
    if user.has_usable_password() and not user.check_password(old_password):
        raise ValidationException(message="当前密码不正确")

    user.set_password(new_password)
    user.save(update_fields=["password", "updated_at"])
    UserSecurity.objects.update_or_create(
        user=user,
        defaults={
            "password_hash": user.password,
            "password_algo": "django",
            "password_updated_at": timezone.now(),
        },
    )

    # 审计：记录密码修改
    log_action(
        user=user,
        action="update",
        module="accounts",
        resource="password",
        resource_id=str(user.uid),
        request=request,
    )


def _ensure_user_can_login(*, user, login_identifier: str, request=None) -> None:
    if not user.is_active or user.status != User.Status.ACTIVE:
        log_login_failed(username=login_identifier, reason="账号不可用", request=request)
        raise AuthenticationFailedException(message="账号已被禁用或不可用，请联系管理员")

    security = getattr(user, "security", None)
    if security and security.locked_until and security.locked_until > timezone.now():
        log_login_failed(username=login_identifier, reason="账号临时锁定", request=request)
        raise AuthenticationFailedException(message="账号临时锁定，请稍后再试")


def _record_login_success(*, user, request=None) -> None:
    ip_address = None
    user_agent = ""
    if request:
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        if ip_address and "," in ip_address:
            ip_address = ip_address.split(",")[0].strip()
        user_agent = request.META.get("HTTP_USER_AGENT", "")

    UserSecurity.objects.update_or_create(
        user=user,
        defaults={
            "failed_login_attempts": 0,
            "locked_until": None,
            "last_login_at": timezone.now(),
            "last_login_ip": ip_address or None,
            "last_login_user_agent": user_agent,
        },
    )
