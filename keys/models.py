from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_choices = [
        ('IT', 'School IT Personnel'),
        ('Admin', 'Micro-Focus Admin'),
    ]
    user_type = models.CharField(max_length=5, choices=user_type_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class AccessKey(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date_of_procurement = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"Key for {self.user.email} - Status: {self.status}"
