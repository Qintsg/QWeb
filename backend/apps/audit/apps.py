#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
审计模块应用配置。
@Project : QWeb
@File : apps.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.apps import AppConfig


class AuditConfig(AppConfig):
    """审计模块。"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    verbose_name = "审计日志"
