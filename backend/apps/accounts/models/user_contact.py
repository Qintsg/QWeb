"""用户联系方式模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower


class UserContact(models.Model):
    """邮箱和手机号等可登录联系方式。"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="uid",
        related_name="contact",
        verbose_name="用户",
    )
    email = models.EmailField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="邮箱",
    )
    phone = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        unique=True,
        verbose_name="手机号",
    )
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="邮箱验证时间",
    )
    phone_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="手机号验证时间",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_contact"
        verbose_name = "用户联系方式"
        verbose_name_plural = "用户联系方式"
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                condition=Q(email__isnull=False),
                name="uq_user_contact_email_ci",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} 的联系方式"
