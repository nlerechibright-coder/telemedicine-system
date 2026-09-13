from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import CustomUser
from doctors.models import DoctorProfile


class DoctorProfileInlineForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = (
            'specialty',
            'license_number',
            'qualifications',
            'bio',
            'consultation_fee',
            'whatsapp_number',
            'availability_status',
            'is_verified',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['availability_status'] = ''
        for field_name in ('specialty', 'license_number', 'qualifications', 'consultation_fee', 'availability_status'):
            self.fields[field_name].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not self.has_changed():
            return cleaned_data

        required_fields = ('specialty', 'license_number', 'qualifications', 'consultation_fee', 'availability_status')
        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, 'This field is required for a doctor profile.')
        return cleaned_data


class DoctorProfileInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if self.instance.is_doctor and not any(form.has_changed() and not form.cleaned_data.get('DELETE') for form in self.forms):
            raise ValidationError('A doctor must have a completed Doctor Profile.')


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    form = DoctorProfileInlineForm
    formset = DoctorProfileInlineFormSet
    extra = 1
    max_num = 1
    can_delete = False
    fields = (
        'specialty',
        'license_number',
        'qualifications',
        'bio',
        'consultation_fee',
        'whatsapp_number',
        'availability_status',
        'is_verified',
    )


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

    inlines = (DoctorProfileInline,)