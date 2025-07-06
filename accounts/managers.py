from django.db  import models
from django.contrib.auth.models import BaseUserManager


class MyUserManger(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        """
        Creates and saves a User with the given email, user_name
        and password.
        """
        if not email:
            raise ValueError("برای ساخت حساب وجود ایمیل ضروری است")
        
        if not user_name:
            raise ValueError("ورود نام کاربری ضروری است")
        
        user = self.model(email=self.normalize_email(email), user_name=user_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, user_name, password=None):
        """
        Creates and saves a superuser with the given email, user_name
        and password.
        """
        user = self.create_user(
            email,
            user_name=user_name,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user