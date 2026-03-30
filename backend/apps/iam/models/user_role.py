"""用户-角色关联模型。"""

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel


class UserRole(BaseModel):
    """用户与角色的多对多关联。

    一个用户可以拥有多个角色，最终权限为所有角色权限的并集。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name="用户",
    )
    role = models.ForeignKey(
        "iam.Role",
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name="角色",
    )

    class Meta:
        db_table = "iam_user_role"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="uq_user_role",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} -> {self.role_id}"
