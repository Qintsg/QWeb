#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
首页服务链接序列化器。
@Project : QWeb
@File : service_link.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from rest_framework import serializers

from apps.homepage.models import ServiceLink


class ServiceLinkPublicSerializer(serializers.ModelSerializer):
    """公开 API 使用的只读序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = ServiceLink
        fields = [
            "id",
            "title",
            "url",
            "description",
            "remark",
            "icon",
            "color",
            "category",
            "sort_order",
        ]
        read_only_fields = fields


class ServiceLinkAdminSerializer(serializers.ModelSerializer):
    """管理后台使用的完整序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = ServiceLink
        fields = [
            "id",
            "title",
            "url",
            "description",
            "remark",
            "icon",
            "color",
            "category",
            "sort_order",
            "is_visible",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
