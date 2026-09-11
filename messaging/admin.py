from django.contrib import admin
from .models import ChatRoom, ChatMessage


class ChatMessageInline(admin.TabularInline):
    """
    Inline display of messages within the ChatRoom admin view.
    Allows viewing the message history directly on the ChatRoom page.
    """
    model = ChatMessage
    extra = 0  # No empty rows
    fields = ('sender', 'content', 'sent_at', 'is_read')
    readonly_fields = ('sender', 'content', 'sent_at', 'is_read')
    ordering = ('-sent_at',)  # Newest first
    
    verbose_name = 'Message'
    verbose_name_plural = 'Messages'
    
    def has_add_permission(self, request, obj=None):
        return False  # Messages should be created via the chat UI, not admin


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """
    Admin interface for managing chat rooms.
    """
    list_display = ('id', 'episode_title', 'created_at', 'message_count')
    search_fields = ('episode__title', 'episode__client__email')
    ordering = ('-created_at',)
    
    inlines = [ChatMessageInline]
    
    @admin.display(description='Episode', ordering='episode__title')
    def episode_title(self, obj):
        return str(obj.episode)
    
    @admin.display(description='# Messages')
    def message_count(self, obj):
        return obj.messages.count()


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Standalone admin for chat messages (useful for debugging).
    """
    list_display = ('id', 'room_episode', 'sender_email', 'content_preview', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('content', 'sender__email', 'room__episode__title')
    ordering = ('-sent_at',)
    autocomplete_fields = ('room', 'sender')
    
    @admin.display(description='Episode', ordering='room__episode__title')
    def room_episode(self, obj):
        return str(obj.room.episode)
    
    @admin.display(description='Sender', ordering='sender__email')
    def sender_email(self, obj):
        return obj.sender.email
    
    @admin.display(description='Content')
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    
    @admin.display(description='Read?', boolean=True)
    def is_read(self, obj):
        return obj.is_read