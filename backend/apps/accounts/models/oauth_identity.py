"""第三方 OAuth 身份绑定模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class OAuthIdentity(BaseModel):
    """外部 OAuth 账号与本地用户的绑定关系。"""

    class Provider(models.TextChoices):
        GITHUB = "github", "GitHub"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="oauth_identities",
        verbose_name="本地用户",
    )
    provider = models.CharField(
        max_length=32,
        choices=Provider.choices,
        db_index=True,
        verbose_name="OAuth 提供方",
    )
    provider_user_id = models.CharField(
        max_length=128,
        verbose_name="提供方用户 ID",
    )
    provider_username = models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="提供方用户名",
    )
    email = models.EmailField(
        blank=True,
        default="",
        verbose_name="提供方邮箱",
    )
    avatar_url = models.URLField(
        blank=True,
        default="",
        verbose_name="头像 URL",
    )
    profile_url = models.URLField(
        blank=True,
        default="",
        verbose_name="资料页 URL",
    )
    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最近登录时间",
    )

    class Meta:
        db_table = "accounts_oauth_identity"
        verbose_name = "OAuth 身份绑定"
        verbose_name_plural = "OAuth 身份绑定"
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_user_id"],
                name="uniq_oauth_provider_user",
            ),
            models.UniqueConstraint(
                fields=["provider", "user"],
                name="uniq_oauth_provider_local_user",
            ),
        ]
        indexes = [
            models.Index(fields=["provider", "provider_username"]),
            models.Index(fields=["provider", "email"]),
        ]

    def __str__(self) -> str:
        return f"{self.provider}:{self.provider_username or self.provider_user_id}"
