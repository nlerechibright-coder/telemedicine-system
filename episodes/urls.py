from django.urls import path
from . import views

app_name = 'episodes'

urlpatterns = [
    # Episode management
    path('', views.episode_list_view, name='episode_list'),
    path('<int:episode_id>/', views.episode_detail_view, name='episode_detail'),
    
    # Doctor requests
    path('<int:episode_id>/request-doctor/', views.request_doctor_view, name='request_doctor'),
    path('requests/', views.client_request_list_view, name='client_request_list'),
    path('requests/<int:request_id>/', views.client_request_detail_view, name='client_request_detail'),
    
    # Doctor views
    path('doctor/pending/', views.doctor_pending_requests_view, name='doctor_pending_requests'),
    path('doctor/requests/<int:request_id>/', views.doctor_request_detail_view, name='doctor_request_detail'),
]