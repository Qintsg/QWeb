"""用户查询选择器。

提供统一的用户查询接口，封装 ORM 查询逻辑，
与视图和服务层解耦。
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.core.exceptions import ResourceNotFoundException

User = get_user_model()


def get_user_by_id(user_id: int | str):
    """根据 uid 获取用户。

    Args:
        user_id: 用户 uid

    Returns:
        User 实例

    Raises:
        ResourceNotFoundException: 用户不存在
    """
    try:
        return User.objects.select_related("contact", "profile", "settings").get(pk=user_id)
    except User.DoesNotExist:
        raise ResourceNotFoundException(message="用户不存在")


def get_user_by_email(email: str):
    """根据邮箱获取用户。

    Args:
        email: 用户邮箱

    Returns:
        User 实例

    Raises:
        ResourceNotFoundException: 用户不存在
    """
    try:
        return User.objects.select_related("contact", "profile", "settings").get(
            contact__email__iexact=email
        )
    except User.DoesNotExist:
        raise ResourceNotFoundException(message="用户不存在")


def list_users(
    *,
    is_active: bool | None = None,
    search: str | None = None,
) -> QuerySet:
    """获取用户列表。

    支持按激活状态过滤和关键词搜索。

    Args:
        is_active: 筛选激活状态（None 表示不过滤）
        search: 搜索关键词（匹配用户名、邮箱、显示名称）

    Returns:
        User QuerySet
    """
    qs = User.objects.select_related("contact", "profile", "settings").all()

    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    if search:
        from django.db.models import Q

        qs = qs.filter(
            Q(username__icontains=search)
            | Q(contact__email__icontains=search)
            | Q(contact__phone__icontains=search)
            | Q(nickname__icontains=search)
        )

    return qs
