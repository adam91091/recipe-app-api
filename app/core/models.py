"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # we just passing kwargs into the model instance
        # anytime when new fields will be added in user field
        # you do not need to update this code
        # under self.model UserManager has instance to User
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # password can be excluded when we want to have unusable user
        # set encrypted password
        user.set_password(password)
        # passing self._db is for support of multiple databases
        # when used in this way, this code will work under different
        # database - best practice to pass using=self._db
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign custom user manager to our custom user class
    objects = UserManager()

    USERNAME_FIELD = 'email'
