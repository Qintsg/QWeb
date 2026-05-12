#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
定义当前模块的 API 视图。
@Project : QWeb
@File : views.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from django.http import JsonResponse
from django.http import HttpRequest
from django.http import HttpResponse


def healthcheck(request: HttpRequest) -> HttpResponse:
    """执行 healthcheck 对应的业务逻辑。"""
    return JsonResponse({"status": "ok", "service": "qweb-backend"})
