from django.db import models
from django.conf import settings


class ClientProfile(models.Model):
    """
    Extended profile information for clients.
    Contains personal and health information that doctors will need during consultations.
    """
    
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'
    
    class BloodType(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'
        A_NEGATIVE = 'A-', 'A-'
        B_POSITIVE = 'B+', 'B+'
        B_NEGATIVE = 'B-', 'B-'
        AB_POSITIVE = 'AB+', 'AB+'
        AB_NEGATIVE = 'AB-', 'AB-'
        O_POSITIVE = 'O+', 'O+'
        O_NEGATIVE = 'O-', 'O-'
        UNKNOWN = 'UNKNOWN', 'Unknown'
    
    # Link to the User model (one-to-one relationship)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        verbose_name='User Account'
    )
    
    # Personal Information
    full_name = models.CharField(max_length=255, verbose_name='Full Name')
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        verbose_name='Gender'
    )
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='WhatsApp Number',
        help_text='Optional WhatsApp contact number, including country code or local format.'
    )
    address = models.TextField(blank=True, verbose_name='Address')
    
    # Health Information
    blood_type = models.CharField(
        max_length=10,  # Changed from 5 to 10 to fit 'UNKNOWN'
        choices=BloodType.choices,
        default=BloodType.UNKNOWN,
        verbose_name='Blood Type'
    )
    chronic_conditions = models.TextField(
        blank=True,
        verbose_name='Chronic Conditions',
        help_text='List any chronic conditions you have (e.g., diabetes, hypertension, asthma)'
    )
    allergies = models.TextField(
        blank=True,
        verbose_name='Allergies',
        help_text='List any allergies you have (e.g., penicillin, peanuts, latex)'
    )
    current_medications = models.TextField(
        blank=True,
        verbose_name='Current Medications',
        help_text='List any medications you are currently taking'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"
    
    def get_age(self):
        """Calculate and return the client's age based on date of birth."""
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age