from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import CustomUser
from doctors.models import DoctorProfile


# 1. Custom forms to handle 'email' instead of 'username'
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'role', 'is_active', 'is_staff', 'is_superuser')


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
        # Only enforce doctor profile validation if the user is actually a doctor
        if getattr(self.instance, 'is_doctor', False) and not any(form.has_changed() and not form.cleaned_data.get('DELETE') for form in self.forms):
            raise ValidationError('A doctor must have a completed Doctor Profile.')


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    form = DoctorProfileInlineForm
    formset = DoctorProfileInlineFormSet
    extra = 0  # Changed to 0 so it doesn't force a blank doctor profile for clients
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

    def get_queryset(self, request):
        # Only show the inline data if the user is a doctor
        qs = super().get_queryset(request)
        if self.instance.pk and not self.instance.is_doctor:
            return qs.none()
        return qs


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 2. Tell Django to use our custom forms
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    inlines = (DoctorProfileInline,)

    def get_inline_instances(self, request, obj=None):
        # 3. Only show the DoctorProfile inline if the user is a doctor
        if obj and obj.is_doctor:
            return super().get_inline_instances(request, obj)
        return []