#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
修复历史开发库中 IAM 用户外键仍指向旧 UUID 用户表的问题。
@Project : QWeb
@File : 0002_repair_legacy_user_foreign_keys.py
@Author : Qintsg
@Date : 2026-05-18 11:05
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


def _repair_user_foreign_key(schema_editor, table_name: str, column_name: str) -> None:
    """
    将旧 UUID 用户外键列重建为当前 bigint UID 外键列。
    :param schema_editor: Django schema editor。
    :param table_name: 数据库表名。
    :param column_name: 用户外键列名。
    :return: 无返回值。
    """
    if not _table_exists(schema_editor, table_name) or not _column_exists(schema_editor, table_name, column_name):
        return
    backup_column = f"{column_name}_legacy_uuid"
    if not _column_exists(schema_editor, table_name, backup_column):
        _execute(schema_editor, f'ALTER TABLE "{table_name}" RENAME COLUMN "{column_name}" TO "{backup_column}"')
        _execute(schema_editor, f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" bigint')
    _execute(
        schema_editor,
        f'''
        UPDATE "{table_name}" target
        SET "{column_name}" = mapped."uid"
        FROM "accounts_legacy_user_id_map" mapped
        WHERE target."{backup_column}" = mapped."legacy_user_id"
        ''',
    )
    _execute(
        schema_editor,
        f'ALTER TABLE "{table_name}" ADD CONSTRAINT "{table_name}_{column_name}_users_uid_fk" FOREIGN KEY ("{column_name}") REFERENCES "users" ("uid") DEFERRABLE INITIALLY DEFERRED',
    )


def repair_legacy_user_foreign_keys(apps, schema_editor) -> None:
    """
    修复 IAM 表中旧用户外键列。
    :param apps: Django 历史应用注册表。
    :param schema_editor: Django schema editor。
    :return: 无返回值。
    """
    if not _table_exists(schema_editor, "accounts_legacy_user_id_map"):
        return
    for table_name in ["iam_user_role", "iam_user_permission_override"]:
        for column_name in ["user_id", "created_by_id", "updated_by_id"]:
            _repair_user_foreign_key(schema_editor, table_name, column_name)


class Migration(migrations.Migration):

    """记录当前应用的数据库迁移步骤。"""

    dependencies = [
        ("accounts", "0002_repair_legacy_account_tables"),
        ("iam", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_legacy_user_foreign_keys, migrations.RunPython.noop),
    ]
