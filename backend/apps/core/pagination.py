#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
统一分页器。

输出格式：
{
    "code": 0,
    "message": "操作成功",
    "data": {
        "count": <总数>,
        "next": <下一页URL或null>,
        "previous": <上一页URL或null>,
        "results": [...]
    }
}
@Project : QWeb
@File : pagination.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from collections import OrderedDict
from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """全局标准分页器。

    默认每页 20 条，客户端可通过 page_size 参数调整（最大 100）。
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data: list[Any]) -> Response:
        """将分页结果包装为统一格式。"""
        return Response(
            OrderedDict(
                [
                    ("code", 0),
                    ("message", "操作成功"),
                    (
                        "data",
                        OrderedDict(
                            [
                                ("count", self.page.paginator.count),
                                ("next", self.get_next_link()),
                                ("previous", self.get_previous_link()),
                                ("results", data),
                            ]
                        ),
                    ),
                ]
            )
        )

    def get_paginated_response_schema(self, schema: dict) -> dict:
        """为 drf-spectacular 提供分页响应的 OpenAPI schema。"""
        return {
            "type": "object",
            "required": ["code", "message", "data"],
            "properties": {
                "code": {"type": "integer", "example": 0},
                "message": {"type": "string", "example": "操作成功"},
                "data": {
                    "type": "object",
                    "required": ["count", "results"],
                    "properties": {
                        "count": {"type": "integer", "example": 100},
                        "next": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": "http://api.example.com/items/?page=2",
                        },
                        "previous": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": None,
                        },
                        "results": schema,
                    },
                },
            },
        }
