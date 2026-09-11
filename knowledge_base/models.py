from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """
    Represents a category for health articles (e.g., General Health, Nutrition, Mental Health).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    description = models.TextField(blank=True, verbose_name='Description')
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Represents a health or medical knowledge article.
    """
    title = models.CharField(max_length=255, verbose_name='Article Title')
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name='URL Slug')
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='articles',
        verbose_name='Category'
    )
    
    content = models.TextField(verbose_name='Article Content')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_articles',
        verbose_name='Author'
    )
    
    # Publication status
    is_published = models.BooleanField(default=False, verbose_name='Published')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Published At')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Automatically generate a slug from the title if it's not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)