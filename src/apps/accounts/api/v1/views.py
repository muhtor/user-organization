from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .serializers import RegisterSerializer, OrganizationSerializer, UserUpdateDestroySerializer, UserDetailSerializer
from apps.accounts.models import User, Organization
from apps.core.api import generics


class TokenObtainPairView(generics.CustomTokenView):
    """Return JWT tokens (access and refresh) for specific user based on email and password."""
    serializer_class = TokenObtainPairSerializer
    tags = ["Auth API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)


class TokenRefreshView(generics.CustomTokenView):
    """Renew tokens (access and refresh) with new expire time based on specific user's access token."""
    serializer_class = TokenRefreshSerializer
    tags = ["Auth API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.success_response(results=serializer.validated_data)


class RegisterView(generics.CustomCreateView):
    """
    http://127.0.0.1:8000/api/v1/accounts/register/
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    tags = ["Register API"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success_response(results=serializer.validated_data, status_code=status.HTTP_201_CREATED)


class UserDetailView(generics.CustomUpdateDestroyView):
    """
    http://127.0.0.1:8000/api/v1/accounts/user/{id}/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateDestroySerializer
    queryset = User.objects.all()
    tags = ["User API"]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserDetailSerializer(instance)
        return self.success_response(results=serializer.data)

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['id'])


class UserListView(generics.CustomListView):
    """
    http://127.0.0.1:8000/api/v1/accounts/user/all/
    """
    tags = ["User API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class OrganizationListView(generics.CustomListView):
    """
    http://127.0.0.1:8000/api/v1/accounts/organization/all/
    """
    tags = ["Organization API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class OrganizationViewSet(generics.APILayer, generics.viewsets.ViewSet):
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


