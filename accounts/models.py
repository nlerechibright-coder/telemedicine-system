from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        DOCTOR = 'DOCTOR', 'Doctor'
        MANAGER = 'MANAGER', 'Manager'
        ADMIN = 'ADMIN', 'Administrator'
    
    email = models.EmailField(unique=True, verbose_name='Email Address')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT, verbose_name='User Role')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff Status')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date Joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Last Login')
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
    
    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
    
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN