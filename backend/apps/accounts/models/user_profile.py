"""用户资料模型。"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """用户扩展资料。"""

    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        OTHER = "other", "其他"
        UNKNOWN = "unknown", "未知"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="uid",
        related_name="profile",
        verbose_name="用户",
    )
    real_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="真实姓名")
    gender = models.CharField(
        max_length=16,
        choices=Gender.choices,
        null=True,
        blank=True,
        verbose_name="性别",
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    bio = models.TextField(null=True, blank=True, verbose_name="个人简介")
    country = models.CharField(max_length=64, null=True, blank=True, verbose_name="国家")
    province = models.CharField(max_length=64, null=True, blank=True, verbose_name="省份")
    city = models.CharField(max_length=64, null=True, blank=True, verbose_name="城市")
    website = models.TextField(null=True, blank=True, verbose_name="个人网站")
    github = models.TextField(null=True, blank=True, verbose_name="GitHub 主页")
    extra = models.JSONField(default=dict, blank=True, verbose_name="扩展资料")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_profile"
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self) -> str:
        return f"{self.user.username} 的资料"
