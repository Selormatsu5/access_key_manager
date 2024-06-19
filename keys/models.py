from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .utils import generate_random_string
from django.contrib.auth import get_user_model  

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    user_type_choices = [
        ('IT', 'School IT Personnel'),
        ('Admin', 'Micro-Focus Admin'),
    ]
    user_type = models.CharField(max_length=5, choices=user_type_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'other_names']

    def __str__(self):
        return self.email

class AccessKey(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=16, unique=True, default=generate_random_string)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_of_procurement = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    revoked_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=30)  # Set default expiry date if not provided
        if not self.key:
            self.key = generate_random_string(16).upper()  # Generate a new key if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Key for {self.user.email} - Status: {self.status}"

    def is_active(self):
        return self.status == 'active' and self.expiry_date > timezone.now()

    def deactivate(self):
        self.status = 'expired'
        self.save()

    def revoke(self):
        self.status = 'revoked'
        self.revoked_date = timezone.now()
        self.save()

    @staticmethod
    def create_key(user):
        # Deactivate any existing active key
        active_keys = AccessKey.objects.filter(user=user, status='active')
        for key in active_keys:
            key.revoke()  # Revoke the existing active keys

        # Create a new key
        new_key = AccessKey(
            user=user,
            status='active',
            expiry_date=timezone.now() + timedelta(days=30),
            date_of_procurement=timezone.now(),
            key=generate_random_string(16).upper()
        )
        new_key.save()
        return new_key



class OTP(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=2)  # OTP expires in 2 minutes

    def __str__(self):
        return f'OTP for {self.user.email}'
