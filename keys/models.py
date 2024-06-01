from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from .utils import generate_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_choices = [
        ('IT', 'School IT Personnel'),
        ('Admin', 'Micro-Focus Admin'),
    ]
    user_type = models.CharField(max_length=5, choices=user_type_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class AccessKey(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=16, unique=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date_of_procurement = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_random_string(16).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Key for {self.user.email} - Status: {self.status}"

    def is_active(self):
        return self.status == 'active' and self.expiry_date > timezone.now()

    def deactivate(self):
        self.status = 'expired'
        self.save()

    @staticmethod
    def create_key(user):
        if AccessKey.objects.filter(user=user, status='active').exists():
            raise ValueError('User already has an active key.')
        expiry_date = timezone.now() + timedelta(days=30)
        access_key = AccessKey(user=user, status='active', expiry_date=expiry_date)
        access_key.save()
        return access_key
