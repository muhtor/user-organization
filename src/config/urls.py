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
from apps.accounts.api.v1.views import CustomTokenObtainPairView, CustomTokenRefreshView

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Baraka ERP API",
        default_version='v1',
        description="For any questions, contact https://t.me/Fatabaeva",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dts@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('baraka-admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # for browsable API - login and logout

    path('auth-token/create/', CustomTokenObtainPairView.as_view(), name="tokencreate"),
    path('auth-token/refresh/', CustomTokenRefreshView.as_view(), name="tokenrefresh"),

    path('api/accounts/', include('apps.accounts.api.urls')),
    path('api/employee/', include('apps.employees.api.urls')),
    path('api/company/', include('apps.branches.api.urls')),
    path('api/address/', include('apps.addresses.api.urls')),
    path('api/upload/', include('apps.uploads.api.urls')),
    path('api/products/', include('apps.products.api.urls')),
    path('api/main/', include('apps.main.api.urls')),
    path('api/credit/', include('apps.credit.api.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
