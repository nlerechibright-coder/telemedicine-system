from django import forms
from django.utils import timezone
from .models import Consultation, Message


class ConsultationRequestForm(forms.ModelForm):
    """
    Form for clients to request a consultation with a doctor.
    Only allows selecting verified doctors.
    """
    
    class Meta:
        model = Consultation
        fields = ['doctor', 'reason', 'scheduled_at']
        
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please describe your symptoms or the reason for your consultation in detail...',
            }),
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
        }
        
        labels = {
            'doctor': 'Select Doctor',
            'reason': 'Reason for Consultation',
            'scheduled_at': 'Preferred Date/Time (Optional)',
        }
        
        help_texts = {
            'doctor': 'Only verified doctors are available for consultation.',
            'reason': 'Please provide as much detail as possible to help the doctor understand your needs.',
            'scheduled_at': 'Leave blank if you don\'t have a specific time preference.',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Customize the form to only show verified doctors.
        """
        super().__init__(*args, **kwargs)
        
        # Filter doctors to only show those with verified profiles
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get all doctors with verified profiles
        verified_doctor_ids = User.objects.filter(
            role='DOCTOR',
            doctor_profile__is_verified=True
        ).values_list('id', flat=True)
        
        self.fields['doctor'].queryset = User.objects.filter(id__in=verified_doctor_ids)
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.email}"


class ConsultationResponseForm(forms.ModelForm):
    """
    Form for doctors to accept or reject a consultation request.
    """
    
    class Meta:
        model = Consultation
        fields = ['status', 'doctor_notes', 'rejection_reason']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'doctor_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add any notes about this consultation...',
            }),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Please explain why you are rejecting this consultation...',
            }),
        }
        
        labels = {
            'status': 'Decision',
            'doctor_notes': 'Consultation Notes',
            'rejection_reason': 'Rejection Reason',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Customize the form to only show ACCEPTED and REJECTED options.
        """
        super().__init__(*args, **kwargs)
        
        # Only allow ACCEPTED or REJECTED status
        self.fields['status'].choices = [
            (Consultation.Status.ACCEPTED, 'Accept'),
            (Consultation.Status.REJECTED, 'Reject'),
        ]


class MessageForm(forms.ModelForm):
    """
    Form for sending messages within a consultation.
    """
    
    class Meta:
        model = Message
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message here...',
            }),
        }
        
        labels = {
            'content': '',
        }


class DoctorNotesForm(forms.ModelForm):
    """
    Simple form for doctors to add or update notes on a consultation.
    """
    
    class Meta:
        model = Consultation
        fields = ['doctor_notes']
        
        widgets = {
            'doctor_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add consultation notes...',
            }),
        }
        
        labels = {
            'doctor_notes': 'Consultation Notes',
        }