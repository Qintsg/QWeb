#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
审计模块序列化器。
@Project : QWeb
@File : serializers.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from rest_framework import serializers

from apps.audit.models import AuditLog, LoginLog


class AuditLogSerializer(serializers.ModelSerializer):
    """操作审计日志序列化器。"""

    username = serializers.CharField(source="user.username", default="", read_only=True)

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = AuditLog
        fields = [
            "id",
            "username",
            "action",
            "module",
            "resource",
            "resource_id",
            "detail",
            "ip_address",
            "user_agent",
            "created_at",
        ]
        read_only_fields = fields


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = LoginLog
        fields = [
            "id",
            "username",
            "login_type",
            "provider",
            "action",
            "ip_address",
            "user_agent",
            "device_info",
            "success",
            "failure_reason",
            "created_at",
        ]
        read_only_fields = fields
