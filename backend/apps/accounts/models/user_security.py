"""用户安全信息模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class UserSecurity(models.Model):
    """用户密码、2FA、锁定和最近登录状态。"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="uid",
        related_name="security",
        verbose_name="用户",
    )
    password_hash = models.TextField(
        null=True,
        blank=True,
        verbose_name="密码哈希快照",
    )
    password_algo = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        default="django",
        verbose_name="密码算法",
    )
    password_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="密码更新时间",
    )
    two_factor_enabled = models.BooleanField(
        default=False,
        verbose_name="是否开启二次验证",
    )
    two_factor_secret_enc = models.TextField(
        null=True,
        blank=True,
        verbose_name="加密后的 2FA 密钥",
    )
    failed_login_attempts = models.IntegerField(
        default=0,
        verbose_name="连续登录失败次数",
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="账号锁定到期时间",
    )
    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最后登录时间",
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="最后登录 IP",
    )
    last_login_user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="最后登录设备 UA",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_security"
        verbose_name = "用户安全信息"
        verbose_name_plural = "用户安全信息"

    def __str__(self) -> str:
        return f"{self.user.username} 的安全信息"
