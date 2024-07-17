from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):

    def create_user(self, full_name, email,  password=None):

        user = self.model( full_name=full_name, email=email, )
        user.set_password(password)

        user.save()
        token = Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError("Password shouldn't be None")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_varified = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=225,unique=True,null=True, blank=True)
    full_name = models.CharField(max_length=225, null=True, blank=True)
    profile_pic =  models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=225, null=True, blank=True)
    occupation = models.CharField(max_length=225, null=True, blank=True)
    phone = models.CharField(max_length=225, unique=True,null=True, blank=True)
    whatsapp_num = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=225, unique=True, db_index=True)
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }