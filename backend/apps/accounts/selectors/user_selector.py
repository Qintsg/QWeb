#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户查询选择器。
@Project : QWeb
@File : user_selector.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.core.exceptions import ResourceNotFoundException

User = get_user_model()


def get_user_by_id(user_id: int | str) -> Any:
    """根据 uid 获取用户。

    :param user_id: 用户 uid

    :return: User 实例

    :raises ResourceNotFoundException: 用户不存在
    """
    try:
        return User.objects.select_related("contact", "profile", "settings").get(pk=user_id)
    except User.DoesNotExist:
        raise ResourceNotFoundException(message="用户不存在")


def get_user_by_email(email: str) -> Any:
    """根据邮箱获取用户。

    :param email: 用户邮箱

    :return: User 实例

    :raises ResourceNotFoundException: 用户不存在
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

    :param is_active: 筛选激活状态（None 表示不过滤）
    :param search: 搜索关键词（匹配用户名、邮箱、显示名称）

    :return: User QuerySet
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
