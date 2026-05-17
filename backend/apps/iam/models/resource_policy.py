#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
资源级策略模型。
@Project : QWeb
@File : resource_policy.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.db import models

from apps.core.models.base import BaseModel


class ResourcePolicy(BaseModel):
    """资源级策略。

    对特定资源实例（resource_type + resource_id）设置
    针对特定主体（subject_type + subject_id）的权限策略。
    """

    class SubjectType(models.TextChoices):
        """定义当前字段的可选枚举值。"""
        USER = "user", "用户"
        ROLE = "role", "角色"

    class Effect(models.TextChoices):
        """定义当前字段的可选枚举值。"""
        ALLOW = "allow", "允许"
        DENY = "deny", "拒绝"

    resource_type = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name="资源类型",
        help_text="如 blog_post、wiki_page",
    )
    resource_id = models.UUIDField(
        db_index=True,
        verbose_name="资源 ID",
    )
    subject_type = models.CharField(
        max_length=16,
        choices=SubjectType.choices,
        verbose_name="主体类型",
    )
    subject_id = models.CharField(
        max_length=64,
        verbose_name="主体 ID",
        help_text="用户 uid 或角色 UUID",
    )
    permission = models.ForeignKey(
        "iam.Permission",
        on_delete=models.CASCADE,
        related_name="resource_policies",
        verbose_name="权限",
    )
    effect = models.CharField(
        max_length=8,
        choices=Effect.choices,
        verbose_name="效果",
    )

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "iam_resource_policy"
        verbose_name = "资源策略"
        verbose_name_plural = "资源策略"
        indexes = [
            models.Index(
                fields=["resource_type", "resource_id"],
                name="idx_resource_policy_resource",
            ),
            models.Index(
                fields=["subject_type", "subject_id"],
                name="idx_resource_policy_subject",
            ),
        ]

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        return f"{self.resource_type}:{self.resource_id} -> {self.subject_type}:{self.subject_id}"
