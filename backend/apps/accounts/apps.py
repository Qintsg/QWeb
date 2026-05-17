#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
accounts 应用配置。
@Project : QWeb
@File : apps.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """用户账号模块。

    负责用户注册、登录、资料管理、密码管理等功能。
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "用户账号"
