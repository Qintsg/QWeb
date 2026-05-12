#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户信息服务层。
@Project : QWeb
@File : user_service.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


def update_profile(
    *,
    user: Any,
    data: dict[str, Any],
) -> None:
    """更新用户资料。

    支持同时更新 User 上的 nickname/avatar_url 和 UserProfile 上的字段。

    :param user: 用户实例
    :param data: 包含待更新字段的字典
    """
    # User 模型上可更新的字段
    user_fields = {"nickname", "avatar_url"}
    user_update = {}
    profile_update = {}

    for key, value in data.items():
        if key in user_fields:
            user_update[key] = value
        else:
            profile_update[key] = value

    if user_update:
        for attr, value in user_update.items():
            setattr(user, attr, value)
        user.save(update_fields=[*user_update.keys(), "updated_at"])

    if profile_update:
        profile = user.profile
        for attr, value in profile_update.items():
            setattr(profile, attr, value)
        profile.save(update_fields=list(profile_update.keys()))
