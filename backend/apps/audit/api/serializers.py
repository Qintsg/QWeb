"""审计模块序列化器。"""

from rest_framework import serializers

from apps.audit.models import AuditLog, LoginLog


class AuditLogSerializer(serializers.ModelSerializer):
    """操作审计日志序列化器。"""

    username = serializers.CharField(source="user.username", default="", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "username",
            "action",
            "module",
            "resource",
            "resource_id",
            "detail",
            "ip_address",
            "user_agent",
            "created_at",
        ]
        read_only_fields = fields


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器。"""

    class Meta:
        model = LoginLog
        fields = [
            "id",
            "username",
            "action",
            "ip_address",
            "user_agent",
            "failure_reason",
            "created_at",
        ]
        read_only_fields = fields
