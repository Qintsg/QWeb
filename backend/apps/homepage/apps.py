#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
定义当前 Django 应用配置。
@Project : QWeb
@File : apps.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.apps import AppConfig


class HomepageConfig(AppConfig):
    """声明当前 Django 应用的配置。"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.homepage"
    verbose_name = "首页管理"
