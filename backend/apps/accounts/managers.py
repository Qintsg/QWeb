"""自定义用户管理器。

提供 create_user / create_superuser 方法，确保用户创建逻辑统一。
"""

from __future__ import annotations

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """自定义用户管理器。"""

    def create_user(
        self,
        username: str,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        """创建普通用户。

        Args:
            username: 用户名，必填。
            email: 邮箱，必填且唯一。
            password: 密码，明文传入后自动哈希。
            **extra_fields: 其他 User 字段。
        """
        if not username:
            raise ValueError("用户名不能为空")
        if not email:
            raise ValueError("邮箱不能为空")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        """创建超级管理员。

        自动设置 is_staff=True, is_superuser=True, is_active=True。
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级管理员必须设置 is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级管理员必须设置 is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)
