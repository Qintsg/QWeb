"""自定义用户模型。

使用 UUID 主键，继承 AbstractBaseUser + PermissionsMixin，
支持用户名 + 邮箱双重唯一标识。
"""

from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """自定义用户模型。

    字段说明：
    - id: UUID 主键
    - username: 用户名，唯一
    - email: 邮箱，唯一
    - display_name: 显示名称（可选）
    - is_active: 是否激活
    - is_staff: 是否允许访问管理后台
    - date_joined: 注册时间
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="用户 ID",
    )
    username = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="用户名",
        help_text="3-64 个字符，仅限字母、数字、下划线。",
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name="邮箱",
    )
    display_name = models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="显示名称",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否激活",
        help_text="未激活的用户无法登录。",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="管理后台权限",
        help_text="允许访问 Django Admin 后台。",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="注册时间",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.display_name or self.username

    @property
    def name(self) -> str:
        """返回用于前端显示的友好名称。"""
        return self.display_name or self.username
