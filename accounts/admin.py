from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.
    Extends Django's built-in UserAdmin to work with our email-based authentication.
    """
    
    # What to display in the list view (table columns)
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined', 'last_login')
    
    # Filters in the right sidebar
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    
    # Search bar fields
    search_fields = ('email',)
    
    # Default ordering
    ordering = ('-date_joined',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for the "add user" view (when creating a new user)
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Make password field read-only in the edit view (since it's hashed)
    readonly_fields = ('last_login', 'date_joined')