from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model


class Consultation(models.Model):
    """
    Represents a consultation request from a client to a doctor.
    Tracks the entire lifecycle from request to completion.
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    # Participants
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_consultations',
        limit_choices_to={'role': 'CLIENT'},
        verbose_name='Client'
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_consultations',
        limit_choices_to={'role': 'DOCTOR'},
        verbose_name='Doctor'
    )
    
    # Consultation Details
    reason = models.TextField(
        verbose_name='Reason for Consultation',
        help_text='Please describe your symptoms or the reason for your consultation.'
    )
    
    doctor_notes = models.TextField(
        blank=True,
        verbose_name='Doctor Notes',
        help_text='Notes from the doctor (visible only to the doctor and client).'
    )
    
    # Status and Scheduling
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Scheduled Date/Time',
        help_text='When the consultation is scheduled to take place.'
    )
    
    # Rejection reason (if rejected)
    rejection_reason = models.TextField(
        blank=True,
        verbose_name='Rejection Reason',
        help_text='Reason for rejecting the consultation (if applicable).'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Requested At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Consultation #{self.id} - {self.client.email if self.client_id else 'Unknown'} with Dr. {self.doctor.email if self.doctor_id else 'Unknown'}"
    
    def clean(self):
        """
        Custom validation to ensure the client and doctor are different users
        and that the doctor has a verified profile.
        """
        # Use _id fields to avoid RelatedObjectDoesNotExist errors during form validation
        client_id = getattr(self, 'client_id', None)
        doctor_id = getattr(self, 'doctor_id', None)
        
        if client_id and doctor_id and client_id == doctor_id:
            raise ValidationError('The client and doctor cannot be the same person.')
        
        if doctor_id:
            User = get_user_model()
            try:
                doctor = User.objects.get(id=doctor_id)
                if hasattr(doctor, 'doctor_profile'):
                    if not doctor.doctor_profile.is_verified:
                        raise ValidationError('The selected doctor is not yet verified by an administrator.')
                else:
                    raise ValidationError('The selected user does not have a doctor profile.')
            except User.DoesNotExist:
                pass  # Standard field validation will catch invalid IDs
    
    def save(self, *args, **kwargs):
        """
        Override save to call full_clean() for validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        """Check if the consultation is currently active (pending or accepted)."""
        return self.status in [self.Status.PENDING, self.Status.ACCEPTED]
    
    @property
    def can_be_messaged(self):
        """Check if messaging is allowed for this consultation."""
        return self.status == self.Status.ACCEPTED


class Message(models.Model):
    """
    Represents a message within a consultation.
    Only the client and doctor involved in the consultation can send/read messages.
    """
    
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Consultation'
    )
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender'
    )
    
    content = models.TextField(verbose_name='Message Content')
    
    # Read status (for future enhancement)
    is_read = models.BooleanField(default=False, verbose_name='Read')
    
    # Timestamp
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Sent At')
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message from {self.sender.email if self.sender_id else 'Unknown'} in Consultation #{self.consultation_id}"
    
    def clean(self):
        """
        Custom validation to ensure the sender is either the client or doctor
        in the consultation.
        """
        sender_id = getattr(self, 'sender_id', None)
        consultation_id = getattr(self, 'consultation_id', None)
        
        if sender_id and consultation_id:
            consultation = Consultation.objects.get(id=consultation_id)
            if sender_id not in [consultation.client_id, consultation.doctor_id]:
                raise ValidationError('Only the client or doctor in this consultation can send messages.')
    
    def save(self, *args, **kwargs):
        """
        Override save to call full_clean() for validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)