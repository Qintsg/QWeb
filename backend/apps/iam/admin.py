"""IAM Admin 配置。"""

from django.contrib import admin

from apps.iam.models import (
    Permission,
    ResourcePolicy,
    Role,
    RolePermission,
    UserPermissionOverride,
    UserRole,
)


class RolePermissionInline(admin.TabularInline):
    """角色权限内联。"""

    model = RolePermission
    extra = 0
    autocomplete_fields = ["permission"]


class UserRoleInline(admin.TabularInline):
    """用户角色内联。"""

    model = UserRole
    extra = 0
    autocomplete_fields = ["user", "role"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理。"""

    list_display = ["code", "name", "module", "resource", "action", "is_active"]
    list_filter = ["module", "is_active"]
    search_fields = ["code", "name", "module"]
    ordering = ["module", "resource", "action"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理。"""

    list_display = ["name", "display_name", "level", "is_system"]
    list_filter = ["is_system"]
    search_fields = ["name", "display_name"]
    ordering = ["level"]
    inlines = [RolePermissionInline]


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """角色权限关联管理。"""

    list_display = ["role", "permission"]
    list_filter = ["role"]
    autocomplete_fields = ["role", "permission"]


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色管理。"""

    list_display = ["user", "role", "created_at"]
    list_filter = ["role"]
    autocomplete_fields = ["user", "role"]


@admin.register(UserPermissionOverride)
class UserPermissionOverrideAdmin(admin.ModelAdmin):
    """用户权限覆盖管理。"""

    list_display = ["user", "permission", "effect", "reason", "created_at"]
    list_filter = ["effect"]
    autocomplete_fields = ["user", "permission"]


@admin.register(ResourcePolicy)
class ResourcePolicyAdmin(admin.ModelAdmin):
    """资源策略管理。"""

    list_display = [
        "resource_type", "resource_id", "subject_type", "subject_id",
        "permission", "effect",
    ]
    list_filter = ["resource_type", "subject_type", "effect"]
    autocomplete_fields = ["permission"]
