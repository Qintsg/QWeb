#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
修复历史开发库中登录日志表名与当前模型不一致的问题。
@Project : QWeb
@File : 0002_repair_legacy_login_log_table.py
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


def repair_legacy_login_log_table(apps, schema_editor) -> None:
    """
    修复登录日志应用在早期开发库中遗留的旧表结构。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    login_log_model = apps.get_model("audit", "LoginLog")
    if not _table_exists(schema_editor, login_log_model._meta.db_table):
        if _table_exists(schema_editor, "login_log"):
            _execute(schema_editor, 'ALTER TABLE "login_log" RENAME TO "user_login_logs"')
        else:
            schema_editor.create_model(login_log_model)

    if not _table_exists(schema_editor, "user_login_logs"):
        return

    column_definitions = {
        "login_type": 'varchar(32) NOT NULL DEFAULT \'password\'',
        "provider": 'varchar(64)',
        "device_info": "jsonb NOT NULL DEFAULT '{}'::jsonb",
        "success": 'boolean NOT NULL DEFAULT FALSE',
    }
    for column_name, column_definition in column_definitions.items():
        if not _column_exists(schema_editor, "user_login_logs", column_name):
            _execute(schema_editor, f'ALTER TABLE "user_login_logs" ADD COLUMN "{column_name}" {column_definition}')

    _execute(schema_editor, "UPDATE \"user_login_logs\" SET \"login_type\" = COALESCE(NULLIF(\"login_type\", ''), 'password')")
    _execute(schema_editor, "UPDATE \"user_login_logs\" SET \"success\" = CASE WHEN \"action\" IN ('login', 'oauth_bind', 'oauth_register') THEN TRUE ELSE FALSE END WHERE \"success\" IS NULL OR \"success\" = FALSE")


class Migration(migrations.Migration):

    """记录当前应用的数据库迁移步骤。"""

    dependencies = [
        ("accounts", "0002_repair_legacy_account_tables"),
        ("audit", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_legacy_login_log_table, migrations.RunPython.noop),
    ]
