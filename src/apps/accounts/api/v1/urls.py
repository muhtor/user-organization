from django.urls import path, re_path
from . import views

app_name = "accounts"

urlpatterns = (
    path('auth-me/', views.UserMeAPIView.as_view(), name="me"),
    path('check/', views.CheckUsernameAPIView.as_view(), name="me"),

    re_path(r'^users/(?P<pk>[0-9]+)*', views.UsersViewSet.as_view(), name="users"),
    re_path(r'^roles/(?P<pk>[0-9]+)*', views.AbstractRoleViewSet.as_view(), name="roles"),

    path('permissions/', views.PermissionListView.as_view(), name="permissions"),
    path('role-list/', views.RoleListView.as_view(), name="role-list"),
    re_path(r'^staff-role/(?P<pk>[0-9]+)*', views.StaffRoleViewSet.as_view(), name="staff_role"),
)
