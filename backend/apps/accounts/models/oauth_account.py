"""第三方账号绑定模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class UserOAuthAccount(models.Model):
    """外部 OAuth 账号与本地用户的绑定关系。"""

    class Provider(models.TextChoices):
        GITHUB = "github", "GitHub"

    id = models.BigAutoField(primary_key=True, verbose_name="绑定记录 ID")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="uid",
        related_name="oauth_accounts",
        verbose_name="本地用户",
    )
    provider = models.CharField(
        max_length=64,
        choices=Provider.choices,
        db_index=True,
        verbose_name="第三方平台",
    )
    provider_account_id = models.CharField(
        max_length=255,
        verbose_name="第三方平台用户 ID",
    )
    provider_username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="第三方平台用户名",
    )
    provider_nickname = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="第三方平台显示名称",
    )
    provider_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="第三方平台邮箱",
    )
    provider_email_verified = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="第三方平台邮箱是否已验证",
    )
    provider_avatar_url = models.TextField(
        null=True,
        blank=True,
        verbose_name="第三方平台头像",
    )
    access_token_enc = models.TextField(
        null=True,
        blank=True,
        verbose_name="加密后的访问令牌",
    )
    refresh_token_enc = models.TextField(
        null=True,
        blank=True,
        verbose_name="加密后的刷新令牌",
    )
    token_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="令牌过期时间",
    )
    scopes = models.JSONField(
        null=True,
        blank=True,
        verbose_name="授权范围",
    )
    raw_profile = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="第三方原始用户信息",
    )
    linked_at = models.DateTimeField(auto_now_add=True, verbose_name="绑定时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_oauth_accounts"
        verbose_name = "第三方账号绑定"
        verbose_name_plural = "第三方账号绑定"
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_account_id"],
                name="uq_oauth_provider_account",
            ),
            models.UniqueConstraint(
                fields=["user", "provider"],
                name="uq_oauth_user_provider",
            ),
        ]
        indexes = [
            models.Index(fields=["provider", "provider_username"]),
            models.Index(fields=["provider", "provider_email"]),
        ]

    def __str__(self) -> str:
        account_name = self.provider_username or self.provider_account_id
        return f"{self.provider}:{account_name}"
