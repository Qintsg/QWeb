"""用户权限覆盖模型。

在角色权限基础上，对个别用户做 allow/deny 级别的精确控制。
deny 优先于 allow（黑名单优先原则）。
"""

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel


class UserPermissionOverride(BaseModel):
    """用户权限覆盖记录。

    允许对某个用户额外授予或拒绝特定权限，
    不受其角色配置的影响。
    """

    class Effect(models.TextChoices):
        ALLOW = "allow", "允许"
        DENY = "deny", "拒绝"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="permission_overrides",
        verbose_name="用户",
    )
    permission = models.ForeignKey(
        "iam.Permission",
        on_delete=models.CASCADE,
        related_name="user_overrides",
        verbose_name="权限",
    )
    effect = models.CharField(
        max_length=8,
        choices=Effect.choices,
        verbose_name="效果",
        help_text="allow=额外授予, deny=额外拒绝",
    )
    reason = models.TextField(
        blank=True,
        default="",
        verbose_name="覆盖原因",
        help_text="为什么对此用户进行权限覆盖",
    )

    class Meta:
        db_table = "iam_user_permission_override"
        verbose_name = "用户权限覆盖"
        verbose_name_plural = "用户权限覆盖"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "permission"],
                name="uq_user_permission_override",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} {self.effect} {self.permission_id}"
