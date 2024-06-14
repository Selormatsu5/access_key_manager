from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .utils import generate_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    other_names = models.CharField(max_length=20, blank=True, null=True)
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=16, unique=True, default=generate_random_string)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_of_procurement = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    revoked_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=30)  # Set default expiry to 30 days from now
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

    def revoke(self):
        self.status = 'revoked'
        self.revoked_date = timezone.now()
        self.save()

    @staticmethod
    def create_key(user):
        try:
            # Check for existing key
            existing_key = AccessKey.objects.get(user=user)
            
            if existing_key.status == 'active':
                raise ValueError('User already has an active key.')
            else:
                # Revoke the existing key
                existing_key.revoke()
                # Issue a new key by updating the existing record
                existing_key.key = generate_random_string(16).upper()
                existing_key.status = 'active'
                existing_key.expiry_date = timezone.now() + timedelta(days=30)
                existing_key.revoked_date = None
                existing_key.save()
                return existing_key
        except AccessKey.DoesNotExist:
            # If no existing key, create a new one
            expiry_date = timezone.now() + timedelta(days=30)
            new_key = AccessKey(user=user, status='active', expiry_date=expiry_date)
            new_key.save()
            return new_key
