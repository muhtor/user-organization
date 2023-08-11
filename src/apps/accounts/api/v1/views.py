from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.core.api import generics
from apps.core.services.status import *
from apps.employees.models import StaffUser
from . import serializers as ser
from apps.accounts.utils.services import AccountController
from apps.accounts.models import User, CustomPermission, Role, StaffPermission
from apps.core.services import controller as ctrl
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import BaseCreateSerializer, BaseRoleSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    tags = ["Auth API"]


class CustomTokenRefreshView(TokenRefreshView):
    tags = ["Auth API"]


class UserMeAPIView(generics.CustomAPIView):
    """{{BASE}}/api/accounts/v1/me/"""
    tags = ["Auth API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.UserMeSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return self.success_response(results=serializer.data)


class CheckUsernameAPIView(generics.CustomAPIView):
    """ {{BASE}}/api/accounts/v1/check/?username=john """
    tags = ["Auth API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.UserMeSerializer

    def get(self, request):
        username = request.GET.get('username')
        if User.objects.filter(username=username).exists():
            raise CustomValidationError(msg=f"`{username}` already exists")
        return self.success_response()


class UsersViewSet(generics.CustomCrudView, AccountController):
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.UserMeSerializer
    tags = ["User API"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object_pk()
        serializer = self.serializer_class(instance=instance)
        return self.success_response(results=serializer.data)

    def create(self, request, *args, **kwargs):
        raise CustomValidationError(msg="Method not allowed")

    def update(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object_pk()
        serializer_data = {
            "username": data.get('username', user.username),
            "email": data.get('email', user.email),
            "phone": data.get('phone', user.phone),
        }

        serializer = self.serializer_class(user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(results=serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.get_object_pk()
        if user.is_superuser:
            raise CustomValidationError(msg="SuperAdmin cannot be deleted")
        user.delete()
        return self.success_response()

    def get_queryset(self):
        if self.kwargs:
            return User.objects.filter(id=self.kwargs['pk'])


class PermissionListView(generics.CustomSimpleListView):
    """
    GET: http://127.0.0.1:6060/api/accounts/v1/permission-list/
    """
    tags = ["Permissions API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.CustomPermissionSerializer
    queryset = CustomPermission.objects.filter(parent__isnull=True)


class AbstractRoleViewSet(generics.CustomCrudView, AccountController):
    """
    GET: {{BASE}}/api/accounts/v1/roles/{id}/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BaseRoleSerializer
    tags = ["Role API"]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        data['codes'] = self.validator_perms()
        serializer = BaseCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(results=self.serializer_class(instance=serializer.instance).data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object_pk()
        serializer = self.serializer_class(instance=obj)
        return self.success_response(results=serializer.data)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object_pk()
        obj.delete()
        return self.success_response()

    def update(self, request, *args, **kwargs):
        role = self.get_object_pk()
        data = request.data
        codes = data.get('codes', None)
        if codes:
            codes = self.validator_perms()
            role.codes = codes
            role.save()
        else:
            codes = role.codes

        serializer_data = {
            "name": data.get('name', role.name),
            "description": data.get('description', role.description),
            "status": data.get('status', role.status),
            "codes": codes
        }

        serializer = BaseCreateSerializer(role, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(results=self.serializer_class(instance=role).data)

    def get_queryset(self):
        if self.kwargs:
            return Role.objects.filter(id=self.kwargs['pk'])


class RoleListView(generics.CustomListView):
    """
    GET: http://127.0.0.1:6060/api/accounts/v1/permission-list/
    """
    tags = ["Role API"]
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.RoleListSerializer

    def get_queryset(self):
        params = self.request.query_params
        query = params.get('q', None)
        role_status = params.get('status', None)
        order_by = params.get('order', None)

        queryset = Role.objects.order_by(self.order_by_lookup(by=order_by))

        if query is not None:
            queryset = queryset.filter(Q(name__icontains=query) | Q(codes__icontains=query))

        if role_status is not None:
            queryset = queryset.filter(status=role_status)

        return queryset


class StaffRoleViewSet(generics.CustomCrudView, AccountController):
    """
    GET: {{BASE}}/api/accounts/v1/staff-role/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ser.UserMeSerializer
    tags = ["Role API"]

    def create(self, request, *args, **kwargs):
        data = request.data

        # try:
        staff = StaffUser.objects.get(id=data['staff_id'])
        user = staff.user
        qs = StaffPermission.objects.filter(user_id=user.id, role_id=data['role_id'])
        if not qs.exists():
            StaffPermission.objects.create(creator_id=user.id, user_id=staff.id, staff_id=staff.id, role_id=data['role_id'])
        self.set_staff_password(user=user, password=data.get('password', None))
        serializer = self.serializer_class(instance=user)
        return self.success_response(results=serializer.data)
        # except Exception as e:
        #     raise CustomValidationError(msg=str(e.args))

    def set_staff_password(self, user, password):
        password = self.make_default_password(raw_password=password)
        user.set_password(password)
        user.save()

    def retrieve(self, request, *args, **kwargs):
        role = self.get_object_pk()
        serializer = self.serializer_class(instance=role.user)
        return self.success_response(results=serializer.data)

    def delete(self, request, *args, **kwargs):
        staff = self.get_object_pk()
        qs = StaffPermission.objects.filter(user_id=staff.user_id)
        if qs.exists():
            qs.delete()
        return self.success_response()

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            instance = StaffPermission.objects.filter(staff_id=data['staff_id']).latest('created_at')
            if data.get('password', None):
                self.set_staff_password(user=instance.user, password=data.get('password'))
            instance.role_id = data.get("role_id", instance.role_id)
            instance.save()
            serializer = self.serializer_class(instance=instance.user)
            return self.success_response(results=serializer.data)
        except Exception as e:
            raise CustomValidationError(msg=str(e.args))

    def get_queryset(self):
        if self.kwargs:
            return StaffUser.objects.filter(id=self.kwargs['pk'])
