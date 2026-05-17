#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户管理视图（管理员）。
@Project : QWeb
@File : user_views.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.accounts.api.serializers.user import UserAdminSerializer, UserSerializer
from apps.accounts.selectors.user_selector import get_user_by_id, list_users
from apps.core.responses import success_response


class UserViewSet(GenericViewSet):
    """用户管理 ViewSet（仅管理员可用）。

    list:   GET    /api/v1/users/           — 用户列表（支持搜索、过滤）
    retrieve: GET  /api/v1/users/{uid}/      — 用户详情
    partial_update: PATCH /api/v1/users/{uid}/ — 更新用户信息
    toggle_active: POST /api/v1/users/{uid}/toggle-active/ — 启用/禁用用户
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserAdminSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"

    def get_queryset(self) -> QuerySet:
        """构造当前请求使用的查询集。"""
        return list_users()

    def list(self, request: Request) -> Response:
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

    def retrieve(self, request: Request, uid: int | str | None = None) -> Response:
        """获取单个用户详情。"""
        user = get_user_by_id(uid)
        serializer = UserAdminSerializer(user)
        return success_response(data=serializer.data)

    def partial_update(self, request: Request, uid: int | str | None = None) -> Response:
        """更新用户信息（管理员字段）。"""
        user = get_user_by_id(uid)
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
    def toggle_active(self, request: Request, uid: int | str | None = None) -> Response:
        """切换用户启用/禁用状态。"""
        user = get_user_by_id(uid)
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

        status_text = "已启用" if user.is_active else "已禁用"
        return success_response(
            data=UserAdminSerializer(user).data,
            message=f"用户 {user.username} {status_text}",
        )
