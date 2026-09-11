from django import forms
from .models import DoctorProfile


class DoctorProfileEditForm(forms.ModelForm):
    """
    Form for doctors to edit their own professional information.
    Excludes fields that are managed by administrators (user, is_verified, availability_status).
    """
    
    class Meta:
        model = DoctorProfile
        fields = ['qualifications', 'bio', 'consultation_fee', 'whatsapp_number']
        
        widgets = {
            'qualifications': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g., MD, Board Certified in Internal Medicine'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Tell patients about your experience and approach to care...'
            }),
            'consultation_fee': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 08029011944 or +2348029011944'
            }),
        }
        
        labels = {
            'qualifications': 'Professional Qualifications',
            'bio': 'Professional Bio',
            'consultation_fee': 'Consultation Fee ($)',
            'whatsapp_number': 'WhatsApp Number',
        }
        
        help_texts = {
            'consultation_fee': 'Enter your consultation fee in dollars (e.g., 50.00)',
            'whatsapp_number': 'Used only to open your WhatsApp conversation for accepted consultations.',
        }


class DoctorAvailabilityForm(forms.ModelForm):
    """
    Simple form for doctors to change their availability status.
    """
    
    class Meta:
        model = DoctorProfile
        fields = ['availability_status']
        
        widgets = {
            'availability_status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        
        labels = {
            'availability_status': 'Current Status',
        }