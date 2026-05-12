#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
初始化 IAM 预置角色与权限数据。
@Project : QWeb
@File : init_permissions.py
@Author : Qintsg
@Date : 2026-05-12 00:00
'''
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.iam.models import Permission, Role, RolePermission

# ---------- 预置角色 ----------
PRESET_ROLES = [
    {"name": "owner", "display_name": "站长", "level": 0, "is_system": True},
    {"name": "admin", "display_name": "管理员", "level": 10, "is_system": True},
    {"name": "trusted", "display_name": "信任用户", "level": 50, "is_system": True},
    {"name": "user", "display_name": "普通用户", "level": 100, "is_system": True},
    {"name": "guest", "display_name": "访客", "level": 200, "is_system": True},
]

# ---------- 预置权限 ----------
# 格式: (module, resource, action, code, name)
PRESET_PERMISSIONS = [
    # IAM
    ("iam", "permission", "view", "iam.permission.view", "查看权限"),
    ("iam", "role", "view", "iam.role.view", "查看角色"),
    ("iam", "role", "create", "iam.role.create", "创建角色"),
    ("iam", "role", "update", "iam.role.update", "更新角色"),
    ("iam", "role", "delete", "iam.role.delete", "删除角色"),
    ("iam", "user_role", "view", "iam.user_role.view", "查看用户角色"),
    ("iam", "user_role", "manage", "iam.user_role.manage", "管理用户角色"),
    ("iam", "override", "view", "iam.override.view", "查看权限覆盖"),
    ("iam", "override", "manage", "iam.override.manage", "管理权限覆盖"),

    # 账户
    ("accounts", "user", "view", "accounts.user.view", "查看用户"),
    ("accounts", "user", "update", "accounts.user.update", "更新用户"),
    ("accounts", "user", "delete", "accounts.user.delete", "删除用户"),

    # 博客
    ("blog", "post", "view", "blog.post.view", "查看文章"),
    ("blog", "post", "create", "blog.post.create", "创建文章"),
    ("blog", "post", "update", "blog.post.update", "编辑文章"),
    ("blog", "post", "delete", "blog.post.delete", "删除文章"),
    ("blog", "category", "manage", "blog.category.manage", "管理分类"),
    ("blog", "tag", "manage", "blog.tag.manage", "管理标签"),

    # Wiki
    ("wiki", "page", "view", "wiki.page.view", "查看 Wiki"),
    ("wiki", "page", "create", "wiki.page.create", "创建 Wiki"),
    ("wiki", "page", "update", "wiki.page.update", "编辑 Wiki"),
    ("wiki", "page", "delete", "wiki.page.delete", "删除 Wiki"),

    # 存储
    ("storage", "file", "view", "storage.file.view", "查看文件"),
    ("storage", "file", "upload", "storage.file.upload", "上传文件"),
    ("storage", "file", "delete", "storage.file.delete", "删除文件"),

    # 系统配置
    ("system_config", "config", "view", "system_config.config.view", "查看系统配置"),
    ("system_config", "config", "update", "system_config.config.update", "修改系统配置"),

    # 审计
    ("audit", "log", "view", "audit.log.view", "查看审计日志"),

    # 首页管理
    ("homepage", "service_link", "view", "homepage.service_link.view", "查看服务链接"),
    ("homepage", "service_link", "manage", "homepage.service_link.manage", "管理服务链接"),
]

# ---------- 角色默认权限映射 ----------
# admin 拥有全部权限; trusted/user/guest 逐级递减
ROLE_PERMISSION_MAP = {
    "admin": "*",  # 全部权限
    "trusted": [
        "iam.permission.view", "iam.role.view",
        "accounts.user.view",
        "blog.post.view", "blog.post.create", "blog.post.update",
        "blog.category.manage", "blog.tag.manage",
        "wiki.page.view", "wiki.page.create", "wiki.page.update",
        "storage.file.view", "storage.file.upload",
        "audit.log.view",
        "homepage.service_link.view",
    ],
    "user": [
        "blog.post.view", "blog.post.create",
        "wiki.page.view",
        "storage.file.view", "storage.file.upload",
    ],
    "guest": [
        "blog.post.view",
        "wiki.page.view",
    ],
}


class Command(BaseCommand):
    """实现当前 Django 管理命令。"""
    help = "初始化 IAM 预置角色与权限数据"

    def add_arguments(self, parser: Any) -> None:
        """注册当前管理命令支持的命令行参数。"""
        parser.add_argument(
            "--reset",
            action="store_true",
            help="清除现有角色权限关联后重新创建",
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        """执行当前 Django 管理命令。"""
        reset = options["reset"]

        # 1. 创建权限
        perm_count = 0
        for module, resource, action, code, name in PRESET_PERMISSIONS:
            _, created = Permission.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "module": module,
                    "resource": resource,
                    "action": action,
                    "is_active": True,
                },
            )
            if created:
                perm_count += 1
        self.stdout.write(f"权限: 新增 {perm_count} 条，共 {len(PRESET_PERMISSIONS)} 条")

        # 2. 创建角色
        role_count = 0
        for role_data in PRESET_ROLES:
            _, created = Role.objects.update_or_create(
                name=role_data["name"],
                defaults={
                    "display_name": role_data["display_name"],
                    "level": role_data["level"],
                    "is_system": role_data["is_system"],
                },
            )
            if created:
                role_count += 1
        self.stdout.write(f"角色: 新增 {role_count} 条，共 {len(PRESET_ROLES)} 条")

        # 3. 关联角色权限
        if reset:
            RolePermission.objects.all().delete()
            self.stdout.write("已清除全部角色权限关联")

        all_permissions = {p.code: p for p in Permission.objects.filter(is_active=True)}
        all_roles = {r.name: r for r in Role.objects.all()}

        link_count = 0
        for role_name, permissions in ROLE_PERMISSION_MAP.items():
            role = all_roles.get(role_name)
            if not role:
                continue

            if permissions == "*":
                perm_list = list(all_permissions.values())
            else:
                perm_list = [all_permissions[code] for code in permissions if code in all_permissions]

            for perm in perm_list:
                _, created = RolePermission.objects.get_or_create(
                    role=role,
                    permission=perm,
                )
                if created:
                    link_count += 1

        self.stdout.write(f"角色权限关联: 新增 {link_count} 条")
        self.stdout.write(self.style.SUCCESS("IAM 初始化完成"))
