"""ERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.accounts.api.v1.views import TokenObtainPairView, TokenRefreshView

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="User management API",
        default_version='v1',
        description="For any questions, contact https://t.me/Muxtor_yusuf",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # for browsable API - login and logout

    path('api/v1/auth-token/create/', TokenObtainPairView.as_view(), name="tokencreate"),
    path('api/v1/auth-token/refresh/', TokenRefreshView.as_view(), name="tokenrefresh"),

    path('api/v1/accounts/', include('apps.accounts.api.v1.urls')),
    # path('api/v2/accounts/', include('apps.accounts.api.v2.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
