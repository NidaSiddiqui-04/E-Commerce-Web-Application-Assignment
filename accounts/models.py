
# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    # other fields as needed
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=40,null=True,blank=True)
    email=models.EmailField(null=True,blank=True) 
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # nothing else is required for superuser creation

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
