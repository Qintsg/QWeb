#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
站点元数据模型。
@Project : QWeb
@File : site_metadata.py
@Author : Qintsg
@Date : 2026-05-18 12:10
'''
from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class SiteMetadata(BaseModel):
    """站点公开品牌元数据。"""

    site_name = models.CharField(max_length=100, default="QWeb", verbose_name="站点名称")
    site_title = models.CharField(max_length=150, default="Qintsg's Web", verbose_name="浏览器标题")
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        default="把服务入口、身份权限、审计记录和个人项目收束到一个可控门户。",
        verbose_name="站点副标题",
    )
    logo_url = models.URLField(max_length=500, blank=True, default="", verbose_name="Logo 地址")
    favicon_url = models.URLField(max_length=500, blank=True, default="", verbose_name="favicon 地址")
    brand_initial = models.CharField(max_length=4, blank=True, default="Q", verbose_name="品牌首字母")

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "homepage_site_metadata"
        verbose_name = "站点元数据"
        verbose_name_plural = "站点元数据"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        return self.site_name
