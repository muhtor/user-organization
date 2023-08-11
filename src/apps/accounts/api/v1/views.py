from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from apps.core.api.middleware import APIMiddleware
from .serializers import RegisterSerializer, OrganizationSerializer
from apps.accounts.models import User, Organization
from rest_framework import permissions, generics, viewsets


class TokenObtainPairView(TokenViewBase, APIMiddleware):
    """Return JWT tokens (access and refresh) for specific user based on email and password."""
    serializer_class = TokenObtainPairSerializer
    tags = ["Auth API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)


class TokenRefreshView(TokenViewBase, APIMiddleware):
    """Renew tokens (access and refresh) with new expire time based on specific user's access token."""
    serializer_class = TokenRefreshSerializer
    tags = ["Auth API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)


class RegisterView(generics.CreateAPIView, APIMiddleware):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    tags = ["Register API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success_response(results=serializer.validated_data)


class UserUpdateDestroyView(generics.CreateAPIView, APIMiddleware):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    tags = ["User API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success_response(results=serializer.validated_data)


class OrganizationViewSet(APIMiddleware, viewsets.ViewSet):
    """
    http://127.0.0.1:8000/api/v1/accounts/organization/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer
    tags = ["Organization API"]

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object_pk()
        serializer = self.serializer_class(instance=obj)
        return self.success_response(results=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(results=serializer.data)

    def update(self, request, *args, **kwargs):
        obj = self.get_object_pk()
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(results=serializer.data)

    def destroy(self, request, pk):
        obj = self.get_object_pk()
        obj.delete()
        return self.success_response()

    def get_queryset(self):
        if self.kwargs:
            return Organization.objects.filter(id=self.kwargs['pk'])



