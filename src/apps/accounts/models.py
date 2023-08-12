from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from apps.core.models import TimestampedModel
from .manager import UserManager


class Organization(TimestampedModel):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}/{self.name}"

    class Meta:
        ordering = ['-id']


class User(AbstractBaseUser, TimestampedModel):
    email = models.EmailField(max_length=120, unique=True, db_index=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    organizations = models.ManyToManyField(Organization, blank=True)
    avatar = models.ImageField(upload_to="images/avatar/", null=True, blank=True)
    activated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password required by default

    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True  # does user have a specific permision, simple answer - yes

    def has_module_perms(self, app_label):
        return True  # does user have permission to view the app 'app_label'?

