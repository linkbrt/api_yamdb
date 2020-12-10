from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

GROUPS = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Profile(AbstractUser):
    username = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    role = models.CharField(max_length=20,
                            default='user',
                            choices=GROUPS)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()


class Confirm(models.Model):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=10)
