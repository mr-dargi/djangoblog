from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManger


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICE = (
        ("superuser", "Superuser"),
        ("admin", "Admin"),
        ("author", "Author"),
        ("user", "User"),
        ("premium", "Premium"),
    )
    
    email = models.EmailField(max_length=255, unique=True, verbose_name="email address")
    user_name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default="user")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    

    objects = UserManger()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.user_name
    
    @property
    def is_staff(self):
        return self.is_admin