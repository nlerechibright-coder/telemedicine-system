from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing article categories.
    """
    
    # What to display in the list view (table columns)
    list_display = ('name', 'description')
    
    # Search bar fields
    search_fields = ('name', 'description')
    
    # Default ordering
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for managing health articles.
    """
    
    # What to display in the list view (table columns)
    list_display = ('title', 'category', 'author_email', 'is_published', 'published_at', 'created_at')
    
    # Filters in the right sidebar
    list_filter = ('category', 'is_published', 'published_at', 'created_at')
    
    # Search bar fields
    search_fields = ('title', 'content', 'category__name', 'author__email')
    
    # Default ordering
    ordering = ('-created_at',)
    
    # Fieldsets for the edit view (organizes the form into sections)
    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'category', 'content')
        }),
        ('Author & Publication', {
            'fields': ('author', 'is_published', 'published_at'),
            'description': 'Control article visibility and publication'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Make timestamp fields read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Pre-populate slug from title
    prepopulated_fields = {'slug': ('title',)}
    
    # Custom method to display author email in list view
    @admin.display(description='Author', ordering='author__email')
    def author_email(self, obj):
        if obj.author:
            return obj.author.email
        return '—'