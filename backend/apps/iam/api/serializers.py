"""IAM 序列化器。"""

from __future__ import annotations

from rest_framework import serializers

from apps.iam.models import (
    Permission,
    Role,
    RolePermission,
    UserPermissionOverride,
    UserRole,
)


# ---------- 权限 ----------

class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器。"""

    class Meta:
        model = Permission
        fields = ["id", "code", "name", "module", "resource", "action", "description", "is_active"]
        read_only_fields = ["id"]


class PermissionBriefSerializer(serializers.ModelSerializer):
    """权限简要序列化器（用于嵌套显示）。"""

    class Meta:
        model = Permission
        fields = ["id", "code", "name"]


# ---------- 角色 ----------

class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器。"""

    class Meta:
        model = Role
        fields = ["id", "name", "display_name", "description", "is_system", "level"]
        read_only_fields = ["id", "is_system"]


class RoleDetailSerializer(serializers.ModelSerializer):
    """角色详情序列化器（含权限列表）。"""

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "display_name", "description", "is_system", "level", "permissions"]
        read_only_fields = ["id", "is_system"]

    def get_permissions(self, obj: Role) -> list[dict]:
        """获取角色关联的权限列表。"""
        role_perms = RolePermission.objects.filter(role=obj).select_related("permission")
        return PermissionBriefSerializer(
            [rp.permission for rp in role_perms], many=True
        ).data


class RoleCreateSerializer(serializers.Serializer):
    """角色创建序列化器。"""

    name = serializers.CharField(max_length=50)
    display_name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, default="", allow_blank=True)
    level = serializers.IntegerField(required=False, default=100)


class RoleUpdateSerializer(serializers.Serializer):
    """角色更新序列化器。"""

    display_name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    level = serializers.IntegerField(required=False)


class RolePermissionSetSerializer(serializers.Serializer):
    """角色权限设置序列化器（全量替换）。"""

    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
    )


# ---------- 用户角色 ----------

class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色序列化器。"""

    role = RoleSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ["id", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class AssignRoleSerializer(serializers.Serializer):
    """分配角色序列化器。"""

    role_id = serializers.UUIDField()


# ---------- 用户权限覆盖 ----------

class UserPermissionOverrideSerializer(serializers.ModelSerializer):
    """用户权限覆盖序列化器。"""

    permission = PermissionBriefSerializer(read_only=True)

    class Meta:
        model = UserPermissionOverride
        fields = ["id", "permission", "effect", "reason", "created_at"]
        read_only_fields = ["id", "created_at"]


class AddOverrideSerializer(serializers.Serializer):
    """添加权限覆盖序列化器。"""

    permission_code = serializers.CharField(max_length=100)
    effect = serializers.ChoiceField(choices=["allow", "deny"])
    reason = serializers.CharField(required=False, default="", allow_blank=True)


class RemoveOverrideSerializer(serializers.Serializer):
    """移除权限覆盖序列化器。"""

    permission_code = serializers.CharField(max_length=100)


# ---------- 用户权限汇总 ----------

class UserPermissionSummarySerializer(serializers.Serializer):
    """用户权限汇总序列化器。"""

    roles = serializers.ListField(child=serializers.CharField())
    permissions = serializers.ListField(child=serializers.CharField())
