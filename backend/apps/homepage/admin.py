#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
注册当前模块的 Django Admin 配置。
@Project : QWeb
@File : admin.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.contrib import admin

from apps.homepage.models import ServiceLink, SiteMetadata


@admin.register(SiteMetadata)
class SiteMetadataAdmin(admin.ModelAdmin):
    """定义站点元数据 Django Admin 管理界面配置。"""

    list_display = ("site_name", "site_title", "updated_at")
    search_fields = ("site_name", "site_title", "subtitle")


@admin.register(ServiceLink)
class ServiceLinkAdmin(admin.ModelAdmin):
    """定义 Django Admin 管理界面配置。"""
    list_display = ("title", "category", "sort_order", "is_visible", "created_at")
    list_filter = ("category", "is_visible")
    search_fields = ("title", "url", "description")
    ordering = ("sort_order", "created_at")
