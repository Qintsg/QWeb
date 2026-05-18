#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
站点元数据视图。
@Project : QWeb
@File : site_metadata.py
@Author : Qintsg
@Date : 2026-05-18 12:10
'''
from __future__ import annotations

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.responses import success_response
from apps.homepage.api.serializers.site_metadata import SiteMetadataSerializer
from apps.homepage.services.site_metadata_service import (
    get_site_metadata,
    update_site_metadata,
)
from apps.iam.permissions import RequirePermission


class SiteMetadataPublicView(GenericAPIView):
    """公开接口：获取站点元数据。"""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = SiteMetadataSerializer

    def get(self, request: Request) -> Response:
        """处理 GET 请求并返回统一响应。"""
        serializer = self.get_serializer(get_site_metadata())
        return success_response(data=serializer.data, message="获取站点元数据成功")


class SiteMetadataAdminView(GenericAPIView):
    """管理接口：查看和更新站点元数据。"""

    permission_classes = [IsAuthenticated, RequirePermission]
    required_permission = "system_config.config.update"
    serializer_class = SiteMetadataSerializer

    def get_required_permission(self, request: Request) -> str:
        """根据当前请求动作返回所需权限码。"""
        if request.method == "GET":
            return "system_config.config.view"
        return "system_config.config.update"

    def get(self, request: Request) -> Response:
        """处理 GET 请求并返回统一响应。"""
        serializer = self.get_serializer(get_site_metadata())
        return success_response(data=serializer.data, message="获取站点元数据成功")

    def patch(self, request: Request) -> Response:
        """处理 PATCH 请求并返回统一响应。"""
        metadata = get_site_metadata()
        serializer = self.get_serializer(metadata, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_metadata = update_site_metadata(
            fields=serializer.validated_data,
            operator=request.user,
            request=request._request,
        )
        return success_response(
            data=self.get_serializer(updated_metadata).data,
            message="站点元数据已更新",
        )
