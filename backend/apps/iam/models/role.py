"""角色模型。

预置角色：owner / admin / trusted / user / guest
level 值越小权限等级越高，用于角色排序和对比。
"""

from django.db import models

from apps.core.models.base import BaseModel


class Role(BaseModel):
    """角色定义。

    角色是权限的集合，按职责分配给用户。
    系统预置角色可修改权限配置但不可删除。
    """

    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="角色名",
        help_text="唯一标识，如 owner、admin、user",
    )
    display_name = models.CharField(
        max_length=128,
        verbose_name="显示名称",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="描述",
    )
    is_system = models.BooleanField(
        default=False,
        verbose_name="是否系统预置",
        help_text="系统预置角色不可删除",
    )
    level = models.IntegerField(
        default=100,
        verbose_name="权限等级",
        help_text="值越小权限越高。owner=0, admin=10, trusted=30, user=50, guest=90",
    )

    class Meta:
        db_table = "iam_role"
        verbose_name = "角色"
        verbose_name_plural = "角色"
        ordering = ["level", "name"]

    def __str__(self) -> str:
        return f"{self.display_name} ({self.name})"
