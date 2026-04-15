"""
初始化首页服务链接数据
Usage: python manage.py seed_service_links
"""
from django.core.management.base import BaseCommand

from apps.homepage.models import ServiceLink


SEED_DATA = [
    {
        "title": "知识图谱驱动的个性化自适应学习系统",
        "url": "https://edu.qintsg.cn/",
        "description": "上海市计算机应用能力大赛作品",
        "remark": "仅用于2026上海市计算机应用能力大赛作品展示，不进行实际运营",
        "icon": "🎓",
        "color": "#0e9aa7",
        "category": "project",
        "sort_order": 10,
    },
    {
        "title": "喵喵湾",
        "url": "https://meow.qintsg.cn/",
        "description": "上海第二工业大学大学生创新创业作品",
        "remark": "仅用于2026上海市第二工业大学大学生创新创业作品展示，不进行实际运营",
        "icon": "🐱",
        "color": "#f28a2e",
        "category": "project",
        "sort_order": 20,
    },
    {
        "title": "Frps 管理网页",
        "url": "https://frps.qintsg.cn/",
        "description": "本服务器 frps 管理网页",
        "icon": "🖥️",
        "color": "#3b82f6",
        "category": "server",
        "sort_order": 30,
    },
    {
        "title": "1Panel 管理面板",
        "url": "https://panel.qintsg.cn/",
        "description": "本服务器 1Panel 管理面板",
        "icon": "🛠️",
        "color": "#10b981",
        "category": "server",
        "sort_order": 40,
    },
    {
        "title": "8C16G 服务器 1Panel",
        "url": "https://panel.jfy2.qintsg.cn/",
        "description": "8C16G 服务器 1Panel 管理面板",
        "icon": "🖥️",
        "color": "#6366f1",
        "category": "server",
        "sort_order": 50,
    },
    {
        "title": "8C16G 服务器 Frpc",
        "url": "https://frpc.jfy2.qintsg.cn/",
        "description": "8C16G 服务器 frpc 管理面板",
        "icon": "🔗",
        "color": "#8b5cf6",
        "category": "server",
        "sort_order": 60,
    },
    {
        "title": "HFS 临时文件传输",
        "url": "https://hfs.qintsg.cn/",
        "description": "hfs 临时文件传输",
        "icon": "📁",
        "color": "#f59e0b",
        "category": "tool",
        "sort_order": 70,
    },
    {
        "title": "Notebook Frpc 管理面板",
        "url": "https://frpc.nootbook.cn/",
        "description": "Notebook Frpc 管理面板",
        "icon": "📓",
        "color": "#ec4899",
        "category": "server",
        "sort_order": 80,
    },
]


class Command(BaseCommand):
    help = "初始化首页服务链接种子数据（幂等操作，按 URL 去重）"

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0
        for item in SEED_DATA:
            url = item["url"]
            if ServiceLink.objects.filter(url=url).exists():
                skipped_count += 1
                self.stdout.write(f"  跳过（已存在）: {item['title']}")
                continue
            ServiceLink.objects.create(**item)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"  创建: {item['title']}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n完成: 创建 {created_count} 条，跳过 {skipped_count} 条"
            )
        )
