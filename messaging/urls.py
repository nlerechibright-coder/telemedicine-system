from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Chat list view (shows all active chats for the user)
    path('', views.chat_list_view, name='chat_list'),
    
    # Main chat view (HTML page for a specific episode)
    path('episode/<int:episode_id>/', views.chat_view, name='chat_view'),
    path('episode/<int:episode_id>/start-video/', views.start_video_view, name='start_video'),
    
    # API endpoints
    path('api/episode/<int:episode_id>/messages/', views.api_messages, name='api_messages'),
    path('api/episode/<int:episode_id>/mark-read/', views.api_mark_read, name='api_mark_read'),
]