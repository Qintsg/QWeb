"""首页服务链接模型。"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class ServiceLink(BaseModel):
    """首页展示的服务链接卡片。"""

    class Category(models.TextChoices):
        PROJECT = "project", "项目展示"
        SERVER = "server", "服务器管理"
        TOOL = "tool", "工具"
        OTHER = "other", "其他"

    title = models.CharField(max_length=100, verbose_name="标题")
    url = models.URLField(max_length=500, verbose_name="链接地址")
    description = models.CharField(max_length=300, blank=True, default="", verbose_name="描述")
    remark = models.CharField(max_length=500, blank=True, default="", verbose_name="备注")
    icon = models.CharField(max_length=50, blank=True, default="", verbose_name="图标标识")
    color = models.CharField(max_length=20, blank=True, default="", verbose_name="主题色")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="分类",
    )
    sort_order = models.IntegerField(default=0, verbose_name="排序权重")
    is_visible = models.BooleanField(default=True, db_index=True, verbose_name="是否可见")

    class Meta:
        db_table = "homepage_service_link"
        ordering = ["sort_order", "created_at"]
        verbose_name = "服务链接"
        verbose_name_plural = "服务链接"

    def __str__(self) -> str:
        return self.title
