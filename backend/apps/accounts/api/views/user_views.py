"""用户管理视图（管理员）。

提供用户列表查询、详情查看、状态管理等管理接口。
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from apps.accounts.api.serializers.user import UserAdminSerializer, UserSerializer
from apps.accounts.selectors.user_selector import get_user_by_id, list_users
from apps.core.responses import success_response


class UserViewSet(GenericViewSet):
    """用户管理 ViewSet（仅管理员可用）。

    list:   GET    /api/v1/users/           — 用户列表（支持搜索、过滤）
    retrieve: GET  /api/v1/users/{id}/      — 用户详情
    partial_update: PATCH /api/v1/users/{id}/ — 更新用户信息
    toggle_active: POST /api/v1/users/{id}/toggle-active/ — 启用/禁用用户
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserAdminSerializer

    def get_queryset(self):
        return list_users()

    def list(self, request: Request):
        """获取用户列表，支持搜索和激活状态过滤。"""
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")

        # 解析 is_active 参数
        active_filter = None
        if is_active is not None:
            active_filter = is_active.lower() in ("true", "1")

        queryset = list_users(is_active=active_filter, search=search)

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return success_response(data=serializer.data)

    def retrieve(self, request: Request, pk=None):
        """获取单个用户详情。"""
        user = get_user_by_id(pk)
        serializer = UserAdminSerializer(user)
        return success_response(data=serializer.data)

    def partial_update(self, request: Request, pk=None):
        """更新用户信息（管理员字段）。"""
        user = get_user_by_id(pk)
        serializer = UserAdminSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            data=UserAdminSerializer(user).data,
            message="用户信息已更新",
        )

    @action(detail=True, methods=["post"], url_path="toggle-active")
    def toggle_active(self, request: Request, pk=None):
        """切换用户启用/禁用状态。"""
        user = get_user_by_id(pk)
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

        status_text = "已启用" if user.is_active else "已禁用"
        return success_response(
            data=UserAdminSerializer(user).data,
            message=f"用户 {user.username} {status_text}",
        )
