#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
提供 Django 管理命令入口。
@Project : QWeb
@File : manage.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
import os
import sys


def main() -> None:
    """启动 Django 管理命令执行流程。"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
