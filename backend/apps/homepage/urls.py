"""首页模块 URL 配置。"""

from django.urls import path

from apps.homepage.api.views.service_link import (
    ServiceLinkAdminDetailView,
    ServiceLinkAdminListCreateView,
    ServiceLinkPublicListView,
)

urlpatterns = [
    # 公开接口
    path("homepage/links/", ServiceLinkPublicListView.as_view(), name="homepage-links-public"),
    # 管理接口
    path("homepage/admin/links/", ServiceLinkAdminListCreateView.as_view(), name="homepage-links-admin-list"),
    path("homepage/admin/links/<uuid:pk>/", ServiceLinkAdminDetailView.as_view(), name="homepage-links-admin-detail"),
]
