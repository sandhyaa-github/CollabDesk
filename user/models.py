from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          phone=phone, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
