#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
账号关联表初始化工具。
@Project : QWeb
@File : account_bootstrap.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from django.utils import timezone

from apps.accounts.models import UserContact, UserProfile, UserSecurity, UserSettings


def ensure_user_related_records(
    *,
    user: Any,
    email: str = "",
    email_verified: bool = False,
    phone: str = "",
) -> None:
    """确保用户一对一扩展表存在。"""
    contact_defaults = {}
    if email:
        contact_defaults["email"] = email
    if phone:
        contact_defaults["phone"] = phone
    if email and email_verified:
        contact_defaults["email_verified_at"] = timezone.now()

    UserContact.objects.update_or_create(user=user, defaults=contact_defaults)
    UserSecurity.objects.update_or_create(
        user=user,
        defaults={
            "password_hash": user.password if user.has_usable_password() else None,
            "password_algo": "django" if user.has_usable_password() else None,
            "password_updated_at": timezone.now() if user.has_usable_password() else None,
        },
    )
    UserProfile.objects.get_or_create(user=user)
    UserSettings.objects.get_or_create(user=user)
