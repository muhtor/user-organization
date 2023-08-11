from rest_framework import serializers
from apps.core.services.status import *
from apps.core.services import controller as ctrl


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""

    password = serializers.CharField(max_length=128, min_length=5, write_only=True, required=True)

    class Meta:
        model = ctrl.User
        fields = (
            'username',
            'password',
            'email',
            'phone',
        )

    def create(self, validated_data):
        password = validated_data.get('password', None)
        if password is None:
            raise CustomValidationError(msg="password required", status_code=status.HTTP_400_BAD_REQUEST)

        user = ctrl.User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    # profile = ProfileSerializer(write_only=True)  # never expose profile information hence `write_only=True`
    # first_name = serializers.CharField(source='profile.first_name', read_only=True)
    # last_name = serializers.CharField(source='profile.last_name', read_only=True)

    class Meta:
        model = ctrl.User

        fields = ('username', 'email', 'phone', 'password') #, 'first_name', 'last_name')

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)
        # profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        # for (key, value) in profile_data.items():
        #     setattr(instance.profile, key, value)
        # instance.profile.save()

        return instance


class UserMiniSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""

    class Meta:
        model = ctrl.User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'phone_2',
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""

    class Meta:
        model = ctrl.User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'roles',
        )


class SubPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ctrl.CustomPermission
        fields = (
            'id',
            'title',
            'permission_code',
        )


class CustomPermissionSerializer(serializers.ModelSerializer):
    children = SubPermissionSerializer(many=True, required=False)

    class Meta:
        model = ctrl.CustomPermission
        fields = ('id', 'title', 'permission_code', 'children')


class MiniCustomPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ctrl.CustomPermission
        fields = ('id', 'title', 'permission_code')


class BaseCreateSerializer(serializers.ModelSerializer):
    codes = serializers.CharField(allow_null=False)

    class Meta:
        model = ctrl.Role
        fields = (
            'id',
            'name',
            'description',
            'status',
            'creator',
            'codes',
        )


class BaseRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ctrl.Role
        fields = (
            'id',
            'name',
            'description',
            'status',
            'permissions',
        )


class RoleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ctrl.Role
        fields = (
            'id',
            'name',
            'status',
        )

