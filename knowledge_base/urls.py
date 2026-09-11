from django.urls import path
from . import views

# All URLs for the knowledge_base app will start with 'knowledge/'
# For example: /knowledge/articles/, /knowledge/articles/how-to-manage-stress/

app_name = 'knowledge_base'

urlpatterns = [
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<slug:slug>/', views.article_detail_view, name='article_detail'),
]