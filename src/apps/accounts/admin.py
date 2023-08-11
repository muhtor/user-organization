from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy

from .models import User, UserProfile, Role, CustomPermission, StaffPermission

admin.site.unregister(Group)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = ("<a href=\"%s\"><strong>Change the Password</strong></a>."
                                             ) % reverse_lazy('admin:auth_user_password_change',
                                                              args=[self.instance.id])

    def clean_password(self):
        return self.initial["password"]


@admin.register(User)
class AdminView(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    filter_horizontal = ()
    list_display = ('id', 'username', 'phone', 'status', 'is_staff', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('id', 'username', 'email', 'phone')

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'phone',
                'phone_2',
                'activated_date',
                'status',
                'is_active',
                'is_staff',
                'is_superuser',
                'password',
            )
        }),
        ('Important dates', {'fields': ('last_login',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'phone_2',
                'activated_date',
                'status',
                'is_active',
                'is_staff',
                'is_superuser',
                'password1',
                'password2',
            )
        }),
        # ('Personal info', {'fields': ('groups',)}),
        # ('Permissions', {'fields': ('user_permissions',)}),
    )

    list_display_links = ('id', 'username', 'phone')
    ordering = ('-id',)


@admin.register(UserProfile)
class AdminView(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'status'
    )
    list_display_links = ('phone', )


@admin.register(Role)
class AdminView(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'creator',
        'codes',
        'status'
    )
    list_display_links = ('name', )


@admin.register(CustomPermission)
class AdminView(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'permission_code',
        'parent',
    )
    list_display_links = ('title', )
    search_fields = ['id', 'title', ]


@admin.register(StaffPermission)
class AdminView(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'user',
        'role',
        'status'
    )
    list_display_links = ('creator', 'user')


