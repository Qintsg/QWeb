#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
修复历史开发库中登录日志用户外键列名与当前模型不一致的问题。
@Project : QWeb
@File : 0004_repair_login_log_uid_column.py
@Author : Qintsg
@Date : 2026-05-18 11:15
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


def _foreign_key_exists(schema_editor, table_name: str, column_name: str) -> bool:
    """
    判断指定列是否已有指向 users.uid 的外键约束。
    :param schema_editor: Django schema editor。
    :param table_name: 数据库表名。
    :param column_name: 用户外键列名。
    :return: 外键约束存在时返回 True。
    """
    with schema_editor.connection.cursor() as cursor:
        constraints = schema_editor.connection.introspection.get_constraints(cursor, table_name)
    return any(
        constraint.get("foreign_key") == ("users", "uid")
        and constraint.get("columns") == [column_name]
        for constraint in constraints.values()
    )


def _execute(schema_editor, sql: str) -> None:
    """
    执行当前数据库修复语句。
    :param schema_editor: Django schema editor。
    :param sql: 需要执行的 SQL。
    :return: 无返回值。
    """
    schema_editor.execute(sql)


def repair_login_log_uid_column(apps, schema_editor) -> None:
    """
    将登录日志表的当前用户外键列修正为模型约定的 uid。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    table_name = "user_login_logs"
    if not _table_exists(schema_editor, table_name):
        return

    if not _column_exists(schema_editor, table_name, "uid"):
        if _column_exists(schema_editor, table_name, "user_id"):
            _execute(schema_editor, f'ALTER TABLE "{table_name}" RENAME COLUMN "user_id" TO "uid"')
        else:
            _execute(schema_editor, f'ALTER TABLE "{table_name}" ADD COLUMN "uid" bigint')

    if _column_exists(schema_editor, table_name, "user_id"):
        _execute(
            schema_editor,
            f'''
            UPDATE "{table_name}"
            SET "uid" = COALESCE("uid", "user_id")
            ''',
        )

    if _column_exists(schema_editor, table_name, "user_id_legacy_uuid") and _table_exists(schema_editor, "accounts_legacy_user_id_map"):
        _execute(
            schema_editor,
            f'''
            UPDATE "{table_name}" target
            SET "uid" = COALESCE(target."uid", mapped."uid")
            FROM "accounts_legacy_user_id_map" mapped
            WHERE target."user_id_legacy_uuid" = mapped."legacy_user_id"
            ''',
        )

    if not _foreign_key_exists(schema_editor, table_name, "uid"):
        _execute(
            schema_editor,
            f'ALTER TABLE "{table_name}" ADD CONSTRAINT "{table_name}_uid_users_uid_fk" FOREIGN KEY ("uid") REFERENCES "users" ("uid") DEFERRABLE INITIALLY DEFERRED',
        )


class Migration(migrations.Migration):

    """记录当前应用的数据库迁移步骤。"""

    dependencies = [
        ("audit", "0003_repair_legacy_user_foreign_keys"),
    ]

    operations = [
        migrations.RunPython(repair_login_log_uid_column, migrations.RunPython.noop),
    ]
