"""认证相关视图。

提供注册、登录、登出、Token 刷新等接口。
"""

from __future__ import annotations

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTRefreshView

from apps.accounts.api.serializers.auth import (
    ChangePasswordSerializer,
    GitHubOAuthAuthorizeSerializer,
    GitHubOAuthCallbackSerializer,
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
    change_password,
    register_user,
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


class RegisterView(GenericAPIView):
    """用户注册接口。

    POST /api/v1/auth/register/
    公开接口，无需认证。
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request: Request):
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

    def post(self, request: Request):
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

    def get(self, request: Request, provider: str):
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

    def post(self, request: Request, provider: str):
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

    def post(self, request: Request, provider: str):
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

    def post(self, request: Request, provider: str):
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


class GitHubOAuthAuthorizeView(OAuthAuthorizeView):
    """兼容旧 GitHub OAuth 授权地址接口。"""

    serializer_class = GitHubOAuthAuthorizeSerializer

    def get(self, request: Request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = build_oauth_authorization_url(
            provider="github",
            redirect=serializer.validated_data.get("redirect", ""),
        )
        return success_response(data=result, message="获取 GitHub 授权地址成功")


class GitHubOAuthCallbackView(OAuthCallbackView):
    """兼容旧 GitHub OAuth 回调接口。"""

    serializer_class = GitHubOAuthCallbackSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = complete_oauth_callback(
            provider="github",
            code=serializer.validated_data["code"],
            state=serializer.validated_data["state"],
            request=request._request,
        )
        if result["status"] == "requires_account_choice":
            return success_response(data=result, message="请选择 GitHub 账号绑定方式")
        return success_response(
            data={
                "status": result["status"],
                "user": UserSerializer(result["user"]).data,
                "access": result["access"],
                "refresh": result["refresh"],
                "redirect": result["redirect"],
            },
            message="GitHub 登录成功",
        )


class LogoutView(GenericAPIView):
    """用户登出接口。

    POST /api/v1/auth/logout/
    将 refresh token 加入黑名单，使其失效。
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request: Request):
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

    def post(self, request: Request, *args, **kwargs):
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


class ChangePasswordView(GenericAPIView):
    """修改密码接口。

    POST /api/v1/auth/change-password/
    需要认证，验证旧密码后设置新密码。
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
            request=request._request,
        )

        return success_response(message="密码修改成功")
