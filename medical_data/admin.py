from django.contrib import admin
from .models import Symptom, Condition, ConditionSymptom


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    """
    Admin interface for managing medical symptoms.
    """
    
    # What to display in the list view (table columns)
    list_display = ('name', 'is_red_flag', 'description_preview', 'emergency_message_preview')
    
    # Filters in the right sidebar
    list_filter = ('is_red_flag',)
    
    # Search bar fields
    search_fields = ('name', 'description')
    
    # Default ordering
    ordering = ('name',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description'),
            'description': 'The basic details of this symptom.'
        }),
        ('Emergency / Red Flag Settings', {
            'fields': ('is_red_flag', 'emergency_message'),
            'description': 'If this symptom is a red flag, provide a clear emergency warning message. '
                           'This message will be shown prominently to users who select this symptom.'
        }),
    )
    
    # Custom method to show a preview of the description
    @admin.display(description='Description Preview')
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:80] + ('...' if len(obj.description) > 80 else '')
        return '—'
    
    # Custom method to show a preview of the emergency message
    @admin.display(description='Emergency Message Preview')
    def emergency_message_preview(self, obj):
        if obj.is_red_flag:
            if obj.emergency_message:
                return obj.emergency_message[:80] + ('...' if len(obj.emergency_message) > 80 else '')
            return '⚠️ No message set!'
        return '—'


class ConditionSymptomInline(admin.TabularInline):
    """
    Inline display of symptom rules within the Condition admin view.
    Allows adding/editing symptom rules directly on the Condition page.
    """
    model = ConditionSymptom
    extra = 1  # Show one empty row for adding new rules
    autocomplete_fields = ('symptom',)  # Makes symptom selection searchable
    
    # Fieldsets for inline (compact view)
    fields = ('symptom', 'weight', 'is_core', 'notes')
    
    verbose_name = 'Symptom Rule'
    verbose_name_plural = 'Symptom Rules'


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing medical conditions.
    """
    
    # What to display in the list view
    list_display = ('name', 'description_preview', 'symptom_count', 'article_count')
    
    # Search bar fields
    search_fields = ('name', 'description')
    
    # Default ordering
    ordering = ('name',)
    
    # Fieldsets for the edit view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description'),
            'description': 'The basic details of this medical condition.'
        }),
        ('Related Knowledge Base Articles', {
            'fields': ('articles',),
            'description': 'Link existing Knowledge Base articles that provide information about this condition. '
                           'These articles will be shown to users when this condition is identified by the matching engine.'
        }),
    )
    
    # Makes the M2M articles field easier to use (side-by-side selection)
    filter_horizontal = ('articles',)
    
    # Inline symptom rules (so admins can add rules directly on the Condition page)
    inlines = [ConditionSymptomInline]
    
    # Custom method to show a preview of the description
    @admin.display(description='Description Preview')
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:80] + ('...' if len(obj.description) > 80 else '')
        return '—'
    
    # Custom method to show how many symptom rules this condition has
    @admin.display(description='# of Symptoms', ordering='symptom_rules__count')
    def symptom_count(self, obj):
        return obj.symptom_rules.count()
    
    # Custom method to show how many articles are linked
    @admin.display(description='# of Articles')
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(ConditionSymptom)
class ConditionSymptomAdmin(admin.ModelAdmin):
    """
    Admin interface for managing condition-symptom rules directly.
    (Note: Most rule management should happen via the Condition inline above,
    but this view is useful for bulk operations and debugging.)
    """
    
    # What to display in the list view
    list_display = ('condition', 'symptom', 'weight', 'is_core', 'notes_preview')
    
    # Filters in the right sidebar
    list_filter = ('condition', 'is_core', 'weight')
    
    # Search bar fields
    search_fields = ('condition__name', 'symptom__name', 'notes')
    
    # Default ordering
    ordering = ('condition', '-weight', 'symptom')
    
    # Makes selection searchable
    autocomplete_fields = ('condition', 'symptom')
    
    # Custom method to show a preview of the notes
    @admin.display(description='Notes Preview')
    def notes_preview(self, obj):
        if obj.notes:
            return obj.notes[:60] + ('...' if len(obj.notes) > 60 else '')
        return '—'