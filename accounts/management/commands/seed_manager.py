from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Seeds the fixed management account (Uche1234) into the database.'

    def handle(self, *args, **kwargs):
        # Note: Since the CustomUser model uses EmailField as USERNAME_FIELD, 
        # we use a valid email format for the fixed identifier.
        manager_email = 'Uche1234@telemedicine.com'
        manager_password = 'Menny12345'
        
        user, created = CustomUser.objects.get_or_create(
            email=manager_email,
            defaults={
                'role': CustomUser.Role.MANAGER,
                'is_active': True,
                'is_staff': False, # Not a Django admin superuser
                'is_superuser': False,
            }
        )
        
        if created:
            user.set_password(manager_password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully created management account: {manager_email}'))
        else:
            # Ensure role and password are correct if the user already exists
            if user.role != CustomUser.Role.MANAGER:
                user.role = CustomUser.Role.MANAGER
                user.save()
                self.stdout.write(self.style.WARNING(f'⚠️ Updated existing user {manager_email} to MANAGER role.'))
            
            # We don't reset the password if it already exists to avoid locking out 
            # a manager who has already changed their password, unless explicitly forced.
            self.stdout.write(self.style.SUCCESS(f'ℹ️ Management account {manager_email} already exists.'))