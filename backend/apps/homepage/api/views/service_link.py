"""首页服务链接视图。"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core.responses import success_response, error_response
from apps.homepage.api.serializers.service_link import (
    ServiceLinkAdminSerializer,
    ServiceLinkPublicSerializer,
)
from apps.homepage.models import ServiceLink
from apps.iam.permissions import RequirePermission


class ServiceLinkPublicListView(APIView):
    """公开接口：获取所有可见的服务链接列表。"""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: Request) -> success_response:
        links = ServiceLink.objects.filter(is_visible=True).order_by("sort_order", "created_at")
        serializer = ServiceLinkPublicSerializer(links, many=True)
        return success_response(data=serializer.data, message="获取成功")


class ServiceLinkAdminListCreateView(APIView):
    """管理接口：列表查询 + 创建服务链接。"""

    permission_classes = [IsAuthenticated, RequirePermission]
    required_permission = "homepage.service_link.manage"

    def get(self, request: Request) -> success_response:
        links = ServiceLink.objects.all_with_deleted().active().order_by("sort_order", "created_at")
        serializer = ServiceLinkAdminSerializer(links, many=True)
        return success_response(data=serializer.data)

    def post(self, request: Request) -> success_response:
        serializer = ServiceLinkAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return success_response(
            data=serializer.data,
            message="创建成功",
            status=status.HTTP_201_CREATED,
        )


class ServiceLinkAdminDetailView(APIView):
    """管理接口：查看/更新/删除单个服务链接。"""

    permission_classes = [IsAuthenticated, RequirePermission]
    required_permission = "homepage.service_link.manage"

    def _get_link(self, pk: str) -> ServiceLink | None:
        try:
            return ServiceLink.objects.get(pk=pk)
        except ServiceLink.DoesNotExist:
            return None

    def get(self, request: Request, pk: str) -> success_response:
        link = self._get_link(pk)
        if not link:
            return error_response(message="服务链接不存在", status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceLinkAdminSerializer(link)
        return success_response(data=serializer.data)

    def patch(self, request: Request, pk: str) -> success_response:
        link = self._get_link(pk)
        if not link:
            return error_response(message="服务链接不存在", status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceLinkAdminSerializer(link, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return success_response(data=serializer.data, message="更新成功")

    def delete(self, request: Request, pk: str) -> success_response:
        link = self._get_link(pk)
        if not link:
            return error_response(message="服务链接不存在", status=status.HTTP_404_NOT_FOUND)
        link.is_deleted = True
        link.updated_by = request.user
        link.save(update_fields=["is_deleted", "updated_by", "updated_at"])
        return success_response(message="删除成功")
