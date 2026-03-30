"""用户信息序列化器。

用于用户资料查看/编辑、管理员用户列表等接口。
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器。

    用于查看和编辑个人资料扩展信息。
    """

    class Meta:
        model = UserProfile
        fields = [
            "avatar",
            "bio",
            "phone",
            "timezone",
            "language",
            "theme_preference",
        ]


class UserSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器。

    用于用户列表、用户详情等只读场景。
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "is_active",
            "date_joined",
            "last_login",
            "profile",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "last_login",
        ]


class MeSerializer(serializers.ModelSerializer):
    """当前登录用户信息序列化器。

    包含完整的用户信息和资料，部分字段可编辑。
    """

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "is_active",
            "date_joined",
            "last_login",
            "profile",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "is_active",
            "date_joined",
            "last_login",
        ]

    def update(self, instance, validated_data: dict):
        """更新用户信息及嵌套的资料字段。"""
        profile_data = validated_data.pop("profile", None)

        # 更新 User 字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 更新 UserProfile 字段
        if profile_data is not None:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserAdminSerializer(serializers.ModelSerializer):
    """管理员视角的用户序列化器。

    包含管理字段如 is_active、is_staff 等，管理员可修改。
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
            "profile",
        ]
        read_only_fields = [
            "id",
            "username",
            "date_joined",
            "last_login",
        ]
