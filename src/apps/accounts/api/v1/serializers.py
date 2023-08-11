from rest_framework import serializers
from apps.accounts.models import User, Organization
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Organization.objects.all())]
    )

    class Meta:
        model = Organization
        fields = ("id", "name", "description")
        extra_kwargs = {
            'name': {'required': True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserUpdateDestroySerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(many=True, queryset=Organization.objects.all())

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'first_name', 'organizations', 'avatar')
        extra_kwargs = {'organizations': {'required': False}}


class UserDetailSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'first_name', 'organizations', 'avatar')





