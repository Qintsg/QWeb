"""GitHub OAuth provider 接入。"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import requests
from django.conf import settings

from apps.accounts.models import UserOAuthAccount
from apps.accounts.services.oauth_types import OAuthProfile
from apps.core.exceptions import AuthenticationFailedException, ValidationException

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"


def build_github_authorization_url(*, state: str) -> str:
    """生成 GitHub OAuth 授权地址。"""
    config = _get_github_oauth_config()
    query = urlencode(
        {
            "client_id": config["client_id"],
            "redirect_uri": config["callback_url"],
            "scope": "read:user user:email",
            "state": state,
            "allow_signup": "true",
        }
    )
    return f"{GITHUB_AUTHORIZE_URL}?{query}"


def fetch_github_profile(*, code: str) -> OAuthProfile:
    """使用授权码读取 GitHub 用户资料。"""
    access_token = _exchange_github_code_for_token(code=code)
    github_user = _fetch_github_user(access_token)
    email, email_verified = _resolve_github_email(access_token, github_user)
    return OAuthProfile(
        provider=UserOAuthAccount.Provider.GITHUB,
        provider_account_id=str(github_user["id"]),
        provider_username=str(github_user.get("login") or github_user["id"]),
        provider_nickname=str(github_user.get("name") or github_user.get("login") or ""),
        provider_email=email,
        provider_email_verified=email_verified,
        provider_avatar_url=str(github_user.get("avatar_url") or ""),
        profile_url=str(github_user.get("html_url") or ""),
        raw_profile=github_user,
    )


def _get_github_oauth_config() -> dict[str, str]:
    client_id = getattr(settings, "GITHUB_OAUTH_CLIENT_ID", "")
    client_secret = getattr(settings, "GITHUB_OAUTH_CLIENT_SECRET", "")
    callback_url = getattr(settings, "GITHUB_OAUTH_CALLBACK_URL", "")
    if not client_id or not client_secret or not callback_url:
        raise ValidationException(message="GitHub 登录未配置，请联系管理员")
    return {"client_id": client_id, "client_secret": client_secret, "callback_url": callback_url}


def _exchange_github_code_for_token(*, code: str) -> str:
    config = _get_github_oauth_config()
    try:
        response = requests.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "code": code,
                "redirect_uri": config["callback_url"],
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise AuthenticationFailedException(message="无法连接 GitHub 登录服务") from exc

    token_payload = _parse_github_response(response, "GitHub 授权码换取失败")
    access_token = token_payload.get("access_token")
    if not access_token:
        raise AuthenticationFailedException(message="GitHub 未返回访问令牌")
    return str(access_token)


def _fetch_github_user(access_token: str) -> dict[str, Any]:
    try:
        response = requests.get(
            GITHUB_USER_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        raise AuthenticationFailedException(message="无法读取 GitHub 用户信息") from exc
    payload = _parse_github_response(response, "GitHub 用户信息读取失败")
    if "id" not in payload or "login" not in payload:
        raise AuthenticationFailedException(message="GitHub 用户信息不完整")
    return payload


def _resolve_github_email(access_token: str, github_user: dict[str, Any]) -> tuple[str, bool | None]:
    email = str(github_user.get("email") or "")
    if email:
        return email, None

    try:
        response = requests.get(
            GITHUB_EMAILS_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        raise AuthenticationFailedException(message="无法读取 GitHub 邮箱信息") from exc

    emails = _parse_github_response(response, "GitHub 邮箱信息读取失败")
    if not isinstance(emails, list):
        raise AuthenticationFailedException(message="GitHub 邮箱信息格式无效")

    primary_verified = [
        item for item in emails
        if item.get("primary") and item.get("verified") and item.get("email")
    ]
    verified = [item for item in emails if item.get("verified") and item.get("email")]
    selected = (primary_verified or verified or [{}])[0]
    selected_email = str(selected.get("email") or "")
    return selected_email, bool(selected.get("verified")) if selected_email else None


def _parse_github_response(response: requests.Response, fallback_message: str) -> Any:
    try:
        payload = response.json()
    except ValueError as exc:
        raise AuthenticationFailedException(message=fallback_message) from exc

    if response.status_code >= 400:
        message = payload.get("error_description") or payload.get("message") or fallback_message
        raise AuthenticationFailedException(message=str(message))
    return payload
