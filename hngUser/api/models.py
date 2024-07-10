from uuid import uuid4

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName, lastName=lastName, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    userId = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    email = models.CharField(unique=True, null=False, max_length=100)
    firstName = models.CharField(null=False, max_length=50)
    lastName = models.CharField(null=False, max_length=50)
    password = models.CharField(null=False, max_length=50)
    phone = models.CharField(blank=True, max_length=18)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


class Organisation(models.Model):
    orgId = models.UUIDField(unique=True, default=uuid4, editable=False)
    name = models.CharField(null=False, max_length=100, unique=True)
    description = models.CharField(blank=True, max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orgs_created', null=False)
    users = models.ManyToManyField(User, related_name='organisations')
    
    def __str__(self) -> str:
        return self.name
