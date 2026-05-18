#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
认证相关视图。
@Project : QWeb
@File : auth_views.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTRefreshView

from apps.accounts.api.serializers.auth import (
    BootstrapOwnerSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    OAuthAuthorizeSerializer,
    OAuthBindSerializer,
    OAuthCallbackSerializer,
    OAuthRegisterSerializer,
    RegisterSerializer,
)
from apps.accounts.api.serializers.user import UserSerializer
from apps.accounts.services.auth_service import (
    authenticate_user,
    register_user,
)
from apps.accounts.services.bootstrap_service import (
    create_owner_user,
    get_bootstrap_status,
)
from apps.accounts.services.oauth_service import (
    bind_oauth_to_existing_user,
    build_oauth_authorization_url,
    complete_oauth_callback,
    register_user_from_oauth,
)
from apps.accounts.services.token_service import (
    get_user_from_refresh_token,
    record_rotated_refresh_token,
    revoke_refresh_token,
)
from apps.audit.services.login_audit import log_logout
from apps.core.responses import success_response


class BootstrapStatusView(GenericAPIView):
    """首次部署状态接口。

    GET /api/v1/auth/bootstrap/status/
    公开接口，用于前端判断是否需要进入站长创建流程。
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: Request) -> Response:
        """处理 GET 请求并返回统一响应。"""
        return success_response(data=get_bootstrap_status(), message="获取首次部署状态成功")


class BootstrapOwnerView(GenericAPIView):
    """首次部署创建站长账号接口。

    POST /api/v1/auth/bootstrap/owner/
    仅在系统没有任何 owner 角色用户时可用。
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = BootstrapOwnerSerializer

    def post(self, request: Request) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_owner_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            request=request._request,
        )
        return success_response(
            data={
                "status": "authenticated",
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
                "redirect": "/dashboard",
            },
            message="站长账号创建成功",
            status=201,
        )


class RegisterView(GenericAPIView):
    """用户注册接口。

    POST /api/v1/auth/register/
    公开接口，无需认证。
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = register_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            request=request._request,
        )

        return success_response(
            data={
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
            },
            message="注册成功",
            status=201,
        )


class LoginView(GenericAPIView):
    """用户登录接口。

    POST /api/v1/auth/login/
    支持用户名、邮箱或手机号登录，返回 JWT Token。
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = authenticate_user(
            login=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
            request=request._request,
        )

        return success_response(
            data={
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
            },
            message="登录成功",
        )


class OAuthAuthorizeView(GenericAPIView):
    """OAuth 授权地址接口。

    GET /api/v1/auth/oauth/{provider}/authorize/
    返回第三方授权跳转 URL，client secret 不下发到前端。
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OAuthAuthorizeSerializer

    def get(self, request: Request, provider: str) -> Response:
        """处理 GET 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = build_oauth_authorization_url(
            provider=provider,
            redirect=serializer.validated_data.get("redirect", "")
        )
        return success_response(data=result, message="获取第三方授权地址成功")


class OAuthCallbackView(GenericAPIView):
    """OAuth 回调完成接口。

    POST /api/v1/auth/oauth/{provider}/callback/
    前端回调页提交 code/state 后，后端换取资料并返回登录或待选择状态。
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OAuthCallbackSerializer

    def post(self, request: Request, provider: str) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = complete_oauth_callback(
            provider=provider,
            code=serializer.validated_data["code"],
            state=serializer.validated_data["state"],
            request=request._request,
        )
        if result["status"] == "requires_account_choice":
            return success_response(data=result, message="请选择第三方账号绑定方式")
        return success_response(
            data={
                "status": result["status"],
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
                "redirect": result["redirect"],
            },
            message="第三方登录成功",
        )


class OAuthBindView(GenericAPIView):
    """绑定第三方账号到已有账号。"""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OAuthBindSerializer

    def post(self, request: Request, provider: str) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = bind_oauth_to_existing_user(
            provider=provider,
            pending_token=serializer.validated_data["pending_token"],
            login=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
            request=request._request,
        )
        return success_response(
            data={
                "status": result["status"],
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
                "redirect": result["redirect"],
            },
            message="第三方账号绑定成功",
        )


class OAuthRegisterView(GenericAPIView):
    """使用第三方账号自动注册新账号。"""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OAuthRegisterSerializer

    def post(self, request: Request, provider: str) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = register_user_from_oauth(
            provider=provider,
            pending_token=serializer.validated_data["pending_token"],
            username=serializer.validated_data["username"],
            nickname=serializer.validated_data.get("nickname", ""),
            request=request._request,
        )
        return success_response(
            data={
                "status": result["status"],
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
                "redirect": result["redirect"],
            },
            message="第三方账号注册成功",
            status=201,
        )


class LogoutView(GenericAPIView):
    """用户登出接口。

    POST /api/v1/auth/logout/
    将 refresh token 加入黑名单，使其失效。
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request: Request) -> Response:
        """处理 POST 请求并返回统一响应。"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            revoke_refresh_token(refresh_token=refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            # Token 无效或已黑名单，静默处理
            pass

        # 审计：记录登出
        log_logout(user=request.user, request=request._request)

        return success_response(message="已登出")


class TokenRefreshView(SimpleJWTRefreshView):
    """Token 刷新接口。

    POST /api/v1/auth/token/refresh/
    使用 refresh token 获取新的 access token。
    复用 SimpleJWT 刷新逻辑，并同步项目级 refresh token 记录。
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """处理 POST 请求并返回统一响应。"""
        old_refresh_token = str(request.data.get("refresh") or "")
        user = get_user_from_refresh_token(old_refresh_token, verify=True) if old_refresh_token else None
        response = super().post(request, *args, **kwargs)
        if response.status_code < 400 and old_refresh_token:
            record_rotated_refresh_token(
                old_refresh_token=old_refresh_token,
                new_refresh_token=response.data.get("refresh"),
                user=user,
                request=request._request,
            )
        return response
