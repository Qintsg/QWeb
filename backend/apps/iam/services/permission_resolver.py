#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
权限解析器。

实现 IAM 设计文档中的 7 步权限检查流程：
1. owner 角色 → 放行
2. 用户已禁用 → 拒绝
3. 用户 deny 覆盖命中 → 拒绝
4. 用户 allow 覆盖命中 → 放行
5. 角色权限包含 → 放行
6. 资源级策略命中 → 按策略决定
7. 默认拒绝
@Project : QWeb
@File : permission_resolver.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import TYPE_CHECKING

from apps.iam.models import (
    Permission,
    ResourcePolicy,
    RolePermission,
    UserPermissionOverride,
    UserRole,
)

if TYPE_CHECKING:
    from apps.accounts.models import User


class PermissionResolver:
    """统一权限解析入口。"""

    @staticmethod
    def has_permission(
        user: User,
        permission_code: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> bool:
        """检查用户是否拥有指定权限。

        严格按照 7 步检查流程执行，任意一步命中即返回结果。

        :param user: 待检查的用户
        :param permission_code: 权限码，如 blog.post.create
        :param resource_type: 资源类型（用于资源级策略），可选
        :param resource_id: 资源 ID（用于资源级策略），可选

        :return: 是否拥有权限
        """
        # 未认证用户一律拒绝
        if not user or not user.is_authenticated:
            return False

        # ① owner 角色拥有一切权限
        if PermissionResolver._is_owner(user):
            return True

        # ② 用户已禁用
        if not user.is_active:
            return False

        # ③ 用户 deny 覆盖命中
        if PermissionResolver._has_deny_override(user, permission_code):
            return False

        # ④ 用户 allow 覆盖命中
        if PermissionResolver._has_allow_override(user, permission_code):
            return True

        # ⑤ 角色权限包含
        if PermissionResolver._has_role_permission(user, permission_code):
            return True

        # ⑥ 资源级策略
        if resource_type and resource_id:
            policy_result = PermissionResolver._check_resource_policy(
                user, permission_code, resource_type, resource_id
            )
            if policy_result is not None:
                return policy_result

        # ⑦ 默认拒绝
        return False

    @staticmethod
    def resolve_user_permissions(user: User) -> set[str]:
        """解析用户最终拥有的全部权限码集合。

        注意：此方法不考虑资源级策略（资源级策略需要具体资源上下文）。

        :return: 权限码集合
        """
        if not user or not user.is_authenticated:
            return set()

        # owner 拥有全部权限
        if PermissionResolver._is_owner(user):
            return set(
                Permission.objects.filter(is_active=True).values_list("code", flat=True)
            )

        if not user.is_active:
            return set()

        # 角色权限
        role_ids = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
        role_permissions = set(
            RolePermission.objects.filter(
                role_id__in=role_ids,
                permission__is_active=True,
            ).values_list("permission__code", flat=True)
        )

        # 覆盖：加入 allow，移除 deny
        overrides = UserPermissionOverride.objects.filter(
            user=user,
            permission__is_active=True,
        ).select_related("permission")

        for override in overrides:
            if override.effect == UserPermissionOverride.Effect.ALLOW:
                role_permissions.add(override.permission.code)
            elif override.effect == UserPermissionOverride.Effect.DENY:
                role_permissions.discard(override.permission.code)

        return role_permissions

    @staticmethod
    def get_user_roles(user: User) -> list[str]:
        """获取用户的全部角色名列表。"""
        if not user or not user.is_authenticated:
            return []
        return list(
            UserRole.objects.filter(user=user).values_list("role__name", flat=True)
        )

    # ---------- 内部方法 ----------

    @staticmethod
    def _is_owner(user: User) -> bool:
        """检查用户是否拥有 owner 角色。"""
        return UserRole.objects.filter(user=user, role__name="owner").exists()

    @staticmethod
    def _has_deny_override(user: User, permission_code: str) -> bool:
        """检查用户是否有 deny 覆盖。"""
        return UserPermissionOverride.objects.filter(
            user=user,
            permission__code=permission_code,
            permission__is_active=True,
            effect=UserPermissionOverride.Effect.DENY,
        ).exists()

    @staticmethod
    def _has_allow_override(user: User, permission_code: str) -> bool:
        """检查用户是否有 allow 覆盖。"""
        return UserPermissionOverride.objects.filter(
            user=user,
            permission__code=permission_code,
            permission__is_active=True,
            effect=UserPermissionOverride.Effect.ALLOW,
        ).exists()

    @staticmethod
    def _has_role_permission(user: User, permission_code: str) -> bool:
        """检查用户的角色中是否包含指定权限。"""
        role_ids = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
        return RolePermission.objects.filter(
            role_id__in=role_ids,
            permission__code=permission_code,
            permission__is_active=True,
        ).exists()

    @staticmethod
    def _check_resource_policy(
        user: User,
        permission_code: str,
        resource_type: str,
        resource_id: str,
    ) -> bool | None:
        """检查资源级策略。

        :return: True=放行, False=拒绝, None=无匹配策略
        """
        # 收集用户角色 ID
        role_ids = list(
            UserRole.objects.filter(user=user).values_list("role_id", flat=True)
        )

        # 查询匹配的策略（用户级 + 角色级）
        from django.db.models import Q

        policies = ResourcePolicy.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id,
            permission__code=permission_code,
            permission__is_active=True,
        ).filter(
            Q(subject_type=ResourcePolicy.SubjectType.USER, subject_id=str(user.pk))
            | Q(
                subject_type=ResourcePolicy.SubjectType.ROLE,
                subject_id__in=[str(role_id) for role_id in role_ids],
            )
        )

        if not policies.exists():
            return None

        # deny 优先
        for policy in policies:
            if policy.effect == ResourcePolicy.Effect.DENY:
                return False

        # 存在 allow 策略
        return True
