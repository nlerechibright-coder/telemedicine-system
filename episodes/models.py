from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from medical_data.models import Symptom, Condition
from doctors.models import Specialty


class HealthEpisode(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        MATCHING = 'MATCHING', 'Matching Symptoms'
        AWAITING_DOCTOR = 'AWAITING_DOCTOR', 'Awaiting Doctor'
        IN_CONSULTATION = 'IN_CONSULTATION', 'In Consultation'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        EMERGENCY = 'EMERGENCY', 'Emergency'
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='health_episodes',
        limit_choices_to={'role': 'CLIENT'},
        verbose_name='Client'
    )
    
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Episode Title',
        help_text='A brief description of this health issue'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Status'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    video_started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Video Consultation Started At'
    )
    
    class Meta:
        verbose_name = 'Health Episode'
        verbose_name_plural = 'Health Episodes'
        ordering = ['-created_at']
    
    def __str__(self):
        title_display = self.title if self.title else f"Episode #{self.id}"
        return f"{title_display} - {self.client.email} ({self.get_status_display()})"
    
    def clean(self):
        if self.client_id and not self.client.is_client:
            raise ValidationError('The selected user must have the CLIENT role.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class EpisodeSymptom(models.Model):
    class Severity(models.TextChoices):
        MILD = 'MILD', 'Mild'
        MODERATE = 'MODERATE', 'Moderate'
        SEVERE = 'SEVERE', 'Severe'
    
    episode = models.ForeignKey(
        HealthEpisode,
        on_delete=models.CASCADE,
        related_name='episode_symptoms',
        verbose_name='Health Episode'
    )
    
    symptom = models.ForeignKey(
        Symptom,
        on_delete=models.CASCADE,
        related_name='episode_occurrences',
        verbose_name='Symptom'
    )
    
    reported_severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.MODERATE,
        verbose_name='Reported Severity'
    )
    
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Added At')
    
    class Meta:
        verbose_name = 'Episode Symptom'
        verbose_name_plural = 'Episode Symptoms'
        ordering = ['added_at']
        constraints = [
            models.UniqueConstraint(
                fields=['episode', 'symptom'],
                name='unique_episode_symptom'
            )
        ]
    
    def __str__(self):
        return f"{self.episode} - {self.symptom.name} ({self.get_reported_severity_display()})"


class EpisodeConditionMatch(models.Model):
    episode = models.ForeignKey(
        HealthEpisode,
        on_delete=models.CASCADE,
        related_name='condition_matches',
        verbose_name='Health Episode'
    )
    
    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name='episode_matches',
        verbose_name='Condition'
    )
    
    match_score = models.PositiveIntegerField(
        default=0,
        verbose_name='Match Score',
        help_text='Total weight of matched symptoms for this condition'
    )
    
    coverage_percentage = models.FloatField(
        default=0.0,
        verbose_name='Coverage Percentage',
        help_text='Percentage of the condition total symptoms that were matched'
    )
    
    matched_at = models.DateTimeField(auto_now_add=True, verbose_name='Matched At')
    
    class Meta:
        verbose_name = 'Episode Condition Match'
        verbose_name_plural = 'Episode Condition Matches'
        ordering = ['-match_score', '-coverage_percentage']
        constraints = [
            models.UniqueConstraint(
                fields=['episode', 'condition'],
                name='unique_episode_condition_match'
            )
        ]
    
    def __str__(self):
        return f"{self.episode} - {self.condition.name} (Score: {self.match_score}, Coverage: {self.coverage_percentage}%)"


class DoctorRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    episode = models.ForeignKey(
        HealthEpisode,
        on_delete=models.CASCADE,
        related_name='doctor_requests',
        verbose_name='Health Episode'
    )
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_requests_made',
        limit_choices_to={'role': 'CLIENT'},
        verbose_name='Client'
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_requests_received',
        limit_choices_to={'role': 'DOCTOR'},
        verbose_name='Requested Doctor',
        help_text='Leave blank for specialty-based routing'
    )
    
    requested_specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_requests',
        verbose_name='Requested Specialty',
        help_text='Optional: specify a specialty for routing'
    )
    
    reason = models.TextField(
        verbose_name='Reason for Request',
        help_text='Explain why you need a doctor consultation for this episode'
    )
    
    doctor_notes = models.TextField(
        blank=True,
        verbose_name='Doctor Notes',
        help_text='Notes from the doctor (visible to client)'
    )
    
    rejection_reason = models.TextField(
        blank=True,
        verbose_name='Rejection Reason',
        help_text='Reason for rejecting the request (if applicable)'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Requested At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name='Responded At')
    
    class Meta:
        verbose_name = 'Doctor Request'
        verbose_name_plural = 'Doctor Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        doctor_display = self.doctor.email if self.doctor else f"Specialty: {self.requested_specialty.name if self.requested_specialty else 'Any'}"
        return f"Request #{self.id} - {self.client.email} → {doctor_display} ({self.get_status_display()})"
    
    def clean(self):
        if self.episode_id and self.client_id:
            if self.episode.client_id != self.client_id:
                raise ValidationError('The client must match the episode owner.')
        
        if not self.doctor_id and not self.requested_specialty_id:
            raise ValidationError('Please specify either a doctor or a specialty for the request.')
        
        if self.doctor_id:
            if hasattr(self.doctor, 'doctor_profile'):
                if not self.doctor.doctor_profile.is_verified:
                    raise ValidationError('The selected doctor is not yet verified by an administrator.')
            else:
                raise ValidationError('The selected user does not have a doctor profile.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            old_status = DoctorRequest.objects.values_list('status', flat=True).filter(pk=self.pk).first()
            if old_status == self.Status.PENDING and self.status != self.Status.PENDING:
                self.responded_at = timezone.now()

        with transaction.atomic():
            super().save(*args, **kwargs)

            if self.status == self.Status.ACCEPTED:
                self.episode.status = HealthEpisode.Status.IN_CONSULTATION
                self.episode.save(update_fields=['status', 'updated_at'])

                from messaging.models import ChatRoom
                ChatRoom.objects.get_or_create(episode=self.episode)
            elif self.status == self.Status.REJECTED:
                pending_count = DoctorRequest.objects.filter(
                    episode=self.episode,
                    status=self.Status.PENDING
                ).exclude(pk=self.pk).count()
                if pending_count == 0:
                    self.episode.status = HealthEpisode.Status.AWAITING_DOCTOR
                    self.episode.save(update_fields=['status', 'updated_at'])
            elif self.status == self.Status.PENDING:
                self.episode.status = HealthEpisode.Status.AWAITING_DOCTOR
                self.episode.save(update_fields=['status', 'updated_at'])