"""accounts 模块 Admin 配置。"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import (
    User,
    UserContact,
    UserOAuthAccount,
    UserProfile,
    UserRefreshToken,
    UserSecurity,
    UserSettings,
)


class UserContactInline(admin.StackedInline):
    model = UserContact
    fk_name = "user"
    can_delete = False
    extra = 0
    verbose_name_plural = "联系方式"


class UserSecurityInline(admin.StackedInline):
    model = UserSecurity
    fk_name = "user"
    can_delete = False
    extra = 0
    readonly_fields = ("last_login_at", "last_login_ip", "last_login_user_agent")
    verbose_name_plural = "安全信息"


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    extra = 0
    verbose_name_plural = "用户资料"


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    fk_name = "user"
    can_delete = False
    extra = 0
    verbose_name_plural = "用户设置"


class OAuthAccountInline(admin.TabularInline):
    model = UserOAuthAccount
    fk_name = "user"
    extra = 0
    can_delete = False
    readonly_fields = (
        "provider",
        "provider_account_id",
        "provider_username",
        "provider_email",
        "linked_at",
        "updated_at",
    )
    fields = readonly_fields
    verbose_name_plural = "第三方账号绑定"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """自定义 User 管理后台。"""

    inlines = (
        UserContactInline,
        UserSecurityInline,
        UserProfileInline,
        UserSettingsInline,
        OAuthAccountInline,
    )
    list_display = ("uid", "username", "nickname", "status", "user_type", "is_staff", "created_at")
    list_filter = ("status", "user_type", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "nickname", "contact__email", "contact__phone")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("基本信息", {"fields": ("nickname", "avatar_url", "status", "user_type")}),
        ("权限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("时间", {"fields": ("last_login", "created_at", "updated_at", "deleted_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "nickname", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("uid", "created_at", "updated_at", "last_login")


@admin.register(UserOAuthAccount)
class UserOAuthAccountAdmin(admin.ModelAdmin):
    """第三方账号绑定管理后台。"""

    list_display = ("provider", "provider_username", "provider_email", "user", "linked_at")
    list_filter = ("provider",)
    search_fields = (
        "provider_account_id",
        "provider_username",
        "provider_email",
        "user__username",
    )
    readonly_fields = ("linked_at", "updated_at")


@admin.register(UserRefreshToken)
class UserRefreshTokenAdmin(admin.ModelAdmin):
    """刷新令牌记录管理后台。"""

    list_display = ("user", "device_name", "ip", "expires_at", "revoked_at", "created_at")
    list_filter = ("revoked_at", "created_at", "expires_at")
    search_fields = ("user__username", "device_id", "device_name", "ip")
    readonly_fields = ("token_hash", "created_at")
