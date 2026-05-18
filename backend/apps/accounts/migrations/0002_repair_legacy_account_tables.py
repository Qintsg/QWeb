#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
修复历史开发库中账号表名与当前模型不一致的问题。
@Project : QWeb
@File : 0002_repair_legacy_account_tables.py
@Author : Qintsg
@Date : 2026-05-18 10:55
'''
from __future__ import annotations

from django.db import migrations


def _table_exists(schema_editor, table_name: str) -> bool:
    """
    判断指定数据库表是否存在。
    :param schema_editor: Django schema editor。
    :param table_name: 数据库表名。
    :return: 表存在时返回 True。
    """
    return table_name in schema_editor.connection.introspection.table_names()


def _column_exists(schema_editor, table_name: str, column_name: str) -> bool:
    """
    判断指定数据库列是否存在。
    :param schema_editor: Django schema editor。
    :param table_name: 数据库表名。
    :param column_name: 数据库列名。
    :return: 列存在时返回 True。
    """
    if not _table_exists(schema_editor, table_name):
        return False
    with schema_editor.connection.cursor() as cursor:
        columns = schema_editor.connection.introspection.get_table_description(cursor, table_name)
    return any(column.name == column_name for column in columns)


def _execute(schema_editor, sql: str) -> None:
    """
    执行当前数据库修复语句。
    :param schema_editor: Django schema editor。
    :param sql: 需要执行的 SQL。
    :return: 无返回值。
    """
    schema_editor.execute(sql)


def _create_model_table(apps, schema_editor, model_name: str) -> None:
    """
    创建当前账号模型对应的数据表。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :param model_name: 模型名称。
    :return: 无返回值。
    """
    model = apps.get_model("accounts", model_name)
    if not _table_exists(schema_editor, model._meta.db_table):
        schema_editor.create_model(model)


def _backup_incompatible_renamed_user_table(schema_editor) -> None:
    """
    回滚曾被错误重命名为 users 的旧 UUID 用户表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    if not _table_exists(schema_editor, "users"):
        return
    with schema_editor.connection.cursor() as cursor:
        columns = schema_editor.connection.introspection.get_table_description(cursor, "users")
    uid_column = next((column for column in columns if column.name == "uid"), None)
    if uid_column is None:
        return
    if "uuid" not in str(uid_column.type_code).lower():
        return
    if _table_exists(schema_editor, "accounts_user"):
        _execute(schema_editor, 'ALTER TABLE "users" RENAME TO "legacy_accounts_user_uuid"')
    else:
        _execute(schema_editor, 'ALTER TABLE "users" RENAME TO "accounts_user"')


def _create_current_account_tables(apps, schema_editor) -> None:
    """
    创建当前账号模型所需但数据库缺失的数据表。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    _backup_incompatible_renamed_user_table(schema_editor)
    for model_name in [
        "User",
        "UserContact",
        "UserProfile",
        "UserSecurity",
        "UserSettings",
        "UserOAuthAccount",
        "UserRefreshToken",
    ]:
        _create_model_table(apps, schema_editor, model_name)

    user_model = apps.get_model("accounts", "User")
    for field in user_model._meta.local_many_to_many:
        through_model = field.remote_field.through
        if not _table_exists(schema_editor, through_model._meta.db_table):
            schema_editor.create_model(through_model)


def _create_legacy_user_mapping(schema_editor) -> None:
    """
    创建旧 UUID 用户 ID 到当前 bigint UID 的映射表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    _execute(
        schema_editor,
        """
        CREATE TABLE IF NOT EXISTS "accounts_legacy_user_id_map" (
            "legacy_user_id" uuid PRIMARY KEY,
            "uid" bigint NOT NULL UNIQUE REFERENCES "users" ("uid") ON DELETE CASCADE
        )
        """,
    )


def _has_legacy_users(schema_editor) -> bool:
    """
    判断当前数据库是否存在旧账号表。
    :param schema_editor: Django schema editor。
    :return: 存在旧账号表时返回 True。
    """
    return _table_exists(schema_editor, "accounts_user")


def _migrate_legacy_users(schema_editor) -> None:
    """
    将旧 UUID 主键用户迁移到当前 bigint UID 用户表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    if not _has_legacy_users(schema_editor):
        return

    _create_legacy_user_mapping(schema_editor)
    _execute(
        schema_editor,
        """
        WITH inserted AS (
            INSERT INTO "users" (
                "password",
                "last_login",
                "is_superuser",
                "username",
                "nickname",
                "avatar_url",
                "status",
                "user_type",
                "is_active",
                "is_staff",
                "created_at",
                "updated_at",
                "deleted_at"
            )
            SELECT
                legacy."password",
                legacy."last_login",
                legacy."is_superuser",
                legacy."username",
                NULLIF(legacy."display_name", ''),
                NULLIF(profile."avatar", ''),
                CASE WHEN legacy."is_active" THEN 'active' ELSE 'inactive' END,
                CASE WHEN legacy."is_staff" OR legacy."is_superuser" THEN 'admin' ELSE 'normal' END,
                legacy."is_active",
                legacy."is_staff",
                COALESCE(legacy."date_joined", NOW()),
                COALESCE(legacy."date_joined", NOW()),
                NULL
            FROM "accounts_user" legacy
            LEFT JOIN "accounts_user_profile" profile ON profile."user_id" = legacy."id"
            WHERE NOT EXISTS (
                SELECT 1 FROM "accounts_legacy_user_id_map" mapped WHERE mapped."legacy_user_id" = legacy."id"
            )
            ON CONFLICT ("username") DO NOTHING
            RETURNING "uid", "username"
        )
        INSERT INTO "accounts_legacy_user_id_map" ("legacy_user_id", "uid")
        SELECT legacy."id", inserted."uid"
        FROM "accounts_user" legacy
        JOIN inserted ON inserted."username" = legacy."username"
        ON CONFLICT ("legacy_user_id") DO NOTHING
        """,
    )
    _execute(
        schema_editor,
        """
        INSERT INTO "accounts_legacy_user_id_map" ("legacy_user_id", "uid")
        SELECT legacy."id", users."uid"
        FROM "accounts_user" legacy
        JOIN "users" users ON users."username" = legacy."username"
        ON CONFLICT ("legacy_user_id") DO NOTHING
        """,
    )


def _migrate_legacy_related_records(schema_editor) -> None:
    """
    将旧用户资料和 Django 权限关联迁移到当前账号扩展表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    if not _has_legacy_users(schema_editor):
        return

    _execute(
        schema_editor,
        """
        INSERT INTO "user_contact" ("uid", "email", "phone", "email_verified_at", "phone_verified_at", "created_at", "updated_at")
        SELECT
            mapped."uid",
            NULLIF(legacy."email", ''),
            NULLIF(profile."phone", ''),
            NULL,
            NULL,
            COALESCE(profile."created_at", legacy."date_joined", NOW()),
            COALESCE(profile."updated_at", legacy."date_joined", NOW())
        FROM "accounts_user" legacy
        JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy."id"
        LEFT JOIN "accounts_user_profile" profile ON profile."user_id" = legacy."id"
        WHERE NOT EXISTS (SELECT 1 FROM "user_contact" contact WHERE contact."uid" = mapped."uid")
        """,
    )
    _execute(
        schema_editor,
        """
        INSERT INTO "user_profile" ("uid", "real_name", "gender", "birthday", "bio", "country", "province", "city", "website", "github", "extra", "created_at", "updated_at")
        SELECT
            mapped."uid",
            NULL,
            NULL,
            NULL,
            COALESCE(profile."bio", ''),
            NULL,
            NULL,
            NULL,
            NULL,
            NULL,
            '{}'::jsonb,
            COALESCE(profile."created_at", legacy."date_joined", NOW()),
            COALESCE(profile."updated_at", legacy."date_joined", NOW())
        FROM "accounts_user" legacy
        JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy."id"
        LEFT JOIN "accounts_user_profile" profile ON profile."user_id" = legacy."id"
        WHERE NOT EXISTS (SELECT 1 FROM "user_profile" current_profile WHERE current_profile."uid" = mapped."uid")
        """,
    )
    _execute(
        schema_editor,
        """
        INSERT INTO "user_security" ("uid", "password_hash", "password_algo", "password_updated_at", "two_factor_enabled", "two_factor_secret_enc", "failed_login_attempts", "locked_until", "last_login_at", "last_login_ip", "last_login_user_agent", "created_at", "updated_at")
        SELECT
            mapped."uid",
            legacy."password",
            'django',
            NULL,
            FALSE,
            NULL,
            0,
            NULL,
            legacy."last_login",
            NULL,
            '',
            COALESCE(legacy."date_joined", NOW()),
            COALESCE(legacy."date_joined", NOW())
        FROM "accounts_user" legacy
        JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy."id"
        WHERE NOT EXISTS (SELECT 1 FROM "user_security" security WHERE security."uid" = mapped."uid")
        """,
    )
    _execute(
        schema_editor,
        """
        INSERT INTO "user_settings" ("uid", "language", "timezone", "theme", "notification_settings", "privacy_settings", "preferences", "created_at", "updated_at")
        SELECT
            mapped."uid",
            COALESCE(NULLIF(profile."language", ''), 'zh-CN'),
            COALESCE(NULLIF(profile."timezone", ''), 'Asia/Shanghai'),
            CASE WHEN profile."theme_preference" IN ('light', 'dark', 'system') THEN profile."theme_preference" ELSE 'system' END,
            '{}'::jsonb,
            '{}'::jsonb,
            '{}'::jsonb,
            COALESCE(profile."created_at", legacy."date_joined", NOW()),
            COALESCE(profile."updated_at", legacy."date_joined", NOW())
        FROM "accounts_user" legacy
        JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy."id"
        LEFT JOIN "accounts_user_profile" profile ON profile."user_id" = legacy."id"
        WHERE NOT EXISTS (SELECT 1 FROM "user_settings" settings WHERE settings."uid" = mapped."uid")
        """,
    )
    if _table_exists(schema_editor, "accounts_user_groups"):
        _execute(
            schema_editor,
            """
            INSERT INTO "users_groups" ("user_id", "group_id")
            SELECT mapped."uid", legacy_group."group_id"
            FROM "accounts_user_groups" legacy_group
            JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy_group."user_id"
            ON CONFLICT DO NOTHING
            """,
        )
    if _table_exists(schema_editor, "accounts_user_user_permissions"):
        _execute(
            schema_editor,
            """
            INSERT INTO "users_user_permissions" ("user_id", "permission_id")
            SELECT mapped."uid", legacy_permission."permission_id"
            FROM "accounts_user_user_permissions" legacy_permission
            JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy_permission."user_id"
            ON CONFLICT DO NOTHING
            """,
        )


def repair_legacy_account_tables(apps, schema_editor) -> None:
    """
    修复账号应用在早期开发库中遗留的旧表结构。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    _create_current_account_tables(apps, schema_editor)
    _migrate_legacy_users(schema_editor)
    _migrate_legacy_related_records(schema_editor)


class Migration(migrations.Migration):

    """记录当前应用的数据库迁移步骤。"""

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_legacy_account_tables, migrations.RunPython.noop),
    ]
