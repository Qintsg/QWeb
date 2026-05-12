#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户核心模型。
@Project : QWeb
@File : user.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """系统用户核心账号。"""

    class Status(models.TextChoices):
        """定义当前字段的可选枚举值。"""
        ACTIVE = "active", "正常"
        INACTIVE = "inactive", "未激活"
        BANNED = "banned", "已封禁"
        DELETED = "deleted", "已删除"
        PENDING = "pending", "待确认"

    class UserType(models.TextChoices):
        """定义当前字段的可选枚举值。"""
        NORMAL = "normal", "普通用户"
        ADMIN = "admin", "管理员"
        SYSTEM = "system", "系统用户"

    uid = models.BigAutoField(
        primary_key=True,
        verbose_name="用户 UID",
    )
    username = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name="用户名",
        help_text="3-32 个字符，允许字母、数字、短横线、下划线和点号。",
    )
    nickname = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="展示昵称",
    )
    avatar_url = models.TextField(
        null=True,
        blank=True,
        verbose_name="头像 URL",
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name="账号状态",
    )
    user_type = models.CharField(
        max_length=32,
        choices=UserType.choices,
        default=UserType.NORMAL,
        db_index=True,
        verbose_name="用户类型",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Django 认证是否启用",
        help_text="与 status 一起用于 Django 认证框架判断。",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="管理后台权限",
        help_text="允许访问 Django Admin 后台。",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="软删除时间",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                Lower("username"),
                name="uq_users_username_ci",
            ),
        ]

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        return self.nickname or self.username

    @property
    def name(self) -> str:
        """返回用于前端显示的友好名称。"""
        return self.nickname or self.username

    @property
    def date_joined(self) -> datetime:
        """兼容 Django Admin 和现有前端字段名。"""
        return self.created_at
