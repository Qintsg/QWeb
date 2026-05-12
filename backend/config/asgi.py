#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
暴露 ASGI 应用入口。
@Project : QWeb
@File : asgi.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
