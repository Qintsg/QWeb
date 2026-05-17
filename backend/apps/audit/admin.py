#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
审计模块 Admin 配置。
@Project : QWeb
@File : admin.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.contrib import admin
from django.http import HttpRequest

from apps.audit.models import AuditLog, LoginLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """操作审计日志 Admin。"""

    list_display = ["created_at", "user", "action", "module", "resource", "resource_id", "ip_address"]
    list_filter = ["action", "module", "created_at"]
    search_fields = ["user__username", "resource", "resource_id", "ip_address"]
    readonly_fields = [
        "id", "user", "action", "module", "resource", "resource_id",
        "detail", "ip_address", "user_agent", "created_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        """禁止通过 Admin 新增只读审计记录。"""
        return False

    def has_change_permission(self, request: HttpRequest, obj: object | None = None) -> bool:
        """禁止通过 Admin 修改只读审计记录。"""
        return False

    def has_delete_permission(self, request: HttpRequest, obj: object | None = None) -> bool:
        """禁止通过 Admin 删除只读审计记录。"""
        return False


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """登录日志 Admin。"""

    list_display = [
        "created_at",
        "username",
        "login_type",
        "provider",
        "action",
        "success",
        "ip_address",
    ]
    list_filter = ["action", "login_type", "provider", "success", "created_at"]
    search_fields = ["username", "ip_address", "provider"]
    readonly_fields = [
        "id", "user", "username", "login_type", "provider", "action", "ip_address",
        "user_agent", "device_info", "success", "failure_reason", "created_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        """禁止通过 Admin 新增只读审计记录。"""
        return False

    def has_change_permission(self, request: HttpRequest, obj: object | None = None) -> bool:
        """禁止通过 Admin 修改只读审计记录。"""
        return False

    def has_delete_permission(self, request: HttpRequest, obj: object | None = None) -> bool:
        """禁止通过 Admin 删除只读审计记录。"""
        return False
