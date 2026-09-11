from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier
    for authentication instead of username.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the Telemedicine System.
    Uses email as the unique identifier instead of username.
    """
    
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        DOCTOR = 'DOCTOR', 'Doctor'
        ADMIN = 'ADMIN', 'Administrator'
    
    # Authentication fields
    email = models.EmailField(unique=True, verbose_name='Email Address')
    
    # User role
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='User Role'
    )
    
    # Status fields
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff Status')
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date Joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Last Login')
    
    # Use our custom manager
    objects = CustomUserManager()
    
    # Tell Django to use email instead of username for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's email as their full name."""
        return self.email
    
    def get_short_name(self):
        """Return the user's email as their short name."""
        return self.email
    
    @property
    def is_client(self):
        """Check if user is a client."""
        return self.role == self.Role.CLIENT
    
    @property
    def is_doctor(self):
        """Check if user is a doctor."""
        return self.role == self.Role.DOCTOR
    
    @property
    def is_admin(self):
        """Check if user is an administrator."""
        return self.role == self.Role.ADMIN