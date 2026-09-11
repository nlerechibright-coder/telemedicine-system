from django import forms
from .models import ClientProfile


class ClientProfileForm(forms.ModelForm):
    """
    Form for clients to create or update their personal and health profile.
    """
    
    class Meta:
        model = ClientProfile
        fields = [
            'full_name', 'date_of_birth', 'gender', 'phone_number', 'whatsapp_number', 'address',
            'blood_type', 'chronic_conditions', 'allergies', 'current_medications'
        ]
        
        # Customize the appearance of each field using HTML attributes
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., John Doe'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'  # This gives a nice calendar picker in modern browsers
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., +1 234 567 8900'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 08029011944 or +2348029011944'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Your residential address'
            }),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'chronic_conditions': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g., Asthma, Hypertension (leave blank if none)'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g., Penicillin, Peanuts (leave blank if none)'
            }),
            'current_medications': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g., Lisinopril 10mg daily (leave blank if none)'
            }),
        }
        
        # Custom labels to make the form more user-friendly
        labels = {
            'full_name': 'Full Name',
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'phone_number': 'Phone Number',
            'whatsapp_number': 'WhatsApp Number',
            'address': 'Address',
            'blood_type': 'Blood Type',
            'chronic_conditions': 'Chronic Conditions',
            'allergies': 'Allergies',
            'current_medications': 'Current Medications',
        }