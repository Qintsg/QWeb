"""用户权限覆盖管理服务。"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from apps.audit.services.audit_service import log_action
from apps.core.exceptions import ConflictException, ResourceNotFoundException
from apps.iam.models import Permission, UserPermissionOverride

if TYPE_CHECKING:
    from apps.accounts.models import User


def add_override(
    *,
    user: User,
    permission_code: str,
    effect: str,
    reason: str = "",
    operator: User | None = None,
    request=None,
) -> UserPermissionOverride:
    """为用户添加权限覆盖。

    Args:
        user: 目标用户
        permission_code: 权限码
        effect: allow 或 deny
        reason: 覆盖原因
        operator: 操作人
    """
    try:
        permission = Permission.objects.get(code=permission_code, is_active=True)
    except Permission.DoesNotExist:
        raise ResourceNotFoundException(f"权限 '{permission_code}' 不存在")

    if UserPermissionOverride.objects.filter(user=user, permission=permission).exists():
        raise ConflictException(f"用户已存在对权限 '{permission_code}' 的覆盖")

    override = UserPermissionOverride.objects.create(
        user=user,
        permission=permission,
        effect=effect,
        reason=reason,
        created_by=operator,
        updated_by=operator,
    )
    log_action(
        user=operator,
        action="create",
        module="iam",
        resource="override",
        resource_id=str(override.pk),
        detail={"target_user": str(user.pk), "permission": permission_code, "effect": effect},
        request=request,
    )
    return override


def remove_override(*, user: User, permission_code: str, request=None) -> None:
    """移除用户的权限覆盖。"""
    deleted_count, _ = UserPermissionOverride.objects.filter(
        user=user,
        permission__code=permission_code,
    ).delete()
    if deleted_count == 0:
        raise ResourceNotFoundException("该用户不存在此权限覆盖")
    log_action(
        user=getattr(request, "user", None) if request else None,
        action="delete",
        module="iam",
        resource="override",
        resource_id="",
        detail={"target_user": str(user.pk), "permission": permission_code},
        request=request,
    )


def update_override(
    *,
    override_id: UUID,
    operator: User | None = None,
    request=None,
    **fields,
) -> UserPermissionOverride:
    """更新权限覆盖（如修改 effect 或 reason）。"""
    try:
        override = UserPermissionOverride.objects.get(pk=override_id)
    except UserPermissionOverride.DoesNotExist:
        raise ResourceNotFoundException("权限覆盖记录不存在")

    for key, value in fields.items():
        setattr(override, key, value)
    override.updated_by = operator
    override.save()
    log_action(
        user=operator,
        action="update",
        module="iam",
        resource="override",
        resource_id=str(override.pk),
        detail={"fields": list(fields.keys())},
        request=request,
    )
    return override


def list_overrides(*, user: User) -> list[UserPermissionOverride]:
    """列出用户的全部权限覆盖。"""
    return list(
        UserPermissionOverride.objects.filter(user=user)
        .select_related("permission")
        .order_by("permission__code")
    )
