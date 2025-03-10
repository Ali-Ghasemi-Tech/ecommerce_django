from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not phone_number:
            raise ValueError('Phone number is required')

        email = extra_fields.pop('email', None)
        if email:
            email = self.normalize_email(email)

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, phone_number, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=11, unique=True) 
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username
    
    def save(self, *args , **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args , **kwargs)
    

class Profile(models.Model):
    user = models.OneToOneField(Account , on_delete=models.CASCADE)
    email_verification_token = models.CharField(max_length=255 , blank=True , null= True)
    phone_verification_token = models.CharField(max_length=255 , blank=True , null= True)
    
    def generate_verification_token(self):
        self.email_verification_token = str(uuid.uuid4())
        self.save()
        return self.email_verification_token

    def generate_phone_verification_token(self):
        verification_token = str(uuid.uuid4())
        self.phone_verification_token = verification_token[0:4]
        self.save()
        return self.phone_verification_token
