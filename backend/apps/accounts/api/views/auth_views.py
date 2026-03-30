"""认证相关视图。

提供注册、登录、登出、Token 刷新等接口。
"""

from __future__ import annotations

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTRefreshView

from apps.accounts.api.serializers.auth import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from apps.accounts.api.serializers.user import UserSerializer
from apps.accounts.services.auth_service import (
    authenticate_user,
    change_password,
    register_user,
)
from apps.audit.services.login_audit import log_logout
from apps.core.responses import error_response, success_response


class RegisterView(APIView):
    """用户注册接口。

    POST /api/v1/auth/register/
    公开接口，无需认证。
    """

    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
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


class LoginView(APIView):
    """用户登录接口。

    POST /api/v1/auth/login/
    支持用户名或邮箱登录，返回 JWT Token。
    """

    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
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


class LogoutView(APIView):
    """用户登出接口。

    POST /api/v1/auth/logout/
    将 refresh token 加入黑名单，使其失效。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return error_response(
                message="缺少 refresh token",
                code=1,
                status=400,
            )

        try:
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
    直接复用 simplejwt 的刷新逻辑。
    """

    pass


class ChangePasswordView(APIView):
    """修改密码接口。

    POST /api/v1/auth/change-password/
    需要认证，验证旧密码后设置新密码。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
            request=request._request,
        )

        return success_response(message="密码修改成功")
