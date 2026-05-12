#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
审计模块视图 — IAM 授权只读查询。
@Project : QWeb
@File : views.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.db.models import QuerySet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.audit.api.serializers import AuditLogSerializer, LoginLogSerializer
from apps.audit.models import AuditLog, LoginLog
from apps.core.pagination import StandardPagination
from apps.iam.permissions import RequirePermission


class AuditLogListView(generics.ListAPIView):
    """
    操作审计日志列表（管理员只读）。

    支持按 action、module、resource 过滤，按 created_at 排序。
    """

    serializer_class = AuditLogSerializer
    permission_classes = [RequirePermission]
    required_permission = "audit.log.view"
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["action", "module", "resource"]
    search_fields = ["user__username", "resource_id"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet:
        """构造当前请求使用的查询集。"""
        return AuditLog.objects.select_related("user").all()


class LoginLogListView(generics.ListAPIView):
    """
    登录日志列表（管理员只读）。

    支持按 action 过滤，按 created_at 排序。
    """

    serializer_class = LoginLogSerializer
    permission_classes = [RequirePermission]
    required_permission = "audit.log.view"
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["action", "login_type", "provider", "success"]
    search_fields = ["username", "ip_address", "provider"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet:
        """构造当前请求使用的查询集。"""
        return LoginLog.objects.select_related("user").all()
