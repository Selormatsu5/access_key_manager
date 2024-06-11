from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from .models import CustomUser  # Adjust the import to your custom user model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_group_on_creation(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'Admin':
            admin_group, created = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)
        elif instance.user_type == 'IT':
            it_group, created = Group.objects.get_or_create(name='IT Personnel')
            instance.groups.add(it_group)
