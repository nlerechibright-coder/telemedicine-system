from django import forms
from django.core.exceptions import ValidationError
from .models import DoctorRequest, HealthEpisode
from doctors.models import DoctorProfile, Specialty


class DoctorRequestForm(forms.ModelForm):
    """
    Form for clients to request a doctor for a specific health episode.
    Supports both direct doctor selection and specialty-based routing.
    """
    
    class Meta:
        model = DoctorRequest
        fields = ['doctor', 'requested_specialty', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please describe why you need a doctor consultation for this episode...',
                'class': 'form-control'
            }),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'requested_specialty': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'doctor': 'Select Doctor (Optional)',
            'requested_specialty': 'Or Select Specialty (Optional)',
            'reason': 'Reason for Consultation',
        }
        help_texts = {
            'doctor': 'Choose a specific doctor, or leave blank to request by specialty.',
            'requested_specialty': 'Choose a specialty if you don\'t have a specific doctor in mind.',
            'reason': 'Explain your symptoms and why you need professional medical advice.',
        }
    
    def __init__(self, *args, episode=None, client=None, **kwargs):
        """
        Initialize the form with episode and client context.
        Filter doctors to only show verified ones.
        """
        super().__init__(*args, **kwargs)
        
        self.episode = episode
        self.client = client
        
        # Filter doctors to only show verified ones
        verified_doctors = DoctorProfile.objects.filter(is_verified=True).values_list('user_id', flat=True)
        self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(id__in=verified_doctors)
        
        # Make both doctor and specialty optional (but at least one must be provided)
        self.fields['doctor'].required = False
        self.fields['requested_specialty'].required = False
    
    def clean(self):
        """
        Validate that at least one routing method is specified (doctor OR specialty).
        """
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        specialty = cleaned_data.get('requested_specialty')
        
        if not doctor and not specialty:
            raise ValidationError(
                'Please select either a specific doctor or a specialty for your request.'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the form and automatically set the episode and client.
        """
        instance = super().save(commit=False)
        
        if self.episode:
            instance.episode = self.episode
        if self.client:
            instance.client = self.client
        
        if commit:
            instance.save()
        
        return instance


class DoctorResponseForm(forms.ModelForm):
    """
    Form for doctors to accept or reject a doctor request.
    """
    
    class Meta:
        model = DoctorRequest
        fields = ['status', 'doctor_notes', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'doctor_notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add any notes for the client...',
                'class': 'form-control'
            }),
            'rejection_reason': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Please explain why you are rejecting this request...',
                'class': 'form-control'
            }),
        }
        labels = {
            'status': 'Decision',
            'doctor_notes': 'Notes for Client (Optional)',
            'rejection_reason': 'Rejection Reason (Required if Rejecting)',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Limit status choices to only ACCEPTED or REJECTED.
        """
        super().__init__(*args, **kwargs)
        
        # Only allow ACCEPTED or REJECTED status
        self.fields['status'].choices = [
            (DoctorRequest.Status.ACCEPTED, 'Accept Request'),
            (DoctorRequest.Status.REJECTED, 'Reject Request'),
        ]
        
        # Initially hide rejection reason (will be shown via JavaScript if REJECTED is selected)
        self.fields['rejection_reason'].widget.attrs['style'] = 'display: none;'
    
    def clean(self):
        """
        Validate that rejection_reason is provided if status is REJECTED.
        """
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')
        
        if status == DoctorRequest.Status.REJECTED and not rejection_reason:
            raise ValidationError(
                'Please provide a reason for rejecting this request.'
            )
        
        return cleaned_data