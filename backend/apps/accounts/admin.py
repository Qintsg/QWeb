"""accounts 模块 Admin 配置。

在 Django 管理后台注册 User 和 UserProfile 模型，
提供用户检索、筛选与内联编辑能力。
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models.user import User
from apps.accounts.models.user_profile import UserProfile


class UserProfileInline(admin.StackedInline):
    """用户资料内联编辑（嵌入 User 页面）。"""

    model = UserProfile
    fk_name = "user"
    can_delete = False
    verbose_name_plural = "用户资料"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """自定义 User 管理后台。"""

    inlines = (UserProfileInline,)

    list_display = ("username", "email", "display_name", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "display_name")
    ordering = ("-date_joined",)

    # 编辑页字段
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("基本信息", {"fields": ("email", "display_name")}),
        ("权限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("时间", {"fields": ("last_login", "date_joined")}),
    )

    # 新建页字段
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "display_name", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("date_joined",)
