#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
首页模块 URL 配置。
@Project : QWeb
@File : urls.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.urls import path

from apps.homepage.api.views.service_link import (
    ServiceLinkAdminDetailView,
    ServiceLinkAdminListCreateView,
    ServiceLinkPublicListView,
)
from apps.homepage.api.views.site_metadata import (
    SiteMetadataAdminView,
    SiteMetadataPublicView,
)

urlpatterns = [
    # 公开接口
    path("homepage/metadata/", SiteMetadataPublicView.as_view(), name="homepage-metadata-public"),
    path("homepage/links/", ServiceLinkPublicListView.as_view(), name="homepage-links-public"),
    # 管理接口
    path("homepage/admin/metadata/", SiteMetadataAdminView.as_view(), name="homepage-metadata-admin"),
    path("homepage/admin/links/", ServiceLinkAdminListCreateView.as_view(), name="homepage-links-admin-list"),
    path("homepage/admin/links/<uuid:pk>/", ServiceLinkAdminDetailView.as_view(), name="homepage-links-admin-detail"),
]
