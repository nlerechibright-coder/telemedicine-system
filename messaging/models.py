from django.db import models
from django.conf import settings
from episodes.models import HealthEpisode


class ChatRoom(models.Model):
    """
    Represents a chat room for a specific health episode.
    One chat room per health episode (OneToOne relationship).
    Only the episode's client and assigned doctor can access this room.
    """
    
    episode = models.OneToOneField(
        HealthEpisode,
        on_delete=models.CASCADE,
        related_name='chat_room',
        verbose_name='Health Episode',
        help_text='The health episode this chat room belongs to'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    
    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat Room for Episode #{self.episode_id} - {self.episode.title}"
    
    def get_participants(self):
        """
        Returns a list of users who can access this chat room.
        Includes the episode's client and the assigned doctor.
        """
        from episodes.models import DoctorRequest
        
        participants = [self.episode.client]
        
        # Find the assigned doctor (accepted request)
        accepted_request = DoctorRequest.objects.filter(
            episode=self.episode,
            status=DoctorRequest.Status.ACCEPTED
        ).first()
        
        if accepted_request and accepted_request.doctor:
            participants.append(accepted_request.doctor)
        
        return participants


class ChatMessage(models.Model):
    """
    Represents a single message within a chat room.
    Messages are sent by either the client or the assigned doctor.
    """
    
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Chat Room'
    )
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_chat_messages',
        verbose_name='Sender'
    )
    
    content = models.TextField(
        verbose_name='Message Content',
        help_text='The text content of the message'
    )
    
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sent At'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Is Read',
        help_text='Whether the recipient has read this message'
    )
    
    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['sent_at']  # Oldest first
        indexes = [
            models.Index(fields=['room', 'sent_at']),  # Optimize message fetching
        ]
    
    def __str__(self):
        sender_email = self.sender.email if self.sender else 'Unknown'
        return f"Message from {sender_email} at {self.sent_at}"
    
    def mark_as_read(self):
        """Mark this message as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])