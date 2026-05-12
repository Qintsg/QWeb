#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户管理器。
@Project : QWeb
@File : managers.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """自定义用户管理器。"""

    def create_user(
        self,
        username: str,
        email: str = "",
        password: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        """创建普通用户，并在提供邮箱时同步联系方式表。"""
        if not username:
            raise ValueError("用户名不能为空")

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        normalized_email = self.normalize_email(email) if email else ""
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if normalized_email:
            from apps.accounts.models import UserContact

            UserContact.objects.update_or_create(
                user=user,
                defaults={"email": normalized_email},
            )
        return user

    def create_superuser(
        self,
        username: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        """创建超级管理员。

        自动设置 is_staff=True, is_superuser=True, is_active=True。
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级管理员必须设置 is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级管理员必须设置 is_superuser=True")

        email = extra_fields.pop("email", "")
        return self.create_user(username, email=email, password=password, **extra_fields)
