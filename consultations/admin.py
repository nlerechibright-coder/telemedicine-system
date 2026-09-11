from django.contrib import admin
from .models import Consultation, Message


class MessageInline(admin.TabularInline):
    """
    Inline display of messages within the consultation admin view.
    """
    model = Message
    extra = 0  # Don't show extra empty rows
    readonly_fields = ('sender', 'content', 'sent_at', 'is_read')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding messages directly from admin


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing consultations.
    """
    
    # What to display in the list view (table columns)
    list_display = ('id', 'client_email', 'doctor_email', 'status', 'scheduled_at', 'created_at')
    
    # Filters in the right sidebar
    list_filter = ('status', 'doctor', 'client', 'created_at', 'scheduled_at')
    
    # Search bar fields
    search_fields = ('client__email', 'doctor__email', 'reason', 'doctor_notes')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('Participants', {
            'fields': ('client', 'doctor'),
            'description': 'The client requesting the consultation and the assigned doctor'
        }),
        ('Consultation Details', {
            'fields': ('reason', 'doctor_notes', 'scheduled_at')
        }),
        ('Status & Outcome', {
            'fields': ('status', 'rejection_reason'),
            'description': 'Current status and any rejection details'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Make timestamp fields read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Inline messages (view only)
    inlines = [MessageInline]
    
    # Custom method to display client email in list view
    @admin.display(description='Client', ordering='client__email')
    def client_email(self, obj):
        return obj.client.email
    
    # Custom method to display doctor email in list view
    @admin.display(description='Doctor', ordering='doctor__email')
    def doctor_email(self, obj):
        return obj.doctor.email


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing messages (mostly for debugging/auditing).
    Messages are primarily managed through the Consultation inline.
    """
    
    # What to display in the list view
    list_display = ('id', 'consultation_id', 'sender_email', 'content_preview', 'is_read', 'sent_at')
    
    # Filters in the right sidebar
    list_filter = ('is_read', 'sender', 'consultation')
    
    # Search bar fields
    search_fields = ('content', 'sender__email', 'consultation__id')
    
    # Default ordering
    ordering = ('-sent_at',)
    
    # Make most fields read-only (messages shouldn't be edited after sending)
    readonly_fields = ('consultation', 'sender', 'content', 'sent_at', 'is_read')
    
    # Custom method to display sender email
    @admin.display(description='Sender', ordering='sender__email')
    def sender_email(self, obj):
        return obj.sender.email
    
    # Custom method to show a preview of the message content
    @admin.display(description='Message Preview')
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content