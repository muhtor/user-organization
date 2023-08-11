from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("user/<int:user_id>/", views.UserUpdateDestroyView.as_view(), name="user"),
]

router.register(r'organization', views.OrganizationViewSet, basename='organization')
urlpatterns += router.urls
