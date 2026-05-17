#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
基础抽象模型。
@Project : QWeb
@File : base.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class BaseQuerySet(models.QuerySet):
    """默认排除已软删除记录的查询集。"""

    def active(self) -> BaseQuerySet:
        """仅返回未被软删除的记录。"""
        return self.filter(is_deleted=False)

    def deleted(self) -> BaseQuerySet:
        """仅返回已被软删除的记录。"""
        return self.filter(is_deleted=True)


class BaseManager(models.Manager):
    """默认管理器，查询时自动排除软删除记录。"""

    def get_queryset(self) -> BaseQuerySet:
        """构造当前请求使用的查询集。"""
        return BaseQuerySet(self.model, using=self._db).active()

    def all_with_deleted(self) -> BaseQuerySet:
        """返回包含软删除记录在内的全部记录。"""
        return BaseQuerySet(self.model, using=self._db)

    def deleted_only(self) -> BaseQuerySet:
        """仅返回已软删除的记录。"""
        return BaseQuerySet(self.model, using=self._db).deleted()


class BaseModel(models.Model):
    """全局抽象基类。

    提供以下通用字段：
    - id: UUID 主键
    - created_at / updated_at: 自动时间戳
    - is_deleted: 软删除标记
    - created_by / updated_by: 操作人外键（可选）
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="是否已删除",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name="创建人",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name="更新人",
    )

    objects = BaseManager()

    class Meta:
        """定义当前对象的 Django 元数据。"""
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self) -> None:
        """软删除：仅设置 is_deleted 标记，不物理删除。"""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])

    def restore(self) -> None:
        """恢复软删除的记录。"""
        self.is_deleted = False
        self.save(update_fields=["is_deleted", "updated_at"])
