import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings

BASE_DIR = settings.BASE_DIR

def cv_file_name(instance, filename):
    ext = filename.split('.')[-1]
    file_name = f"{instance.first_name}_{instance.last_name}_{instance.email}.{ext}"
    return os.path.join('cv/', file_name)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email,
            password=password,
            **extra_fields,
        )


class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    cv = models.FileField(upload_to=cv_file_name)
    facebook_username = models.CharField(max_length=50, blank=True)
    facebook_password = models.CharField(max_length=50, blank=True)
    instagram_username = models.CharField(max_length=50, blank=True)
    instagram_password = models.CharField(max_length=50, blank=True)
    checkbox1 = models.BooleanField(default=False)
    checkbox2 = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='myuser_permissions',
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )    
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email is required by default.

    objects = UserManager()
    groups = models.ManyToManyField(Group, blank=True, related_name='myuser_set', verbose_name=_('groups'), help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'))
    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    