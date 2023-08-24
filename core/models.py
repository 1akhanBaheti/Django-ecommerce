from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .user_manager import UserManager

class User(AbstractUser,PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    first_name =models.CharField(max_length=255,blank=False,null=False)
    last_name =models.CharField(max_length=255,blank=False,null=False)
    username =models.CharField(max_length=1,null=True,unique=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['first_name','last_name']
    

