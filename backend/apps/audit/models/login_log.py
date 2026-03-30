"""登录审计日志模型。"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class LoginLog(models.Model):
    """
    登录行为审计日志。

    独立于通用审计日志，专门追踪登录相关事件：
    - 登录成功 / 登出 / 登录失败
    - 来源 IP、User-Agent
    - 失败原因
    """

    class Action(models.TextChoices):
        """登录操作类型。"""

        LOGIN = "login", "登录成功"
        LOGOUT = "logout", "登出"
        FAILED = "failed", "登录失败"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="login_logs",
        verbose_name="用户",
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="登录用户名",
        help_text="登录失败时 user 可能为 null，此字段保留尝试的用户名",
    )
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        db_index=True,
        verbose_name="操作类型",
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP 地址",
    )
    user_agent = models.TextField(
        blank=True,
        default="",
        verbose_name="User-Agent",
    )
    failure_reason = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="失败原因",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="操作时间",
    )

    class Meta:
        db_table = "login_log"
        ordering = ["-created_at"]
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志"

    def __str__(self) -> str:
        name = self.user.username if self.user else self.username or "未知"
        return f"[{self.action}] {name} @ {self.ip_address}"
