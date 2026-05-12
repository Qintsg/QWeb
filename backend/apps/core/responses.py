#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
统一 API 响应格式工具。

所有 API 响应均使用本模块提供的函数，保证返回格式一致：
成功: {"code": 0, "message": "...", "data": ...}
失败: {"code": <非零>, "message": "...", "errors": ...}
@Project : QWeb
@File : responses.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 0,
    status: int = http_status.HTTP_200_OK,
) -> Response:
    """构建统一的成功响应。

    :param data: 响应数据体。
    :param message: 提示消息。
    :param code: 业务状态码，0 代表成功。
    :param status: HTTP 状态码，默认 200。
    """
    return Response(
        {"code": code, "message": message, "data": data},
        status=status,
    )


def error_response(
    message: str = "操作失败",
    code: int = 1,
    errors: Any = None,
    status: int = http_status.HTTP_400_BAD_REQUEST,
) -> Response:
    """构建统一的错误响应。

    :param message: 错误消息。
    :param code: 业务错误码，非零。
    :param errors: 详细错误信息（如字段校验错误）。
    :param status: HTTP 状态码，默认 400。
    """
    payload: dict[str, Any] = {"code": code, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status)
