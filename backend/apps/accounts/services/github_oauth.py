"""GitHub OAuth 登录服务。"""

from __future__ import annotations

import secrets
from typing import Any
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core import signing
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import OAuthIdentity, UserProfile
from apps.audit.services.audit_service import log_action
from apps.audit.services.login_audit import log_login, log_login_failed
from apps.core.exceptions import AuthenticationFailedException, ValidationException

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"
GITHUB_STATE_SALT = "accounts.github_oauth_state"


def build_github_authorization_url(*, redirect: str = "") -> dict[str, str]:
    """生成 GitHub OAuth 授权地址。"""
    config = _get_github_oauth_config()
    nonce = secrets.token_urlsafe(24)
    state = signing.dumps(
        {
            "nonce": nonce,
            "redirect": _normalize_frontend_redirect(redirect),
        },
        salt=GITHUB_STATE_SALT,
    )
    query = urlencode(
        {
            "client_id": config["client_id"],
            "redirect_uri": config["callback_url"],
            "scope": "read:user user:email",
            "state": state,
            "allow_signup": "true",
        }
    )
    return {
        "authorization_url": f"{GITHUB_AUTHORIZE_URL}?{query}",
        "state": state,
    }


def complete_github_login(
    *,
    code: str,
    state: str,
    request=None,
) -> dict[str, Any]:
    """完成 GitHub OAuth 回调并签发本地 JWT。"""
    state_payload = _load_state(state)
    access_token = _exchange_code_for_token(code=code)
    github_user = _fetch_github_user(access_token)
    primary_email = _resolve_github_email(access_token, github_user)

    provider_user_id = str(github_user["id"])
    provider_username = str(github_user.get("login") or provider_user_id)

    inactive_account = False
    identity: OAuthIdentity | None = None
    with transaction.atomic():
        identity = (
            OAuthIdentity.objects.select_related("user")
            .filter(
                provider=OAuthIdentity.Provider.GITHUB,
                provider_user_id=provider_user_id,
            )
            .first()
        )

        if identity:
            user = identity.user
            created_user = False
        else:
            user, created_user = _find_or_create_user_from_github(
                provider_username=provider_username,
                email=primary_email,
                github_user=github_user,
            )
            if user.is_active:
                identity = OAuthIdentity.objects.create(
                    user=user,
                    provider=OAuthIdentity.Provider.GITHUB,
                    provider_user_id=provider_user_id,
                )

        if not user.is_active:
            inactive_account = True
        else:
            if identity is None:
                raise AuthenticationFailedException(message="GitHub 身份绑定失败，请稍后重试")
            _update_identity(identity=identity, github_user=github_user, email=primary_email)
            _update_user_profile(user=user, github_user=github_user)

    if inactive_account:
        log_login_failed(username=provider_username, reason="GitHub 绑定账号已被禁用", request=request)
        raise AuthenticationFailedException(message="账号已被禁用，请联系管理员")

    log_login(user=user, request=request)
    log_action(
        user=user,
        action="login",
        module="accounts",
        resource="oauth.github",
        resource_id=str(identity.pk),
        detail={"provider_username": provider_username, "created_user": created_user},
        request=request,
    )

    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "redirect": state_payload.get("redirect", "/dashboard"),
    }


def _get_github_oauth_config() -> dict[str, str]:
    client_id = getattr(settings, "GITHUB_OAUTH_CLIENT_ID", "")
    client_secret = getattr(settings, "GITHUB_OAUTH_CLIENT_SECRET", "")
    callback_url = getattr(settings, "GITHUB_OAUTH_CALLBACK_URL", "")
    if not client_id or not client_secret or not callback_url:
        raise ValidationException(message="GitHub 登录未配置，请联系管理员")
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "callback_url": callback_url,
    }


def _normalize_frontend_redirect(redirect: str) -> str:
    if not redirect or not redirect.startswith("/") or redirect.startswith("//"):
        return "/dashboard"
    return redirect


def _load_state(state: str) -> dict[str, str]:
    try:
        payload = signing.loads(
            state,
            salt=GITHUB_STATE_SALT,
            max_age=getattr(settings, "GITHUB_OAUTH_STATE_MAX_AGE", 600),
        )
    except signing.BadSignature as exc:
        raise AuthenticationFailedException(message="GitHub 登录状态已失效，请重新登录") from exc
    if not isinstance(payload, dict) or "nonce" not in payload:
        raise AuthenticationFailedException(message="GitHub 登录状态无效，请重新登录")
    return payload


def _exchange_code_for_token(*, code: str) -> str:
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


def _resolve_github_email(access_token: str, github_user: dict[str, Any]) -> str:
    email = str(github_user.get("email") or "")
    if email:
        return email

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
    verified = [
        item for item in emails
        if item.get("verified") and item.get("email")
    ]
    selected = (primary_verified or verified or [{}])[0]
    selected_email = str(selected.get("email") or "")
    if not selected_email:
        raise AuthenticationFailedException(message="GitHub 账号没有可用的已验证邮箱")
    return selected_email


def _parse_github_response(response: requests.Response, fallback_message: str) -> Any:
    try:
        payload = response.json()
    except ValueError as exc:
        raise AuthenticationFailedException(message=fallback_message) from exc

    if response.status_code >= 400:
        message = payload.get("error_description") or payload.get("message") or fallback_message
        raise AuthenticationFailedException(message=str(message))
    return payload


def _find_or_create_user_from_github(
    *,
    provider_username: str,
    email: str,
    github_user: dict[str, Any],
) -> tuple[Any, bool]:
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.filter(email__iexact=email).first()
    if user:
        return user, False

    username = _build_unique_username(provider_username)
    display_name = str(github_user.get("name") or provider_username)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=None,
        display_name=display_name[:128],
    )
    user.set_unusable_password()
    user.save(update_fields=["password"])
    UserProfile.objects.create(
        user=user,
        avatar=str(github_user.get("avatar_url") or ""),
        bio=str(github_user.get("bio") or "")[:500],
    )
    return user, True


def _build_unique_username(provider_username: str) -> str:
    from django.contrib.auth import get_user_model

    User = get_user_model()
    base = "".join(
        char if char.isalnum() or char == "_" else "_"
        for char in provider_username.lower()
    ).strip("_")[:48] or "github_user"
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f"{base}_{suffix}"
    return username


def _update_identity(
    *,
    identity: OAuthIdentity,
    github_user: dict[str, Any],
    email: str,
) -> None:
    identity.provider_username = str(github_user.get("login") or "")
    identity.email = email
    identity.avatar_url = str(github_user.get("avatar_url") or "")
    identity.profile_url = str(github_user.get("html_url") or "")
    identity.last_login_at = timezone.now()
    identity.save(
        update_fields=[
            "provider_username",
            "email",
            "avatar_url",
            "profile_url",
            "last_login_at",
            "updated_at",
        ]
    )


def _update_user_profile(*, user, github_user: dict[str, Any]) -> None:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    update_fields = ["updated_at"]
    avatar_url = str(github_user.get("avatar_url") or "")
    if avatar_url and not profile.avatar:
        profile.avatar = avatar_url
        update_fields.append("avatar")
    bio = str(github_user.get("bio") or "")
    if bio and not profile.bio:
        profile.bio = bio[:500]
        update_fields.append("bio")
    if len(update_fields) > 1:
        profile.save(update_fields=update_fields)
