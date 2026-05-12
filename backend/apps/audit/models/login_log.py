#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
登录审计日志模型。
@Project : QWeb
@File : login_log.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from django.conf import settings
from django.db import models


class LoginLog(models.Model):
    """
    登录行为审计日志。

    独立于通用审计日志，专门追踪登录相关事件：
    - 登录成功 / 登出 / 登录失败
    - 来源 IP、User-Agent
    - 失败原因
    """

    class Action(models.TextChoices):
        """登录操作类型。"""

        LOGIN = "login", "登录成功"
        LOGOUT = "logout", "登出"
        FAILED = "failed", "登录失败"
        OAUTH_BIND = "oauth_bind", "OAuth 绑定"
        OAUTH_REGISTER = "oauth_register", "OAuth 自动注册"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="uid",
        related_name="login_logs",
        verbose_name="用户",
    )
    username = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="登录用户名",
        help_text="登录失败时 user 可能为 null，此字段保留尝试的用户名",
    )
    login_type = models.CharField(
        max_length=32,
        default="password",
        db_index=True,
        verbose_name="登录方式",
    )
    provider = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="第三方平台",
    )
    action = models.CharField(
        max_length=32,
        choices=Action.choices,
        db_index=True,
        verbose_name="操作类型",
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP 地址",
    )
    user_agent = models.TextField(
        blank=True,
        default="",
        verbose_name="User-Agent",
    )
    device_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="设备信息",
    )
    success = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="是否登录成功",
    )
    failure_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name="失败原因",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="操作时间",
    )

    class Meta:
        """定义当前对象的 Django 元数据。"""
        db_table = "user_login_logs"
        ordering = ["-created_at"]
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志"

    def __str__(self) -> str:
        """返回对象的可读显示名称。"""
        name = self.user.username if self.user else self.username or "未知"
        return f"[{self.action}] {name} @ {self.ip_address}"
