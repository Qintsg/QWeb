#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
权限定义模型。
@Project : QWeb
@File : permission.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.db import models

from apps.core.models.base import BaseModel


class Permission(BaseModel):
    """权限定义。

    每条权限代表系统中一个可控制的操作。
    权限码全局唯一，采用 module.resource.action 格式。
    """

    code = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        verbose_name="权限码",
        help_text="格式: module.resource.action",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="显示名称",
    )
    module = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name="所属模块",
        help_text="如 blog、ssh、iam",
    )
    resource = models.CharField(
        max_length=64,
        verbose_name="资源类型",
        help_text="如 post、host、role",
    )
    action = models.CharField(
        max_length=64,
        verbose_name="操作类型",
        help_text="如 create、read、update、delete",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="描述",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否启用",
    )

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "iam_permission"
        verbose_name = "权限"
        verbose_name_plural = "权限"
        ordering = ["module", "resource", "action"]

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        return f"{self.code} ({self.name})"
