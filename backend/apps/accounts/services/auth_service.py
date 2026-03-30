"""认证服务层。

包含用户注册、认证等核心业务逻辑，
与视图层解耦，便于测试和复用。
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import UserProfile
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
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    # 自动创建空资料
    UserProfile.objects.create(user=user)

    # 审计：记录注册
    log_action(
        user=user,
        action="create",
        module="accounts",
        resource="user",
        resource_id=str(user.pk),
        detail={"username": username, "email": email},
        request=request,
    )

    # 生成 JWT Token
    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
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
    # 同时匹配用户名和邮箱
    user = User.objects.filter(
        Q(username=login) | Q(email=login)
    ).first()

    if user is None or not user.check_password(password):
        log_login_failed(username=login, reason="用户名/邮箱或密码错误", request=request)
        raise AuthenticationFailedException(message="用户名/邮箱或密码错误")

    if not user.is_active:
        log_login_failed(username=login, reason="账号已被禁用", request=request)
        raise AuthenticationFailedException(message="账号已被禁用，请联系管理员")

    # 审计：记录登录成功
    log_login(user=user, request=request)

    # 生成 JWT Token
    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
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
    if not user.check_password(old_password):
        raise ValidationException(message="当前密码不正确")

    user.set_password(new_password)
    user.save(update_fields=["password"])

    # 审计：记录密码修改
    log_action(
        user=user,
        action="update",
        module="accounts",
        resource="password",
        resource_id=str(user.pk),
        request=request,
    )
