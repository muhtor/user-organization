from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_superuser=False, **kwargs):
        if not email:
            raise ValueError('Users must have a email')

        user = self.model(email=email)
        if email is not None:
            user.email = self.normalize_email(email)

        user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, email, password=None):
        if not password:
            raise ValueError('staff/admins must have a password.')
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not password:
            raise ValueError('superusers must have a password.')
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
