from django.contrib import admin
from .models import HealthEpisode, EpisodeSymptom, EpisodeConditionMatch, DoctorRequest


class EpisodeSymptomInline(admin.TabularInline):
    """
    Inline display of symptoms within the HealthEpisode admin view.
    Allows adding/editing symptoms directly on the Episode page.
    """
    model = EpisodeSymptom
    extra = 1  # Show one empty row for adding new symptoms
    autocomplete_fields = ('symptom',)
    fields = ('symptom', 'reported_severity', 'added_at')
    readonly_fields = ('added_at',)
    
    verbose_name = 'Selected Symptom'
    verbose_name_plural = 'Selected Symptoms'


class EpisodeConditionMatchInline(admin.TabularInline):
    """
    Inline display of condition matches within the HealthEpisode admin view.
    Shows the matching engine results (read-only).
    """
    model = EpisodeConditionMatch
    extra = 0  # No empty rows - matches are created by the engine
    autocomplete_fields = ('condition',)
    fields = ('condition', 'match_score', 'coverage_percentage', 'matched_at')
    readonly_fields = ('condition', 'match_score', 'coverage_percentage', 'matched_at')
    
    verbose_name = 'Matched Condition'
    verbose_name_plural = 'Matched Conditions'
    
    def has_add_permission(self, request, obj=None):
        return False  # Matches are created by the engine, not manually
    
    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion for cleanup/debugging


class DoctorRequestInline(admin.TabularInline):
    """
    Inline display of doctor requests within the HealthEpisode admin view.
    Shows the full request history for this episode (read-only).
    """
    model = DoctorRequest
    extra = 0
    fields = ('client', 'doctor_or_specialty', 'status', 'created_at', 'responded_at')
    readonly_fields = ('client', 'doctor_or_specialty', 'status', 'created_at', 'responded_at')
    
    verbose_name = 'Doctor Request'
    verbose_name_plural = 'Doctor Requests'
    
    def has_add_permission(self, request, obj=None):
        return False  # Requests are created via the client UI
    
    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion for cleanup
    
    @admin.display(description='Doctor / Specialty')
    def doctor_or_specialty(self, obj):
        if obj.doctor:
            return f"Dr. {obj.doctor.email}"
        elif obj.requested_specialty:
            return f"Specialty: {obj.requested_specialty.name}"
        return "—"


@admin.register(HealthEpisode)
class HealthEpisodeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing health episodes.
    """
    
    # What to display in the list view
    list_display = ('id', 'client_email', 'title', 'status', 'symptom_count', 'match_count', 'request_count', 'created_at')
    
    # Filters in the right sidebar
    list_filter = ('status', 'created_at')
    
    # Search bar fields
    search_fields = ('title', 'client__email')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view
    fieldsets = (
        ('Episode Information', {
            'fields': ('client', 'title', 'status'),
            'description': 'Basic details about this health episode.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # Inline symptoms, condition matches, and doctor requests
    inlines = [EpisodeSymptomInline, EpisodeConditionMatchInline, DoctorRequestInline]
    
    # Custom method to display client email
    @admin.display(description='Client', ordering='client__email')
    def client_email(self, obj):
        return obj.client.email
    
    # Custom method to show symptom count
    @admin.display(description='# Symptoms')
    def symptom_count(self, obj):
        return obj.episode_symptoms.count()
    
    # Custom method to show match count
    @admin.display(description='# Matches')
    def match_count(self, obj):
        return obj.condition_matches.count()
    
    # Custom method to show request count
    @admin.display(description='# Requests')
    def request_count(self, obj):
        return obj.doctor_requests.count()


@admin.register(EpisodeSymptom)
class EpisodeSymptomAdmin(admin.ModelAdmin):
    """
    Standalone admin for episode symptoms (useful for debugging/bulk operations).
    Most management should happen via the HealthEpisode inline.
    """
    
    list_display = ('id', 'episode_title', 'symptom_name', 'reported_severity', 'is_red_flag', 'added_at')
    list_filter = ('reported_severity', 'symptom__is_red_flag')
    search_fields = ('episode__title', 'symptom__name', 'episode__client__email')
    ordering = ('-added_at',)
    autocomplete_fields = ('episode', 'symptom')
    
    @admin.display(description='Episode', ordering='episode__title')
    def episode_title(self, obj):
        return str(obj.episode)
    
    @admin.display(description='Symptom', ordering='symptom__name')
    def symptom_name(self, obj):
        return obj.symptom.name
    
    @admin.display(description='Red Flag?', boolean=True)
    def is_red_flag(self, obj):
        return obj.symptom.is_red_flag


@admin.register(EpisodeConditionMatch)
class EpisodeConditionMatchAdmin(admin.ModelAdmin):
    """
    Standalone admin for condition matches (useful for debugging).
    Most management should happen via the HealthEpisode inline.
    """
    
    list_display = ('id', 'episode_title', 'condition_name', 'match_score', 'coverage_percentage', 'matched_at')
    list_filter = ('condition',)
    search_fields = ('episode__title', 'condition__name', 'episode__client__email')
    ordering = ('-match_score',)
    autocomplete_fields = ('episode', 'condition')
    
    # Make most fields read-only since matches are engine-generated
    readonly_fields = ('episode', 'condition', 'match_score', 'coverage_percentage', 'matched_at')
    
    @admin.display(description='Episode', ordering='episode__title')
    def episode_title(self, obj):
        return str(obj.episode)
    
    @admin.display(description='Condition', ordering='condition__name')
    def condition_name(self, obj):
        return obj.condition.name


@admin.register(DoctorRequest)
class DoctorRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for managing doctor requests.
    """
    
    # What to display in the list view
    list_display = ('id', 'client_email', 'doctor_or_specialty', 'episode_title', 'status', 'created_at', 'responded_at')
    
    # Filters in the right sidebar
    list_filter = ('status', 'requested_specialty', 'created_at')
    
    # Search bar fields
    search_fields = ('client__email', 'doctor__email', 'reason', 'episode__title')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view
    fieldsets = (
        ('Episode & Participants', {
            'fields': ('episode', 'client', 'doctor'),
            'description': 'Link this request to a health episode and identify the participants.'
        }),
        ('Routing Preferences', {
            'fields': ('requested_specialty',),
            'description': 'Optional specialty preference for routing.'
        }),
        ('Request Details', {
            'fields': ('reason', 'doctor_notes', 'rejection_reason'),
            'description': 'The reason for the request and any notes from the doctor.'
        }),
        ('Status', {
            'fields': ('status', 'responded_at'),
            'description': 'Current status of the request.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'responded_at')
    autocomplete_fields = ('episode', 'client', 'doctor', 'requested_specialty')
    
    # Custom method to display client email
    @admin.display(description='Client', ordering='client__email')
    def client_email(self, obj):
        return obj.client.email
    
    # Custom method to display doctor or specialty
    @admin.display(description='Doctor / Specialty', ordering='doctor__email')
    def doctor_or_specialty(self, obj):
        if obj.doctor:
            return f"Dr. {obj.doctor.email}"
        elif obj.requested_specialty:
            return f"Specialty: {obj.requested_specialty.name}"
        return "—"
    
    # Custom method to display episode title
    @admin.display(description='Episode', ordering='episode__title')
    def episode_title(self, obj):
        return str(obj.episode)