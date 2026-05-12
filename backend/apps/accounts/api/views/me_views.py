"""当前用户（me）相关视图。

提供当前登录用户的信息查询与资料更新接口。
"""

from __future__ import annotations

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.accounts.api.serializers.auth import ChangePasswordSerializer
from apps.accounts.api.serializers.user import MeSerializer
from apps.accounts.services.auth_service import change_password
from apps.core.responses import success_response


class MeView(GenericAPIView):
    """当前用户信息接口。

    GET  /api/v1/me/ — 获取当前用户完整信息
    PUT  /api/v1/me/ — 更新当前用户基本信息（nickname 等）
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get(self, request: Request):
        serializer = self.get_serializer(request.user)
        return success_response(data=serializer.data)

    def put(self, request: Request):
        return self._update(request)

    def patch(self, request: Request):
        return self._update(request)

    def _update(self, request: Request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            data=self.get_serializer(request.user).data,
            message="更新成功",
        )


class MePasswordView(GenericAPIView):
    """当前用户修改密码接口。

    PUT /api/v1/me/password/ — 修改当前用户密码
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request: Request):
        return self.put(request)

    def put(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
            request=request._request,
        )

        return success_response(message="密码修改成功")
