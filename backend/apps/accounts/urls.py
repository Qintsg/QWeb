"""accounts 模块 URL 路由配置。

路由前缀由 config/urls.py 中 api/v1/ 挂载。
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.api.views.auth_views import (
    ChangePasswordView,
    GitHubOAuthAuthorizeView,
    GitHubOAuthCallbackView,
    LoginView,
    LogoutView,
    RegisterView,
)
from apps.accounts.api.views.me_views import MePasswordView, MeView
from apps.accounts.api.views.user_views import UserViewSet

app_name = "accounts"

router = DefaultRouter(trailing_slash=True)
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    # ---- 认证 ----
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/github/authorize/", GitHubOAuthAuthorizeView.as_view(), name="github-authorize"),
    path("auth/github/callback/", GitHubOAuthCallbackView.as_view(), name="github-callback"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    # ---- 当前用户 ----
    path("me/", MeView.as_view(), name="me"),
    path("me/password/", MePasswordView.as_view(), name="me-password"),
    # ---- 用户管理（管理员） ----
    path("", include(router.urls)),
]
