#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
审计模块 URL 配置。
@Project : QWeb
@File : urls.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.urls import path

from apps.audit.api.views import AuditLogListView, LoginLogListView

app_name = "audit"

urlpatterns = [
    path("logs/", AuditLogListView.as_view(), name="audit-log-list"),
    path("login-logs/", LoginLogListView.as_view(), name="login-log-list"),
]
