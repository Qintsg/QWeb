"""IAM URL 配置。"""

from django.urls import path

from apps.iam.api.views import (
    MePermissionsView,
    PermissionListView,
    RoleDetailView,
    RoleListCreateView,
    RolePermissionsView,
    UserOverrideListView,
    UserOverrideManageView,
    UserRoleAssignView,
    UserRoleListView,
)

app_name = "iam"

urlpatterns = [
    # ---- 当前用户权限（放在最前避免被 users/<int> 匹配） ----
    path("me/permissions/", MePermissionsView.as_view(), name="me-permissions"),

    # ---- 权限 ----
    path("permissions/", PermissionListView.as_view(), name="permission-list"),

    # ---- 角色 ----
    path("roles/", RoleListCreateView.as_view(), name="role-list-create"),
    path("roles/<uuid:role_id>/", RoleDetailView.as_view(), name="role-detail"),
    path("roles/<uuid:role_id>/permissions/", RolePermissionsView.as_view(), name="role-permissions"),

    # ---- 用户角色 ----
    path("users/<int:user_id>/roles/", UserRoleListView.as_view(), name="user-role-list"),
    path("users/<int:user_id>/roles/manage/", UserRoleAssignView.as_view(), name="user-role-manage"),

    # ---- 用户权限覆盖 ----
    path("users/<int:user_id>/overrides/", UserOverrideListView.as_view(), name="user-override-list"),
    path("users/<int:user_id>/overrides/manage/", UserOverrideManageView.as_view(), name="user-override-manage"),
]
