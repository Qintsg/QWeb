"""IAM API 视图。"""

from __future__ import annotations

from uuid import UUID

from rest_framework import status as http_status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.core.exceptions import ResourceNotFoundException
from apps.core.responses import success_response
from apps.iam.api.serializers import (
    AddOverrideSerializer,
    AssignRoleSerializer,
    PermissionSerializer,
    RemoveOverrideSerializer,
    RoleCreateSerializer,
    RoleDetailSerializer,
    RolePermissionSetSerializer,
    RoleSerializer,
    RoleUpdateSerializer,
    UserPermissionOverrideSerializer,
    UserPermissionSummarySerializer,
    UserRoleSerializer,
)
from apps.iam.models import Permission, Role, UserRole
from apps.iam.permissions import RequirePermission
from apps.iam.services import override_service, role_service
from apps.iam.services.permission_resolver import PermissionResolver


# ==================== 权限管理 ====================


class PermissionListView(GenericAPIView):
    """权限列表（只读）。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.permission.view"
    serializer_class = PermissionSerializer

    def get(self, request: Request):
        """获取全部权限列表，支持按 module 过滤。"""
        queryset = Permission.objects.filter(is_active=True)
        module = request.query_params.get("module")
        if module:
            queryset = queryset.filter(module=module)
        serializer = PermissionSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="获取权限列表成功")


# ==================== 角色管理 ====================


class RoleListCreateView(GenericAPIView):
    """角色列表 & 创建。"""

    permission_classes = [RequirePermission]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoleCreateSerializer
        return RoleSerializer

    def get_required_permission(self, request: Request) -> str:
        if request.method == "GET":
            return "iam.role.view"
        return "iam.role.create"

    def get(self, request: Request):
        """角色列表。"""
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return success_response(data=serializer.data, message="获取角色列表成功")

    def post(self, request: Request):
        """创建角色。"""
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        role = role_service.create_role(**ser.validated_data, operator=request.user, request=request._request)
        return success_response(
            data=RoleSerializer(role).data,
            message="角色创建成功",
            status=http_status.HTTP_201_CREATED,
        )


class RoleDetailView(GenericAPIView):
    """角色详情 / 更新 / 删除。"""

    permission_classes = [RequirePermission]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return RoleUpdateSerializer
        return RoleDetailSerializer

    def get_required_permission(self, request: Request) -> str:
        if request.method == "GET":
            return "iam.role.view"
        if request.method == "DELETE":
            return "iam.role.delete"
        return "iam.role.update"

    def get(self, request: Request, role_id: UUID):
        """角色详情（含权限列表）。"""
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise ResourceNotFoundException("角色不存在")
        serializer = RoleDetailSerializer(role)
        return success_response(data=serializer.data, message="获取角色详情成功")

    def patch(self, request: Request, role_id: UUID):
        """更新角色。"""
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        role = role_service.update_role(
            role_id=role_id, operator=request.user, request=request._request, **ser.validated_data
        )
        return success_response(data=RoleSerializer(role).data, message="角色更新成功")

    def delete(self, request: Request, role_id: UUID):
        """删除角色。"""
        role_service.delete_role(role_id=role_id, request=request._request)
        return success_response(message="角色删除成功")


class RolePermissionsView(GenericAPIView):
    """设置角色权限（全量替换）。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.role.update"
    serializer_class = RolePermissionSetSerializer

    def put(self, request: Request, role_id: UUID):
        """全量替换角色权限。"""
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        count = role_service.set_role_permissions(
            role_id=role_id,
            permission_ids=ser.validated_data["permission_ids"],
            operator=request.user,
            request=request._request,
        )
        return success_response(
            data={"count": count},
            message=f"已设置 {count} 个权限",
        )


# ==================== 用户角色管理 ====================


class UserRoleListView(GenericAPIView):
    """查看指定用户的角色列表。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.user_role.view"
    serializer_class = UserRoleSerializer

    def get(self, request: Request, user_id: int):
        """获取用户角色列表。"""
        user_roles = UserRole.objects.filter(user_id=user_id).select_related("role")
        serializer = UserRoleSerializer(user_roles, many=True)
        return success_response(data=serializer.data, message="获取用户角色成功")


class UserRoleAssignView(GenericAPIView):
    """为用户分配 / 移除角色。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.user_role.manage"
    serializer_class = AssignRoleSerializer

    def post(self, request: Request, user_id: int):
        """为用户分配角色。"""
        from apps.accounts.models import User

        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用户不存在")

        user_role = role_service.assign_role(
            user=target_user,
            role_id=ser.validated_data["role_id"],
            operator=request.user,
            request=request._request,
        )
        return success_response(
            data=UserRoleSerializer(user_role).data,
            message="角色分配成功",
            status=http_status.HTTP_201_CREATED,
        )

    def delete(self, request: Request, user_id: int):
        """移除用户角色。"""
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        from apps.accounts.models import User

        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用户不存在")

        role_service.unassign_role(
            user=target_user,
            role_id=ser.validated_data["role_id"],
            request=request._request,
        )
        return success_response(message="角色已移除")


# ==================== 用户权限覆盖 ====================


class UserOverrideListView(GenericAPIView):
    """查看指定用户的权限覆盖列表。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.override.view"
    serializer_class = UserPermissionOverrideSerializer

    def get(self, request: Request, user_id: int):
        """获取用户的权限覆盖列表。"""
        from apps.accounts.models import User

        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用户不存在")

        overrides = override_service.list_overrides(user=target_user)
        serializer = UserPermissionOverrideSerializer(overrides, many=True)
        return success_response(data=serializer.data, message="获取权限覆盖成功")


class UserOverrideManageView(GenericAPIView):
    """添加 / 移除用户权限覆盖。"""

    permission_classes = [RequirePermission]
    required_permission = "iam.override.manage"

    def get_serializer_class(self):
        if self.request.method == "DELETE":
            return RemoveOverrideSerializer
        return AddOverrideSerializer

    def post(self, request: Request, user_id: int):
        """添加用户权限覆盖。"""
        from apps.accounts.models import User

        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用户不存在")

        override = override_service.add_override(
            user=target_user,
            operator=request.user,
            request=request._request,
            **ser.validated_data,
        )
        return success_response(
            data=UserPermissionOverrideSerializer(override).data,
            message="权限覆盖已添加",
            status=http_status.HTTP_201_CREATED,
        )

    def delete(self, request: Request, user_id: int):
        """移除用户权限覆盖。"""
        from apps.accounts.models import User

        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用户不存在")

        override_service.remove_override(
            user=target_user,
            permission_code=ser.validated_data["permission_code"],
            request=request._request,
        )
        return success_response(message="权限覆盖已移除")


# ==================== 当前用户权限查询 ====================


class MePermissionsView(GenericAPIView):
    """查看当前登录用户的权限汇总。"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserPermissionSummarySerializer

    def get(self, request: Request):
        """获取当前用户的角色与权限汇总。"""
        user = request.user
        roles = PermissionResolver.get_user_roles(user)
        permissions = sorted(PermissionResolver.resolve_user_permissions(user))
        serializer = UserPermissionSummarySerializer(
            {"roles": roles, "permissions": permissions}
        )
        return success_response(data=serializer.data, message="获取权限汇总成功")
