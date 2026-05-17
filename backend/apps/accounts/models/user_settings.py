#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户设置模型。
@Project : QWeb
@File : user_settings.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from django.conf import settings
from django.db import models


class UserSettings(models.Model):
    """用户语言、时区、主题与偏好设置。"""

    class Theme(models.TextChoices):
        """定义当前字段的可选枚举值。"""
        LIGHT = "light", "浅色"
        DARK = "dark", "深色"
        SYSTEM = "system", "跟随系统"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="uid",
        related_name="settings",
        verbose_name="用户",
    )
    language = models.CharField(max_length=32, default="zh-CN", verbose_name="语言偏好")
    timezone = models.CharField(max_length=64, default="Asia/Shanghai", verbose_name="时区")
    theme = models.CharField(
        max_length=32,
        choices=Theme.choices,
        default=Theme.SYSTEM,
        verbose_name="主题",
    )
    notification_settings = models.JSONField(default=dict, blank=True, verbose_name="通知设置")
    privacy_settings = models.JSONField(default=dict, blank=True, verbose_name="隐私设置")
    preferences = models.JSONField(default=dict, blank=True, verbose_name="其他偏好设置")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "user_settings"
        verbose_name = "用户设置"
        verbose_name_plural = "用户设置"

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        return f"{self.user.username} 的设置"
