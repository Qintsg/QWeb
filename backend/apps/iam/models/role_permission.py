#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
角色-权限关联模型。
@Project : QWeb
@File : role_permission.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
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
        """定义当前对象的 Django 元数据。"""
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
        """返回对象的可读显示名称。"""
        return f"{self.role_id} -> {self.permission_id}"
