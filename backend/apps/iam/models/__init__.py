"""IAM 数据模型。

包含权限定义、角色、角色-权限关联、用户-角色关联、用户权限覆盖和资源级策略。
"""

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
