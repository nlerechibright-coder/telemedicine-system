from django import forms
from .models import Category


class ArticleSearchForm(forms.Form):
    """
    Form for clients to search and filter health articles.
    """
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...',
        }),
        label='Search',
    )
    
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Category',
    )