from django.contrib import admin
from .models import Specialty, DoctorProfile


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing medical specialties.
    """
    
    # What to display in the list view (table columns)
    list_display = ('name', 'description')
    
    # Search bar fields
    search_fields = ('name', 'description')
    
    # Default ordering
    ordering = ('name',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for managing doctor profiles.
    """
    
    # What to display in the list view (table columns)
    list_display = ('doctor_name', 'user_email', 'specialty', 'availability_status', 'is_verified', 'consultation_fee', 'created_at')
    
    # Filters in the right sidebar
    list_filter = ('specialty', 'availability_status', 'is_verified', 'created_at')
    
    # Search bar fields
    search_fields = ('user__email', 'license_number', 'specialty__name')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('User Account', {
            'fields': ('user',),
            'description': 'Link to the user account (must have DOCTOR role)'
        }),
        ('Professional Information', {
            'fields': ('specialty', 'license_number', 'qualifications', 'bio', 'consultation_fee')
        }),
        ('Status & Availability', {
            'fields': ('availability_status', 'is_verified'),
            'description': 'Control doctor availability and verification status'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Make timestamp fields read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Custom method to display doctor name in list view
    @admin.display(description='Doctor Name', ordering='user__email')
    def doctor_name(self, obj):
        return f"Dr. {obj.user.email}"
    
    # Custom method to display user email in list view
    @admin.display(description='Email', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email