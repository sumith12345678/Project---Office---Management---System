
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        return self.create_user(username, password, **extra_fields)


ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'HR'),
    (3, 'Employee')

]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=True)
    role = models.IntegerField(choices=ROLE_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def _str_(self):
        return self.username



class Department(models.Model):
    DeptName = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.DeptName
    
    

class Notification(models.Model):
    news_title = models.CharField(max_length=30)
    news_data = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)    