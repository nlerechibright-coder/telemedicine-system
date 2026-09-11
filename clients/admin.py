from django.contrib import admin
from .models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for managing client profiles.
    """
    
    # What to display in the list view (table columns)
    list_display = ('full_name', 'user_email', 'phone_number', 'gender', 'blood_type', 'created_at')
    
    # Filters in the right sidebar
    list_filter = ('gender', 'blood_type', 'created_at')
    
    # Search bar fields
    search_fields = ('full_name', 'user__email', 'phone_number')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('User Account', {
            'fields': ('user',),
            'description': 'Link to the user account'
        }),
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'phone_number', 'address')
        }),
        ('Health Information', {
            'fields': ('blood_type', 'chronic_conditions', 'allergies', 'current_medications'),
            'description': 'Medical information for doctor reference'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Make timestamp fields read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Custom method to display user email in list view
    @admin.display(description='Email', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email