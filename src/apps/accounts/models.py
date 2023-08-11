from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=120, db_index=True, unique=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    phone_2 = models.CharField(max_length=64, blank=True, null=True)
    activated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # email and password required by default

    objects = UserManager()

    def __str__(self):
        return f"{self.id}/{self.username}"

    def has_perm(self, perm, obj=None):
        return True  # does user have a specific permision, simple answer - yes

    def has_module_perms(self, app_label):
        return True  # does user have permission to view the app 'app_label'?

