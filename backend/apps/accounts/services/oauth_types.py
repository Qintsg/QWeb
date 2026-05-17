#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
OAuth 服务共享类型。
@Project : QWeb
@File : oauth_types.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OAuthProfile:
    """第三方账号资料快照。"""

    provider: str
    provider_account_id: str
    provider_username: str
    provider_nickname: str
    provider_email: str
    provider_email_verified: bool | None
    provider_avatar_url: str
    profile_url: str
    raw_profile: dict[str, Any]
