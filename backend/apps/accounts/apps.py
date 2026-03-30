"""accounts 应用配置。"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """用户账号模块。

    负责用户注册、登录、资料管理、密码管理等功能。
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "用户账号"
