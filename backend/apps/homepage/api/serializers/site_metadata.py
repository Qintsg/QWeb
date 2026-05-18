#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
站点元数据序列化器。
@Project : QWeb
@File : site_metadata.py
@Author : Qintsg
@Date : 2026-05-18 12:10
'''
from __future__ import annotations

from rest_framework import serializers

from apps.homepage.models import SiteMetadata


class SiteMetadataSerializer(serializers.ModelSerializer):
    """站点元数据读写序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = SiteMetadata
        fields = [
            "id",
            "site_name",
            "site_title",
            "subtitle",
            "logo_url",
            "favicon_url",
            "brand_initial",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]
