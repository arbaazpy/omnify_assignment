from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation using email instead of username.
    """

    def create_user(self, email, name, password=None):
        """
        Creates and returns a user with the given email, name, and password.
        """
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and returns a superuser with the given email, name, and password.
        """
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the unique identifier instead of username.

    Fields:
        email (str): Unique email address used for login.
        name (str): User's full name.
        is_active (bool): Whether the user's account is active.
        is_staff (bool): Whether the user is a staff member.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        String representation of the user (email).
        """
        return self.email
