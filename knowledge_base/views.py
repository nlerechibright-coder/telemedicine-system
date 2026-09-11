from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from .forms import ArticleSearchForm


def article_list_view(request):
    """
    Display a list of all published health articles.
    Supports searching by keyword and filtering by category.
    """
    
    # Start with all published articles
    articles = Article.objects.filter(is_published=True)
    
    # Initialize the search form with GET data (for bookmarkable search URLs)
    form = ArticleSearchForm(request.GET)
    
    if form.is_valid():
        # Filter by search keyword (searches in title and content)
        search_query = form.cleaned_data.get('search')
        if search_query:
            articles = articles.filter(
                models.Q(title__icontains=search_query) | 
                models.Q(content__icontains=search_query)
            )
        
        # Filter by category
        category = form.cleaned_data.get('category')
        if category:
            articles = articles.filter(category=category)
    
    # Get all categories for the sidebar (optional enhancement)
    categories = Category.objects.all()
    
    return render(request, 'knowledge_base/article_list.html', {
        'articles': articles,
        'form': form,
        'categories': categories,
    })


def article_detail_view(request, slug):
    """
    Display a single health article in detail.
    Only shows published articles.
    """
    
    # Get the article by slug, but only if it's published
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    return render(request, 'knowledge_base/article_detail.html', {
        'article': article,
    })