"""创建初始管理员账号。

Usage: python manage.py seed_admin
"""
from django.core.management.base import BaseCommand

from apps.accounts.models import User, UserContact
from apps.accounts.services.account_bootstrap import ensure_user_related_records
from apps.iam.models import Role, UserRole


class Command(BaseCommand):
    help = "创建初始管理员账号并分配 owner 角色（幂等操作）"

    def handle(self, *args, **options):
        username = "qintsg"
        password = "Ss201803@Qintsg"
        email = "admin@qintsg.cn"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_active": True,
                "nickname": "Qintsg",
                "user_type": User.UserType.ADMIN,
            },
        )
        UserContact.objects.update_or_create(user=user, defaults={"email": email})
        if created:
            user.set_password(password)
            user.save()
            ensure_user_related_records(user=user, email=email)
            self.stdout.write(self.style.SUCCESS(f"创建管理员: {username}"))
        else:
            self.stdout.write(f"管理员已存在: {username}")

        try:
            owner_role = Role.objects.get(name="owner")
            _, role_created = UserRole.objects.get_or_create(
                user=user, role=owner_role
            )
            if role_created:
                self.stdout.write(self.style.SUCCESS("已分配 owner 角色"))
            else:
                self.stdout.write("owner 角色已分配")
        except Role.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    "owner 角色不存在，请先运行 init_permissions"
                )
            )
