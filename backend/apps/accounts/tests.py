"""accounts 核心规则测试。"""

from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase

from apps.accounts.models import UserContact, UserOAuthAccount
from apps.accounts.services.oauth_service import (
    OAUTH_STATE_SALT,
    complete_oauth_callback,
    register_user_from_oauth,
)
from apps.accounts.services.oauth_types import OAuthProfile
from apps.accounts.services.username_policy import validate_username_policy
from apps.core.exceptions import ValidationException


class UsernamePolicyTests(TestCase):
    """用户名注册规则测试。"""

    def test_accepts_valid_usernames(self):
        for username in ["qintsg", "qin.tsg", "qin-tsg", "qin_tsg", "Qin123"]:
            with self.subTest(username=username):
                self.assertEqual(validate_username_policy(username), username)

    def test_rejects_invalid_usernames(self):
        invalid_usernames = [
            "ab",
            ".qintsg",
            "qintsg.",
            "qin..tsg",
            "qin__tsg",
            "qin--tsg",
            "qin tsg",
            "qin@tsg",
            "admin",
        ]
        for username in invalid_usernames:
            with self.subTest(username=username):
                with self.assertRaises(ValidationException):
                    validate_username_policy(username)

    def test_rejects_case_insensitive_duplicate(self):
        User = get_user_model()
        User.objects.create_user(username="Qintsg", password="StrongPass123!")

        with self.assertRaises(ValidationException):
            validate_username_policy("qintsg")


class OAuthFirstLoginTests(TestCase):
    """OAuth 首次登录绑定规则测试。"""

    def test_matching_email_requires_account_choice_without_auto_bind(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="localuser",
            email="same@example.com",
            password="StrongPass123!",
        )
        UserContact.objects.update_or_create(user=user, defaults={"email": "same@example.com"})
        state = signing.dumps(
            {"provider": "github", "nonce": "test", "redirect": "/dashboard"},
            salt=OAUTH_STATE_SALT,
        )
        oauth_profile = OAuthProfile(
            provider="github",
            provider_account_id="github-1001",
            provider_username="githubuser",
            provider_nickname="GitHub User",
            provider_email="same@example.com",
            provider_email_verified=True,
            provider_avatar_url="https://example.com/avatar.png",
            profile_url="https://github.com/githubuser",
            raw_profile={"id": 1001, "login": "githubuser"},
        )

        with patch(
            "apps.accounts.services.oauth_service._fetch_provider_profile",
            return_value=oauth_profile,
        ):
            result = complete_oauth_callback(
                provider="github",
                code="oauth-code",
                state=state,
            )

        self.assertEqual(result["status"], "requires_account_choice")
        self.assertTrue(result["email_matches_existing_account"])
        self.assertEqual(
            UserOAuthAccount.objects.filter(
                provider="github",
                provider_account_id="github-1001",
            ).count(),
            0,
        )

    def test_oauth_register_keeps_duplicate_email_out_of_contact(self):
        User = get_user_model()
        existing_user = User.objects.create_user(
            username="existing",
            email="same@example.com",
            password="StrongPass123!",
        )
        UserContact.objects.update_or_create(
            user=existing_user,
            defaults={"email": "same@example.com"},
        )
        oauth_profile = OAuthProfile(
            provider="github",
            provider_account_id="github-1002",
            provider_username="newgithub",
            provider_nickname="New GitHub",
            provider_email="same@example.com",
            provider_email_verified=True,
            provider_avatar_url="",
            profile_url="https://github.com/newgithub",
            raw_profile={"id": 1002, "login": "newgithub"},
        )
        pending_token = signing.dumps(
            {
                "provider": oauth_profile.provider,
                "provider_account_id": oauth_profile.provider_account_id,
                "provider_username": oauth_profile.provider_username,
                "provider_nickname": oauth_profile.provider_nickname,
                "provider_email": oauth_profile.provider_email,
                "provider_email_verified": oauth_profile.provider_email_verified,
                "provider_avatar_url": oauth_profile.provider_avatar_url,
                "profile_url": oauth_profile.profile_url,
                "raw_profile": oauth_profile.raw_profile,
                "redirect": "/dashboard",
            },
            salt="accounts.oauth_pending",
        )

        result = register_user_from_oauth(
            provider="github",
            pending_token=pending_token,
            username="oauthnew",
            nickname="OAuth New",
        )

        self.assertEqual(result["status"], "authenticated")
        self.assertEqual(result["user"].contact.email, None)
        oauth_account = UserOAuthAccount.objects.get(provider_account_id="github-1002")
        self.assertEqual(oauth_account.provider_email, "same@example.com")
