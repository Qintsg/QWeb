#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
DRF 权限类与权限装饰器。
@Project : QWeb
@File : permissions.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.iam.services.permission_resolver import PermissionResolver


class RequirePermission(BasePermission):
    """基于权限码的通用 DRF 权限类。

    用法:
        class MyView(APIView):
            permission_classes = [RequirePermission]
            required_permission = "blog.post.create"

    或通过 `get_required_permission()` 动态返回权限码。
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """检查当前请求是否具备访问权限。"""
        user = request.user
        if not user or not user.is_authenticated:
            return False

        permission_code = self._get_permission_code(view, request)
        if not permission_code:
            # 未配置权限码时默认放行（仅要求登录）
            return True

        return PermissionResolver.has_permission(user, permission_code)

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        """检查当前请求是否具备对象级访问权限。"""
        user = request.user
        permission_code = self._get_permission_code(view, request)
        if not permission_code:
            return True

        # 尝试获取资源类型和 ID 做资源级策略检查
        resource_type = getattr(view, "resource_type", None)
        resource_id = str(obj.pk) if hasattr(obj, "pk") else None

        if resource_type and resource_id:
            return PermissionResolver.has_permission(
                user, permission_code, resource_type, resource_id
            )

        return PermissionResolver.has_permission(user, permission_code)

    @staticmethod
    def _get_permission_code(view: APIView, request: Request) -> str | None:
        """从视图上获取权限码。"""
        # 优先尝试动态方法
        if hasattr(view, "get_required_permission"):
            return view.get_required_permission(request)
        # 再尝试静态属性
        return getattr(view, "required_permission", None)


class IsOwner(BasePermission):
    """仅 owner 角色可访问。"""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """检查当前请求是否具备访问权限。"""
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return PermissionResolver._is_owner(user)


def require_permission(permission_code: str) -> Callable:
    """视图方法级权限装饰器。

    用法:
        class PostViewSet(ViewSet):
            @require_permission("blog.post.create")
            def create(self, request):
                ...
    """

    def decorator(func: Callable) -> Callable:
        """构造附加权限校验的视图装饰器。"""

        @wraps(func)
        def wrapper(view_self: Any, request: Request, *args: Any, **kwargs: Any) -> Any:
            """执行权限校验后调用原始视图方法。"""
            user = request.user
            if not user or not user.is_authenticated:
                from apps.core.exceptions import AuthenticationFailedException

                raise AuthenticationFailedException()

            if not PermissionResolver.has_permission(user, permission_code):
                from apps.core.exceptions import PermissionDeniedException

                raise PermissionDeniedException()

            return func(view_self, request, *args, **kwargs)

        return wrapper

    return decorator
