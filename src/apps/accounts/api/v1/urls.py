from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("user/<int:id>/", views.UserDetailView.as_view(), name="user"),
    path("user/all/", views.UserListView.as_view(), name="users"),
    path("organization/all/", views.OrganizationListView.as_view(), name="organizations"),
]

router.register(r'organization', views.OrganizationViewSet, basename='organization')
urlpatterns += router.urls
