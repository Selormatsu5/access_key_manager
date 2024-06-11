from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from keys.models import CustomUser

class Command(BaseCommand):
    help = 'Assigns users to Admin and IT Personnel groups'

    def handle(self, *args, **options):
        # Ensure groups exist or create them
        admin_group, created = Group.objects.get_or_create(name='Admin')
        it_group, created = Group.objects.get_or_create(name='IT Personnel')

        # Replace 'admin_user' and 'it_user' with the actual usernames in your database
        try:
            admin_user = CustomUser.objects.get(username='admin_user')  # Replace with actual username
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {admin_user.username} to Admin group'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user does not exist'))

        try:
            it_user = CustomUser.objects.get(username='it_user')  # Replace with actual username
            it_user.groups.add(it_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {it_user.username} to IT Personnel group'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('IT Personnel user does not exist'))
