#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
首次部署站长账号初始化服务。
@Project : QWeb
@File : bootstrap_service.py
@Author : Qintsg
@Date : 2026-05-18 11:35
'''
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpRequest

from apps.accounts.services.account_bootstrap import ensure_user_related_records
from apps.accounts.services.token_service import issue_token_pair
from apps.accounts.services.username_policy import validate_username_policy
from apps.audit.services.audit_service import log_action
from apps.core.exceptions import ConflictException, ValidationException
from apps.iam.management.commands.init_permissions import (
    PRESET_PERMISSIONS,
    PRESET_ROLES,
    ROLE_PERMISSION_MAP,
)
from apps.iam.models import Permission, Role, RolePermission, UserRole

User = get_user_model()


def is_owner_bootstrap_required() -> bool:
    """
    判断当前系统是否仍需要首次创建站长账号。
    :return: 没有任何 owner 角色用户时返回 True。
    """
    return not UserRole.objects.filter(role__name="owner").exists()


def get_bootstrap_status() -> dict[str, bool]:
    """
    返回首次部署引导状态。
    :return: 包含是否需要创建站长账号的状态字典。
    """
    return {"owner_required": is_owner_bootstrap_required()}


@transaction.atomic
def create_owner_user(
    *,
    username: str,
    email: str,
    password: str,
    request: HttpRequest | None = None,
) -> dict[str, Any]:
    """
    在首次部署阶段创建站长账号并签发登录令牌。
    :param username: 站长用户名。
    :param email: 站长邮箱。
    :param password: 站长密码。
    :param request: HTTP 请求对象。
    :return: 包含用户和 JWT token 的字典。
    """
    if not is_owner_bootstrap_required():
        raise ConflictException("站长账号已存在，首次部署入口已关闭")

    normalized_username = validate_username_policy(username)
    normalized_email = email.strip()
    if not normalized_email:
        raise ValidationException(message="邮箱不能为空", errors={"email": ["邮箱不能为空"]})

    _ensure_iam_presets()
    owner_role = Role.objects.get(name="owner")
    user = User.objects.create_user(
        username=normalized_username,
        email=normalized_email,
        password=password,
        is_staff=True,
        is_superuser=True,
        user_type=User.UserType.ADMIN,
    )
    ensure_user_related_records(user=user, email=normalized_email)
    UserRole.objects.create(user=user, role=owner_role, created_by=user, updated_by=user)

    log_action(
        user=user,
        action="create",
        module="accounts",
        resource="owner",
        resource_id=str(user.uid),
        detail={"username": normalized_username, "bootstrap": True},
        request=request,
    )

    tokens = issue_token_pair(user=user, request=request)
    return {
        "user": user,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


def _ensure_iam_presets() -> None:
    """
    确保首次部署创建站长前已有 IAM 预置权限和系统角色。
    :return: 无返回值。
    """
    for module, resource, action, code, name in PRESET_PERMISSIONS:
        Permission.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "module": module,
                "resource": resource,
                "action": action,
                "is_active": True,
            },
        )

    for role_data in PRESET_ROLES:
        Role.objects.update_or_create(
            name=role_data["name"],
            defaults={
                "display_name": role_data["display_name"],
                "level": role_data["level"],
                "is_system": role_data["is_system"],
            },
        )

    all_permissions = {permission.code: permission for permission in Permission.objects.filter(is_active=True)}
    all_roles = {role.name: role for role in Role.objects.all()}
    for role_name, permissions in ROLE_PERMISSION_MAP.items():
        role = all_roles.get(role_name)
        if role is None:
            continue
        if permissions == "*":
            role_permissions = list(all_permissions.values())
        else:
            role_permissions = [all_permissions[code] for code in permissions if code in all_permissions]
        for permission in role_permissions:
            RolePermission.objects.get_or_create(role=role, permission=permission)
