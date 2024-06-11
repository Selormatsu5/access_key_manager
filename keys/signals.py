from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from .models import CustomUser  # Adjust the import to your custom user model

@receiver(post_save, sender=CustomUser)
def assign_group_on_creation(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for user creation: {instance.email}")
        print(f"User type is: {instance.user_type}")
        
        if instance.user_type == 'Admin':
            admin_group, created = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)
            print(f"User assigned to Admin group: {instance.groups.all()}")
        elif instance.user_type == 'IT':
            it_group, created = Group.objects.get_or_create(name='IT Personnel')
            instance.groups.add(it_group)
            print(f"User assigned to IT Personnel group: {instance.groups.all()}")
        else:
            print("User type is neither 'Admin' nor 'IT'")


