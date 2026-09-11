from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class ClientRegistrationForm(UserCreationForm):
    """
    Registration form for new clients.
    Collects email and password, and automatically sets the role to CLIENT.
    """
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        }),
        help_text='Required. Enter a valid email address.',
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
        }),
        help_text='Your password must be at least 8 characters and not too common.',
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        }),
        help_text='Enter the same password as before, for verification.',
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
    
    def save(self, commit=True):
        """
        Save the new user with the CLIENT role.
        """
        user = super().save(commit=False)
        user.role = CustomUser.Role.CLIENT
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form that uses email instead of username.
    """
    
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        }),
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        }),
    )