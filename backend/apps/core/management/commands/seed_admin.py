#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
创建初始站长账号。
@Project : QWeb
@File : seed_admin.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from __future__ import annotations

from getpass import getpass
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from apps.accounts.services.bootstrap_service import create_owner_user, is_owner_bootstrap_required


class Command(BaseCommand):
    """实现当前 Django 管理命令。"""

    help = "交互式创建初始站长账号并分配 owner 角色（不预置固定账号）"

    def add_arguments(self, parser: Any) -> None:
        """注册当前管理命令支持的命令行参数。"""
        parser.add_argument("--username", help="站长用户名。")
        parser.add_argument("--email", help="站长邮箱。")
        parser.add_argument("--password", help="站长密码；不传时交互式输入。")

    def handle(self, *args: Any, **options: Any) -> None:
        """执行当前 Django 管理命令。"""
        if not is_owner_bootstrap_required():
            self.stdout.write("owner 角色用户已存在，无需重复创建")
            return

        username = options.get("username") or input("站长用户名: ").strip()
        email = options.get("email") or input("站长邮箱: ").strip()
        password = options.get("password") or getpass("站长密码: ")
        if not username or not email or not password:
            raise CommandError("用户名、邮箱和密码不能为空")

        result = create_owner_user(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"已创建站长账号: {result['user'].username}"))
