#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
DRF 统一异常处理器。

拦截所有异常并转换为统一格式：
{"code": <int>, "message": <str>, "errors": <可选>}

在 settings.py 的 REST_FRAMEWORK.EXCEPTION_HANDLER 中注册。
@Project : QWeb
@File : exception_handler.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

import logging
from typing import Any

from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import status as http_status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.core.exceptions import BusinessException, ValidationException

logger = logging.getLogger("qweb.exception")


def unified_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """统一异常处理入口。

    处理顺序：
    1. BusinessException 及其子类 → 直接使用异常携带的 code / message
    2. DRF ValidationError → 提取字段校验错误
    3. DRF APIException → 映射为统一格式
    4. Django Http404 / PermissionDenied → 对应 404 / 403
    5. 其他未知异常 → 500 内部错误（生产环境隐藏细节）
    """

    # --- 1. 自定义业务异常 ---
    if isinstance(exc, ValidationException):
        return Response(
            {"code": exc.code, "message": exc.message, "errors": exc.errors},
            status=exc.status_code,
        )

    if isinstance(exc, BusinessException):
        return Response(
            {"code": exc.code, "message": exc.message},
            status=exc.status_code,
        )

    # --- 2. 先让 DRF 默认处理器尝试 ---
    response = drf_exception_handler(exc, context)

    if response is not None:
        # DRF ValidationError → 提取详细校验错误
        if isinstance(exc, ValidationError):
            return Response(
                {
                    "code": 4220,
                    "message": "参数校验失败",
                    "errors": response.data,
                },
                status=response.status_code,
            )

        # 其他 DRF APIException → 统一格式
        detail = response.data.get("detail", str(exc)) if isinstance(response.data, dict) else str(exc)
        return Response(
            {"code": response.status_code, "message": str(detail)},
            status=response.status_code,
        )

    # --- 3. Django 内置异常 ---
    if isinstance(exc, Http404):
        return Response(
            {"code": 4040, "message": "请求的资源不存在"},
            status=http_status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {"code": 4030, "message": "权限不足，拒绝访问"},
            status=http_status.HTTP_403_FORBIDDEN,
        )

    # --- 4. 未知异常 → 500 ---
    logger.exception("未处理的服务端异常", exc_info=exc)
    return Response(
        {"code": 5000, "message": "服务器内部错误，请稍后重试"},
        status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
