"""认证相关序列化器。

包含注册、登录、Token 刷新、修改密码等接口的数据校验。
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import UserContact
from apps.accounts.services.username_policy import validate_username_policy

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """用户注册请求。

    校验规则：
    - username: 3~32 字符，大小写不敏感唯一
    - email: 合法邮箱且未被注册
    - password: 至少 8 位，需通过 Django 密码验证器
    - password_confirm: 必须与 password 一致
    """

    username = serializers.CharField(
        min_length=3,
        max_length=32,
        help_text="用户名，3~32 个字符。",
    )
    email = serializers.EmailField(
        help_text="邮箱地址，需唯一。",
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="密码，至少 8 个字符。",
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="确认密码，必须与密码一致。",
    )

    def validate_username(self, value: str) -> str:
        """检查用户名规则和唯一性。"""
        try:
            return validate_username_policy(value)
        except Exception as exc:
            raise serializers.ValidationError(getattr(exc, "message", "用户名不可用")) from exc

    def validate_email(self, value: str) -> str:
        """检查邮箱唯一性。"""
        if UserContact.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value.strip()

    def validate_password(self, value: str) -> str:
        """使用 Django 内置密码验证器校验密码强度。"""
        validate_password(value)
        return value

    def validate(self, attrs: dict) -> dict:
        """校验两次密码是否一致。"""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "两次密码输入不一致"})
        return attrs


class LoginSerializer(serializers.Serializer):
    """用户登录请求。

    支持用户名或邮箱 + 密码方式登录。
    """

    login = serializers.CharField(
        help_text="用户名或邮箱。",
    )
    password = serializers.CharField(
        write_only=True,
        help_text="密码。",
    )


class GitHubOAuthAuthorizeSerializer(serializers.Serializer):
    """GitHub OAuth 授权地址请求。"""

    redirect = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="登录成功后回到前端的相对路径。",
    )


class GitHubOAuthCallbackSerializer(serializers.Serializer):
    """GitHub OAuth 回调换取本地 Token 请求。"""

    code = serializers.CharField(help_text="GitHub 回调返回的授权码。")
    state = serializers.CharField(help_text="后端签名生成的 OAuth state。")


class OAuthAuthorizeSerializer(serializers.Serializer):
    """第三方 OAuth 授权地址请求。"""

    redirect = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="登录成功后回到前端的相对路径。",
    )


class OAuthCallbackSerializer(serializers.Serializer):
    """第三方 OAuth 回调请求。"""

    code = serializers.CharField(help_text="第三方平台回调返回的授权码。")
    state = serializers.CharField(help_text="后端签名生成的 OAuth state。")


class OAuthBindSerializer(serializers.Serializer):
    """绑定第三方账号到已有账号。"""

    pending_token = serializers.CharField(help_text="待绑定 OAuth 状态令牌。")
    login = serializers.CharField(help_text="已有账号用户名、邮箱或手机号。")
    password = serializers.CharField(write_only=True, help_text="已有账号密码。")


class OAuthRegisterSerializer(serializers.Serializer):
    """第三方账号自动注册请求。"""

    pending_token = serializers.CharField(help_text="待注册 OAuth 状态令牌。")
    username = serializers.CharField(min_length=3, max_length=32)
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def validate_username(self, value: str) -> str:
        try:
            return validate_username_policy(value)
        except Exception as exc:
            raise serializers.ValidationError(getattr(exc, "message", "用户名不可用")) from exc


class LogoutSerializer(serializers.Serializer):
    """登出请求。"""

    refresh = serializers.CharField(help_text="需要吊销的 refresh token。")


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码请求。

    需要提供旧密码验证身份，并设置新密码。
    """

    old_password = serializers.CharField(
        write_only=True,
        help_text="当前密码。",
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="新密码，至少 8 个字符。",
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        help_text="确认新密码。",
    )

    def validate_new_password(self, value: str) -> str:
        """使用 Django 内置密码验证器校验新密码强度。"""
        validate_password(value)
        return value

    def validate(self, attrs: dict) -> dict:
        """校验新密码两次输入是否一致。"""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "两次新密码输入不一致"}
            )
        return attrs
