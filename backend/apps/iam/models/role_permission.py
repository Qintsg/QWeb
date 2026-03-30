"""角色-权限关联模型。"""

from django.db import models

from apps.core.models.base import BaseModel


class RolePermission(BaseModel):
    """角色与权限的多对多关联。

    一个角色可以拥有多个权限，一个权限也可以被多个角色使用。
    """

    role = models.ForeignKey(
        "iam.Role",
        on_delete=models.CASCADE,
        related_name="role_permissions",
        verbose_name="角色",
    )
    permission = models.ForeignKey(
        "iam.Permission",
        on_delete=models.CASCADE,
        related_name="role_permissions",
        verbose_name="权限",
    )

    class Meta:
        db_table = "iam_role_permission"
        verbose_name = "角色权限"
        verbose_name_plural = "角色权限"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="uq_role_permission",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.role_id} -> {self.permission_id}"
