"""审计模块 URL 配置。"""

from django.urls import path

from apps.audit.api.views import AuditLogListView, LoginLogListView

app_name = "audit"

urlpatterns = [
    path("logs/", AuditLogListView.as_view(), name="audit-log-list"),
    path("login-logs/", LoginLogListView.as_view(), name="login-log-list"),
]
