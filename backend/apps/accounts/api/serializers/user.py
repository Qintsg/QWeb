#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
用户信息序列化器。
@Project : QWeb
@File : user.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import UserContact, UserProfile, UserSettings

User = get_user_model()


class UserContactSerializer(serializers.ModelSerializer):
    """用户联系方式序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = UserContact
        fields = ["email", "phone", "email_verified_at", "phone_verified_at"]
        read_only_fields = ["email_verified_at", "phone_verified_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = UserProfile
        fields = [
            "real_name",
            "gender",
            "birthday",
            "bio",
            "country",
            "province",
            "city",
            "website",
            "github",
            "extra",
        ]


class UserSettingsSerializer(serializers.ModelSerializer):
    """用户设置序列化器。"""

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = UserSettings
        fields = [
            "language",
            "timezone",
            "theme",
            "notification_settings",
            "privacy_settings",
            "preferences",
        ]


class UserSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器。"""

    contact = UserContactSerializer(read_only=True)
    profile = UserProfileSerializer(read_only=True)
    settings = UserSettingsSerializer(read_only=True)

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = User
        fields = [
            "uid",
            "username",
            "nickname",
            "avatar_url",
            "status",
            "user_type",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "last_login",
            "contact",
            "profile",
            "settings",
        ]
        read_only_fields = fields


class MeSerializer(serializers.ModelSerializer):
    """当前登录用户信息序列化器。"""

    contact = UserContactSerializer(required=False)
    profile = UserProfileSerializer(required=False)
    settings = UserSettingsSerializer(required=False)

    class Meta:
        """定义当前对象的 Django 元数据。"""
        model = User
        fields = [
            "uid",
            "username",
            "nickname",
            "avatar_url",
            "status",
            "user_type",
            "is_active",
            "created_at",
            "updated_at",
            "last_login",
            "contact",
            "profile",
            "settings",
        ]
        read_only_fields = [
            "uid",
            "username",
            "status",
            "user_type",
            "is_active",
            "created_at",
            "updated_at",
            "last_login",
        ]

    def update(self, instance: Any, validated_data: dict) -> Any:
        """更新用户及其嵌套扩展表。"""
        contact_data = validated_data.pop("contact", None)
        profile_data = validated_data.pop("profile", None)
        settings_data = validated_data.pop("settings", None)

        user_update_fields: list[str] = []
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            user_update_fields.append(attr)
        if user_update_fields:
            user_update_fields.append("updated_at")
            instance.save(update_fields=user_update_fields)

        if contact_data is not None:
            contact, _ = UserContact.objects.get_or_create(user=instance)
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        if profile_data is not None:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        if settings_data is not None:
            settings, _ = UserSettings.objects.get_or_create(user=instance)
            for attr, value in settings_data.items():
                setattr(settings, attr, value)
            settings.save()

        return instance


class UserAdminSerializer(MeSerializer):
    """管理员视角的用户序列化器。"""

    class Meta(MeSerializer.Meta):
        """定义当前对象的 Django 元数据。"""
        fields = MeSerializer.Meta.fields + ["is_staff", "is_superuser"]
        read_only_fields = [
            "uid",
            "username",
            "created_at",
            "updated_at",
            "last_login",
        ]
