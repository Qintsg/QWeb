#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
修复历史开发库中登录日志主键类型与当前模型不一致的问题。
@Project : QWeb
@File : 0005_rebuild_legacy_login_log_table.py
@Author : Qintsg
@Date : 2026-05-18 11:20
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


def _column_udt_name(schema_editor, table_name: str, column_name: str) -> str | None:
    """
    读取 PostgreSQL 列的底层类型名称。
    :param schema_editor: Django schema editor。
    :param table_name: 数据库表名。
    :param column_name: 数据库列名。
    :return: 类型名称；列不存在时返回 None。
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT udt_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
              AND column_name = %s
            """,
            [table_name, column_name],
        )
        row = cursor.fetchone()
    return row[0] if row else None


def _execute(schema_editor, sql: str) -> None:
    """
    执行当前数据库修复语句。
    :param schema_editor: Django schema editor。
    :param sql: 需要执行的 SQL。
    :return: 无返回值。
    """
    schema_editor.execute(sql)


def _create_current_login_log_table(apps, schema_editor) -> None:
    """
    创建当前模型结构的登录日志表。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    login_log_model = apps.get_model("audit", "LoginLog")
    if not _table_exists(schema_editor, login_log_model._meta.db_table):
        schema_editor.create_model(login_log_model)


def _copy_legacy_login_logs(schema_editor) -> None:
    """
    将旧 UUID 主键登录日志复制到当前 bigint 主键登录日志表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    if not _table_exists(schema_editor, "legacy_user_login_logs_uuid"):
        return
    if not _table_exists(schema_editor, "user_login_logs"):
        return

    uid_expression = "NULL"
    if _column_exists(schema_editor, "legacy_user_login_logs_uuid", "uid"):
        uid_expression = 'legacy."uid"'
    elif _column_exists(schema_editor, "legacy_user_login_logs_uuid", "user_id"):
        uid_expression = 'legacy."user_id"'
    elif _column_exists(schema_editor, "legacy_user_login_logs_uuid", "user_id_legacy_uuid") and _table_exists(schema_editor, "accounts_legacy_user_id_map"):
        uid_expression = 'mapped."uid"'

    mapping_join = ""
    if "mapped" in uid_expression:
        mapping_join = 'LEFT JOIN "accounts_legacy_user_id_map" mapped ON mapped."legacy_user_id" = legacy."user_id_legacy_uuid"'

    provider_expression = "NULL"
    if _column_exists(schema_editor, "legacy_user_login_logs_uuid", "provider"):
        provider_expression = 'legacy."provider"'

    login_type_expression = "'password'"
    if _column_exists(schema_editor, "legacy_user_login_logs_uuid", "login_type"):
        login_type_expression = "COALESCE(NULLIF(legacy.\"login_type\", ''), 'password')"

    device_info_expression = "'{}'::jsonb"
    if _column_exists(schema_editor, "legacy_user_login_logs_uuid", "device_info"):
        device_info_expression = "COALESCE(legacy.\"device_info\", '{}'::jsonb)"

    success_expression = "CASE WHEN legacy.\"action\" IN ('login', 'oauth_bind', 'oauth_register') THEN TRUE ELSE FALSE END"
    if _column_exists(schema_editor, "legacy_user_login_logs_uuid", "success"):
        success_expression = "COALESCE(legacy.\"success\", CASE WHEN legacy.\"action\" IN ('login', 'oauth_bind', 'oauth_register') THEN TRUE ELSE FALSE END)"

    _execute(
        schema_editor,
        f'''
        INSERT INTO "user_login_logs" (
            "username",
            "login_type",
            "provider",
            "action",
            "ip_address",
            "user_agent",
            "device_info",
            "success",
            "failure_reason",
            "created_at",
            "uid"
        )
        SELECT
            legacy."username",
            {login_type_expression},
            {provider_expression},
            legacy."action",
            legacy."ip_address",
            COALESCE(legacy."user_agent", ''),
            {device_info_expression},
            {success_expression},
            legacy."failure_reason",
            COALESCE(legacy."created_at", NOW()),
            {uid_expression}
        FROM "legacy_user_login_logs_uuid" legacy
        {mapping_join}
        WHERE NOT EXISTS (
            SELECT 1
            FROM "user_login_logs" current_log
            WHERE current_log."username" = legacy."username"
              AND current_log."action" = legacy."action"
              AND current_log."created_at" = legacy."created_at"
        )
        ''',
    )


def rebuild_legacy_login_log_table(apps, schema_editor) -> None:
    """
    重建当前模型要求的登录日志表并迁移旧日志数据。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    table_name = "user_login_logs"
    if not _table_exists(schema_editor, table_name):
        _create_current_login_log_table(apps, schema_editor)
        return

    id_type = _column_udt_name(schema_editor, table_name, "id")
    if id_type != "uuid":
        return

    if not _table_exists(schema_editor, "legacy_user_login_logs_uuid"):
        _execute(schema_editor, 'ALTER TABLE "user_login_logs" RENAME TO "legacy_user_login_logs_uuid"')
    else:
        _execute(schema_editor, 'DROP TABLE "user_login_logs"')

    _create_current_login_log_table(apps, schema_editor)
    _copy_legacy_login_logs(schema_editor)


class Migration(migrations.Migration):

    """记录当前应用的数据库迁移步骤。"""

    dependencies = [
        ("audit", "0004_repair_login_log_uid_column"),
    ]

    operations = [
        migrations.RunPython(rebuild_legacy_login_log_table, migrations.RunPython.noop),
    ]
