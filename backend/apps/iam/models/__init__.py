#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
IAM 数据模型。
@Project : QWeb
@File : __init__.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from apps.iam.models.permission import Permission
from apps.iam.models.role import Role
from apps.iam.models.role_permission import RolePermission
from apps.iam.models.user_role import UserRole
from apps.iam.models.user_permission_override import UserPermissionOverride
from apps.iam.models.resource_policy import ResourcePolicy

__all__ = [
    "Permission",
    "Role",
    "RolePermission",
    "UserRole",
    "UserPermissionOverride",
    "ResourcePolicy",
]
