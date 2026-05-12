#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
暴露 WSGI 应用入口。
@Project : QWeb
@File : wsgi.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
