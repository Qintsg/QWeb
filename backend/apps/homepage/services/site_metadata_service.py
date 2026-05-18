#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
站点元数据服务。
@Project : QWeb
@File : site_metadata_service.py
@Author : Qintsg
@Date : 2026-05-18 12:10
'''
from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from apps.audit.services.audit_service import log_action
from apps.homepage.models import SiteMetadata


def get_site_metadata() -> SiteMetadata:
    """
    获取当前站点元数据；不存在时创建默认记录。
    :return: 站点元数据对象。
    """
    metadata = SiteMetadata.objects.order_by("created_at").first()
    if metadata is not None:
        return metadata
    return SiteMetadata.objects.create()


def update_site_metadata(
    *,
    fields: dict[str, Any],
    operator: Any | None = None,
    request: HttpRequest | None = None,
) -> SiteMetadata:
    """
    更新站点元数据。
    :param fields: 已通过序列化器校验的字段。
    :param operator: 当前操作人。
    :param request: HTTP 请求对象。
    :return: 更新后的站点元数据对象。
    """
    metadata = get_site_metadata()
    for field_name, value in fields.items():
        setattr(metadata, field_name, value)
    metadata.updated_by = operator
    metadata.save()

    log_action(
        user=operator,
        action="update",
        module="homepage",
        resource="site_metadata",
        resource_id=str(metadata.pk),
        detail={"fields": sorted(fields.keys())},
        request=request,
    )
    return metadata
