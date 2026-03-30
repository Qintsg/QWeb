"""角色管理服务。"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.db import transaction

from apps.core.exceptions import (
    ConflictException,
    ResourceNotFoundException,
    ValidationException,
)
from apps.iam.models import Role, RolePermission, UserRole

if TYPE_CHECKING:
    from django.http import HttpRequest

    from apps.accounts.models import User


def create_role(
    *,
    name: str,
    display_name: str,
    description: str = "",
    level: int = 100,
    operator: User | None = None,
    request: HttpRequest | None = None,
) -> Role:
    """创建角色。"""
    if Role.objects.filter(name=name).exists():
        raise ConflictException(f"角色名 '{name}' 已存在")

    role = Role.objects.create(
        name=name,
        display_name=display_name,
        description=description,
        level=level,
        created_by=operator,
        updated_by=operator,
    )

    from apps.audit.services.audit_service import log_action
    log_action(
        user=operator, action="create", module="iam", resource="role",
        resource_id=str(role.pk), detail={"name": name, "display_name": display_name},
        request=request,
    )

    return role


def update_role(
    *,
    role_id: UUID,
    operator: User | None = None,
    request: HttpRequest | None = None,
    **fields,
) -> Role:
    """更新角色信息。"""
    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        raise ResourceNotFoundException("角色不存在")

    if role.is_system:
        # 系统角色只允许修改 display_name 和 description
        allowed = {"display_name", "description"}
        invalid_fields = set(fields.keys()) - allowed
        if invalid_fields:
            raise ValidationException(f"系统角色不允许修改字段: {', '.join(invalid_fields)}")

    for key, value in fields.items():
        setattr(role, key, value)
    role.updated_by = operator
    role.save()

    from apps.audit.services.audit_service import log_action
    log_action(
        user=operator, action="update", module="iam", resource="role",
        resource_id=str(role.pk), detail={"fields": list(fields.keys())},
        request=request,
    )

    return role


def delete_role(*, role_id: UUID, request: HttpRequest | None = None) -> None:
    """软删除角色。"""
    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        raise ResourceNotFoundException("角色不存在")

    if role.is_system:
        raise ValidationException("系统角色不允许删除")

    role.soft_delete()

    from apps.audit.services.audit_service import log_action
    log_action(
        user=None, action="delete", module="iam", resource="role",
        resource_id=str(role.pk), detail={"name": role.name},
        request=request,
    )


def assign_role(*, user: User, role_id: UUID, operator: User | None = None, request: HttpRequest | None = None) -> UserRole:
    """为用户分配角色。"""
    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        raise ResourceNotFoundException("角色不存在")

    if UserRole.objects.filter(user=user, role=role).exists():
        raise ConflictException("用户已拥有该角色")

    user_role = UserRole.objects.create(
        user=user,
        role=role,
        created_by=operator,
        updated_by=operator,
    )

    from apps.audit.services.audit_service import log_action
    log_action(
        user=operator, action="assign", module="iam", resource="user_role",
        resource_id=str(user_role.pk),
        detail={"target_user": str(user.pk), "role": role.name},
        request=request,
    )

    return user_role


def unassign_role(*, user: User, role_id: UUID, request: HttpRequest | None = None) -> None:
    """移除用户角色。"""
    deleted_count, _ = UserRole.objects.filter(user=user, role_id=role_id).delete()
    if deleted_count == 0:
        raise ResourceNotFoundException("该用户不拥有此角色")

    from apps.audit.services.audit_service import log_action
    log_action(
        user=None, action="revoke", module="iam", resource="user_role",
        resource_id=str(role_id),
        detail={"target_user": str(user.pk)},
        request=request,
    )


@transaction.atomic
def set_role_permissions(
    *,
    role_id: UUID,
    permission_ids: list[UUID],
    operator: User | None = None,
    request: HttpRequest | None = None,
) -> int:
    """设置角色权限（全量替换）。

    Returns:
        新设置的权限数量
    """
    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        raise ResourceNotFoundException("角色不存在")

    # 清除旧权限
    RolePermission.objects.filter(role=role).delete()

    # 批量创建新权限
    role_permissions = [
        RolePermission(
            role=role,
            permission_id=pid,
            created_by=operator,
            updated_by=operator,
        )
        for pid in permission_ids
    ]
    RolePermission.objects.bulk_create(role_permissions)

    from apps.audit.services.audit_service import log_action
    log_action(
        user=operator, action="update", module="iam", resource="role_permissions",
        resource_id=str(role.pk),
        detail={"role": role.name, "permission_count": len(role_permissions)},
        request=request,
    )

    return len(role_permissions)
