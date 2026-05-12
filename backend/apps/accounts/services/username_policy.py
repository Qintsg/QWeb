"""用户名规则校验。"""

from __future__ import annotations

import re

from django.contrib.auth import get_user_model

from apps.core.exceptions import ValidationException

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|[._-](?![._-])){1,30}[A-Za-z0-9]$")
RESERVED_USERNAMES = {
    "admin",
    "administrator",
    "api",
    "auth",
    "blog",
    "dashboard",
    "help",
    "iam",
    "login",
    "logout",
    "me",
    "null",
    "qintsg",
    "root",
    "settings",
    "signup",
    "static",
    "support",
    "system",
    "user",
    "users",
}


def normalize_username(username: str) -> str:
    """返回去除首尾空白后的用户名。"""
    return username.strip()


def validate_username_policy(username: str, *, current_uid: int | None = None) -> str:
    """校验用户名格式、保留词和大小写不敏感唯一性。"""
    normalized = normalize_username(username)
    if not USERNAME_PATTERN.fullmatch(normalized):
        raise ValidationException(
            message="用户名需为 3-32 位，只能包含字母、数字、短横线、下划线和点号，且不能以特殊字符开头或结尾。",
            errors={"username": ["用户名格式不符合规则"]},
        )

    lowered = normalized.lower()
    if lowered in RESERVED_USERNAMES:
        raise ValidationException(
            message="该用户名为系统保留名称",
            errors={"username": ["该用户名不可使用"]},
        )

    User = get_user_model()
    queryset = User.objects.filter(username__iexact=normalized)
    if current_uid is not None:
        queryset = queryset.exclude(pk=current_uid)
    if queryset.exists():
        raise ValidationException(
            message="该用户名已被注册",
            errors={"username": ["该用户名已被注册"]},
        )
    return normalized


def is_username_available(username: str) -> bool:
    """判断用户名是否符合规则且未被占用。"""
    try:
        validate_username_policy(username)
    except ValidationException:
        return False
    return True
