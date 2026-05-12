"""Provider 化 OAuth 登录服务。"""

from __future__ import annotations

import secrets
from typing import Any

from django.conf import settings
from django.core import signing
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import UserContact, UserOAuthAccount, UserProfile
from apps.accounts.services.account_bootstrap import ensure_user_related_records
from apps.accounts.services.auth_service import authenticate_user
from apps.accounts.services.github_oauth_provider import (
    build_github_authorization_url,
    fetch_github_profile,
)
from apps.accounts.services.oauth_types import OAuthProfile
from apps.accounts.services.token_service import issue_token_pair
from apps.accounts.services.username_policy import is_username_available, validate_username_policy
from apps.audit.models import LoginLog
from apps.audit.services.audit_service import log_action
from apps.audit.services.login_audit import log_login_failed, log_oauth_login
from apps.core.exceptions import AuthenticationFailedException, ConflictException, ValidationException

OAUTH_STATE_SALT = "accounts.oauth_state"
OAUTH_PENDING_SALT = "accounts.oauth_pending"


def build_oauth_authorization_url(*, provider: str, redirect: str = "") -> dict[str, str]:
    """生成 OAuth 授权地址。"""
    provider = _normalize_provider(provider)
    if provider != UserOAuthAccount.Provider.GITHUB:
        raise ValidationException(message="暂不支持该第三方登录平台")

    state = signing.dumps(
        {
            "provider": provider,
            "nonce": secrets.token_urlsafe(24),
            "redirect": _normalize_frontend_redirect(redirect),
        },
        salt=OAUTH_STATE_SALT,
    )
    return {
        "authorization_url": build_github_authorization_url(state=state),
        "state": state,
        "provider": provider,
    }


def complete_oauth_callback(
    *,
    provider: str,
    code: str,
    state: str,
    request=None,
) -> dict[str, Any]:
    """完成 OAuth 回调，返回已登录或待选择账号状态。"""
    provider = _normalize_provider(provider)
    state_payload = _load_state(state, expected_provider=provider)
    profile = _fetch_provider_profile(provider=provider, code=code)

    identity = (
        UserOAuthAccount.objects.select_related("user")
        .filter(provider=provider, provider_account_id=profile.provider_account_id)
        .first()
    )
    if identity:
        user = identity.user
        if not user.is_active or user.status != user.Status.ACTIVE:
            log_login_failed(
                username=profile.provider_username,
                reason="OAuth 绑定账号不可用",
                request=request,
                login_type="oauth",
                provider=provider,
            )
            raise AuthenticationFailedException(message="账号已被禁用或不可用，请联系管理员")

        _update_oauth_account(identity=identity, profile=profile)
        log_oauth_login(user=user, provider=provider, request=request)
        tokens = issue_token_pair(user=user, request=request)
        return {
            "status": "authenticated",
            "user": user,
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "redirect": state_payload.get("redirect", "/dashboard"),
        }

    pending_token = _dump_pending_profile(profile=profile, redirect=state_payload.get("redirect", "/dashboard"))
    email_hint_exists = bool(
        profile.provider_email
        and UserContact.objects.filter(email__iexact=profile.provider_email).exists()
    )
    return {
        "status": "requires_account_choice",
        "provider": provider,
        "pending_token": pending_token,
        "suggested_username": _suggest_username(profile.provider_username),
        "suggested_nickname": profile.provider_nickname or profile.provider_username,
        "provider_email": profile.provider_email,
        "provider_email_verified": profile.provider_email_verified,
        "provider_avatar_url": profile.provider_avatar_url,
        "email_matches_existing_account": email_hint_exists,
        "redirect": state_payload.get("redirect", "/dashboard"),
    }


def bind_oauth_to_existing_user(
    *,
    provider: str,
    pending_token: str,
    login: str,
    password: str,
    request=None,
) -> dict[str, Any]:
    """用户登录已有账号后绑定第三方账号。"""
    provider = _normalize_provider(provider)
    pending_payload = _load_pending_profile(pending_token, expected_provider=provider)
    auth_result = authenticate_user(login=login, password=password, request=request)
    user = auth_result["user"]
    profile = _profile_from_payload(pending_payload)

    with transaction.atomic():
        account = _create_or_update_oauth_account(user=user, profile=profile)
        _apply_oauth_profile_to_user(user=user, profile=profile, fill_existing_only=True)

    log_oauth_login(
        user=user,
        provider=provider,
        request=request,
        action=LoginLog.Action.OAUTH_BIND,
    )
    log_action(
        user=user,
        action="create",
        module="accounts",
        resource="oauth_account",
        resource_id=str(account.pk),
        detail={"provider": provider, "provider_username": profile.provider_username},
        request=request,
    )

    return {
        "status": "authenticated",
        "user": user,
        "access": auth_result["access"],
        "refresh": auth_result["refresh"],
        "redirect": pending_payload.get("redirect", "/dashboard"),
    }


def register_user_from_oauth(
    *,
    provider: str,
    pending_token: str,
    username: str,
    nickname: str = "",
    request=None,
) -> dict[str, Any]:
    """用户确认不绑定已有账号后创建新账号并绑定 OAuth。"""
    provider = _normalize_provider(provider)
    pending_payload = _load_pending_profile(pending_token, expected_provider=provider)
    profile = _profile_from_payload(pending_payload)
    username = validate_username_policy(username)
    nickname = nickname.strip() or profile.provider_nickname or username
    contact_email = _available_contact_email(profile.provider_email)

    with transaction.atomic():
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            username=username,
            email=contact_email,
            password=None,
            nickname=nickname[:64],
            avatar_url=profile.provider_avatar_url or None,
        )
        user.set_unusable_password()
        user.save(update_fields=["password", "updated_at"])
        ensure_user_related_records(
            user=user,
            email=contact_email,
            email_verified=bool(contact_email and profile.provider_email_verified),
        )
        _apply_oauth_profile_to_user(user=user, profile=profile, fill_existing_only=True)
        account = _create_or_update_oauth_account(user=user, profile=profile)

    log_oauth_login(
        user=user,
        provider=provider,
        request=request,
        action=LoginLog.Action.OAUTH_REGISTER,
    )
    log_action(
        user=user,
        action="create",
        module="accounts",
        resource="user.oauth",
        resource_id=str(user.uid),
        detail={"provider": provider, "oauth_account_id": account.pk},
        request=request,
    )

    tokens = issue_token_pair(user=user, request=request)
    return {
        "status": "authenticated",
        "user": user,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
        "redirect": pending_payload.get("redirect", "/dashboard"),
    }


def _normalize_provider(provider: str) -> str:
    normalized = provider.strip().lower()
    if normalized != UserOAuthAccount.Provider.GITHUB:
        raise ValidationException(message="暂不支持该第三方登录平台")
    return normalized


def _normalize_frontend_redirect(redirect: str) -> str:
    if not redirect or not redirect.startswith("/") or redirect.startswith("//"):
        return "/dashboard"
    return redirect


def _load_state(state: str, *, expected_provider: str) -> dict[str, Any]:
    try:
        payload = signing.loads(
            state,
            salt=OAUTH_STATE_SALT,
            max_age=getattr(settings, "GITHUB_OAUTH_STATE_MAX_AGE", 600),
        )
    except signing.BadSignature as exc:
        raise AuthenticationFailedException(message="第三方登录状态已失效，请重新登录") from exc
    if not isinstance(payload, dict) or payload.get("provider") != expected_provider:
        raise AuthenticationFailedException(message="第三方登录状态无效，请重新登录")
    return payload


def _fetch_provider_profile(*, provider: str, code: str) -> OAuthProfile:
    if provider == UserOAuthAccount.Provider.GITHUB:
        return fetch_github_profile(code=code)
    raise ValidationException(message="暂不支持该第三方登录平台")


def _dump_pending_profile(*, profile: OAuthProfile, redirect: str) -> str:
    return signing.dumps(
        {
            "provider": profile.provider,
            "provider_account_id": profile.provider_account_id,
            "provider_username": profile.provider_username,
            "provider_nickname": profile.provider_nickname,
            "provider_email": profile.provider_email,
            "provider_email_verified": profile.provider_email_verified,
            "provider_avatar_url": profile.provider_avatar_url,
            "profile_url": profile.profile_url,
            "raw_profile": profile.raw_profile,
            "redirect": _normalize_frontend_redirect(redirect),
        },
        salt=OAUTH_PENDING_SALT,
    )


def _load_pending_profile(pending_token: str, *, expected_provider: str) -> dict[str, Any]:
    try:
        payload = signing.loads(
            pending_token,
            salt=OAUTH_PENDING_SALT,
            max_age=getattr(settings, "GITHUB_OAUTH_STATE_MAX_AGE", 600),
        )
    except signing.BadSignature as exc:
        raise AuthenticationFailedException(message="第三方登录待绑定状态已失效，请重新登录") from exc
    if not isinstance(payload, dict) or payload.get("provider") != expected_provider:
        raise AuthenticationFailedException(message="第三方登录待绑定状态无效，请重新登录")
    return payload


def _profile_from_payload(payload: dict[str, Any]) -> OAuthProfile:
    return OAuthProfile(
        provider=str(payload["provider"]),
        provider_account_id=str(payload["provider_account_id"]),
        provider_username=str(payload.get("provider_username") or ""),
        provider_nickname=str(payload.get("provider_nickname") or ""),
        provider_email=str(payload.get("provider_email") or ""),
        provider_email_verified=payload.get("provider_email_verified"),
        provider_avatar_url=str(payload.get("provider_avatar_url") or ""),
        profile_url=str(payload.get("profile_url") or ""),
        raw_profile=dict(payload.get("raw_profile") or {}),
    )


def _suggest_username(provider_username: str) -> str:
    base = "".join(
        char if char.isalnum() or char in ".-_" else "_"
        for char in provider_username
    ).strip(".-_")[:32] or "oauth_user"
    if is_username_available(base):
        return base
    for suffix in range(2, 1000):
        candidate = f"{base[:28]}_{suffix}"
        if is_username_available(candidate):
            return candidate
    return ""


def _create_or_update_oauth_account(*, user, profile: OAuthProfile) -> UserOAuthAccount:
    account = UserOAuthAccount.objects.filter(
        provider=profile.provider,
        provider_account_id=profile.provider_account_id,
    ).first()
    if account:
        if account.user_id != user.pk:
            raise ConflictException(message="该第三方账号已绑定到其他用户")
        _update_oauth_account(identity=account, profile=profile)
        return account
    if UserOAuthAccount.objects.filter(user=user, provider=profile.provider).exists():
        raise ConflictException(message="该用户已绑定该第三方平台账号")

    account = UserOAuthAccount.objects.create(
        user=user,
        provider=profile.provider,
        provider_account_id=profile.provider_account_id,
        provider_username=profile.provider_username or None,
        provider_nickname=profile.provider_nickname or None,
        provider_email=profile.provider_email or None,
        provider_email_verified=profile.provider_email_verified,
        provider_avatar_url=profile.provider_avatar_url or None,
        raw_profile=profile.raw_profile,
    )
    return account


def _update_oauth_account(*, identity: UserOAuthAccount, profile: OAuthProfile) -> None:
    identity.provider_username = profile.provider_username or None
    identity.provider_nickname = profile.provider_nickname or None
    identity.provider_email = profile.provider_email or None
    identity.provider_email_verified = profile.provider_email_verified
    identity.provider_avatar_url = profile.provider_avatar_url or None
    identity.raw_profile = profile.raw_profile
    identity.updated_at = timezone.now()
    identity.save(
        update_fields=[
            "provider_username",
            "provider_nickname",
            "provider_email",
            "provider_email_verified",
            "provider_avatar_url",
            "raw_profile",
            "updated_at",
        ]
    )


def _apply_oauth_profile_to_user(*, user, profile: OAuthProfile, fill_existing_only: bool) -> None:
    update_fields: list[str] = []
    if profile.provider_avatar_url and (not fill_existing_only or not user.avatar_url):
        user.avatar_url = profile.provider_avatar_url
        update_fields.append("avatar_url")
    if profile.provider_nickname and (not fill_existing_only or not user.nickname):
        user.nickname = profile.provider_nickname[:64]
        update_fields.append("nickname")
    if update_fields:
        update_fields.append("updated_at")
        user.save(update_fields=update_fields)

    if profile.provider == UserOAuthAccount.Provider.GITHUB:
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        if profile.profile_url and not user_profile.github:
            user_profile.github = profile.profile_url
            user_profile.save(update_fields=["github", "updated_at"])


def _available_contact_email(email: str) -> str:
    """返回可写入 user_contact 的邮箱；被占用时只保留在 OAuth 快照中。"""
    if not email:
        return ""
    if UserContact.objects.filter(email__iexact=email).exists():
        return ""
    return email
