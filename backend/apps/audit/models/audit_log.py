"""操作审计日志模型。"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    通用操作审计日志。

    记录系统中所有需要追踪的业务操作，包括：
    - 操作人、操作类型、操作目标
    - 请求源信息（IP、User-Agent）
    - 操作详情（JSON 格式存储变更明细）
    """

    class Action(models.TextChoices):
        """审计操作类型。"""

        CREATE = "create", "创建"
        UPDATE = "update", "更新"
        DELETE = "delete", "删除"
        EXPORT = "export", "导出"
        IMPORT = "import", "导入"
        ASSIGN = "assign", "分配"
        REVOKE = "revoke", "撤销"
        APPROVE = "approve", "审批"
        REJECT = "reject", "拒绝"
        OTHER = "other", "其他"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="操作人",
    )
    action = models.CharField(
        max_length=20,
        choices=Action.choices,
        db_index=True,
        verbose_name="操作类型",
    )
    module = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name="模块",
        help_text="如 accounts、iam、blog 等",
    )
    resource = models.CharField(
        max_length=100,
        verbose_name="操作资源",
        help_text="如 user、role、permission 等",
    )
    resource_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="资源 ID",
    )
    detail = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="操作详情",
        help_text="变更前后、参数等 JSON 信息",
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="操作时间",
    )

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]
        verbose_name = "操作审计日志"
        verbose_name_plural = "操作审计日志"

    def __str__(self) -> str:
        username = self.user.username if self.user else "匿名"
        return f"[{self.action}] {username} -> {self.module}.{self.resource}"
