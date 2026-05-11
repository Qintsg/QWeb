"""认证相关序列化器。

包含注册、登录、Token 刷新、修改密码等接口的数据校验。
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """用户注册请求。

    校验规则：
    - username: 3~64 字符
    - email: 合法邮箱且未被注册
    - password: 至少 8 位，需通过 Django 密码验证器
    - password_confirm: 必须与 password 一致
    """

    username = serializers.CharField(
        min_length=3,
        max_length=64,
        help_text="用户名，3~64 个字符。",
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
        """检查用户名唯一性。"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册")
        return value

    def validate_email(self, value: str) -> str:
        """检查邮箱唯一性。"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value

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
