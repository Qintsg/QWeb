#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
accounts 模块 URL 路由配置。
@Project : QWeb
@File : urls.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.api.views.auth_views import (
    LoginView,
    LogoutView,
    OAuthAuthorizeView,
    OAuthBindView,
    OAuthCallbackView,
    OAuthRegisterView,
    RegisterView,
    TokenRefreshView,
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
    path("auth/oauth/<str:provider>/authorize/", OAuthAuthorizeView.as_view(), name="oauth-authorize"),
    path("auth/oauth/<str:provider>/callback/", OAuthCallbackView.as_view(), name="oauth-callback"),
    path("auth/oauth/<str:provider>/bind/", OAuthBindView.as_view(), name="oauth-bind"),
    path("auth/oauth/<str:provider>/register/", OAuthRegisterView.as_view(), name="oauth-register"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # ---- 当前用户 ----
    path("me/", MeView.as_view(), name="me"),
    path("me/password/", MePasswordView.as_view(), name="me-password"),
    # ---- 用户管理（管理员） ----
    path("", include(router.urls)),
]
