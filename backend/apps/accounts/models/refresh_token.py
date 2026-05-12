"""刷新令牌记录模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class UserRefreshToken(models.Model):
    """项目级刷新令牌设备与吊销记录。"""

    id = models.BigAutoField(primary_key=True, verbose_name="令牌记录 ID")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="uid",
        related_name="refresh_tokens",
        verbose_name="用户",
    )
    token_hash = models.TextField(unique=True, verbose_name="刷新令牌哈希")
    device_id = models.CharField(max_length=128, null=True, blank=True, verbose_name="设备 ID")
    device_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="设备名称")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="签发 IP")
    user_agent = models.TextField(null=True, blank=True, verbose_name="客户端 UA")
    expires_at = models.DateTimeField(verbose_name="过期时间")
    revoked_at = models.DateTimeField(null=True, blank=True, verbose_name="吊销时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "user_refresh_tokens"
        verbose_name = "用户刷新令牌"
        verbose_name_plural = "用户刷新令牌"
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["revoked_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} refresh token {self.pk}"
