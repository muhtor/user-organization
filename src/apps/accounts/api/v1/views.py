from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from apps.core.api.middleware import APIMiddleware


class TokenObtainPairView(TokenViewBase, APIMiddleware):
    """Return JWT tokens (access and refresh) for specific user based on email and password."""
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)


class TokenRefreshView(TokenViewBase, APIMiddleware):
    """Renew tokens (access and refresh) with new expire time based on specific user's access token."""
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)



