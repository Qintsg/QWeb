"""用户资料模型。

存储用户的扩展信息，与 User 模型一对一关联。
注册时自动创建空资料记录。
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class UserProfile(BaseModel):
    """用户资料扩展。

    字段说明：
    - user: 关联用户（一对一）
    - avatar: 头像 URL
    - bio: 个人简介
    - phone: 手机号
    - timezone: 用户时区
    - language: 首选语言
    - theme_preference: 主题偏好（light/dark/auto）
    """

    THEME_CHOICES = [
        ("light", "浅色"),
        ("dark", "深色"),
        ("auto", "跟随系统"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="关联用户",
    )
    avatar = models.URLField(
        blank=True,
        default="",
        verbose_name="头像",
        help_text="头像图片 URL。",
    )
    bio = models.TextField(
        blank=True,
        default="",
        max_length=500,
        verbose_name="个人简介",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="手机号",
    )
    timezone = models.CharField(
        max_length=50,
        default="Asia/Shanghai",
        verbose_name="时区",
    )
    language = models.CharField(
        max_length=10,
        default="zh-hans",
        verbose_name="首选语言",
        help_text="IETF 语言标签，如 zh-hans、en-us。",
    )
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default="auto",
        verbose_name="主题偏好",
    )

    class Meta:
        db_table = "accounts_user_profile"
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self) -> str:
        return f"{self.user.username} 的资料"
