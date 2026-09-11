from django.db import models
from django.conf import settings


class Specialty(models.Model):
    """
    Represents a medical specialty (e.g., General Practice, Cardiology, Pediatrics).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Specialty Name')
    description = models.TextField(blank=True, verbose_name='Description')
    
    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    """
    Extended profile information for doctors.
    Contains professional details and availability status.
    """
    
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        BUSY = 'BUSY', 'Busy'
        AWAY = 'AWAY', 'Away'
        OFFLINE = 'OFFLINE', 'Offline'
    
    # Link to the User model (one-to-one relationship)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='User Account'
    )
    
    # Professional Information
    specialty = models.ForeignKey(
        Specialty, 
        on_delete=models.PROTECT, 
        related_name='doctors',
        verbose_name='Specialty'
    )
    license_number = models.CharField(max_length=100, unique=True, verbose_name='Medical License Number')
    qualifications = models.TextField(verbose_name='Qualifications', help_text='e.g., MD, PhD, Board Certified in...')
    bio = models.TextField(blank=True, verbose_name='Professional Bio')
    consultation_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Consultation Fee'
    )
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='WhatsApp Number',
        help_text='Optional WhatsApp contact number, including country code or local format.'
    )
    
    # Availability and Status
    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.OFFLINE,
        verbose_name='Availability Status'
    )
    is_verified = models.BooleanField(
        default=False, 
        verbose_name='Verified by Admin',
        help_text='Only verified doctors can accept consultations.'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.user.email} ({self.specialty.name})"
    
    @property
    def is_available(self):
        """Check if the doctor is currently available for new requests."""
        return self.availability_status == self.AvailabilityStatus.AVAILABLE