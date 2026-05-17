#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
实现 core 应用的 Django 管理命令。
@Project : QWeb
@File : runserver.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.contrib.staticfiles.management.commands.runserver import Command as StaticfilesRunserverCommand


class Command(StaticfilesRunserverCommand):
    """实现当前 Django 管理命令。"""
    default_port = "8000"
