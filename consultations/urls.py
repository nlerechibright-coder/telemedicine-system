from django.urls import path
from . import views

# All URLs for the consultations app will start with 'consultations/'

app_name = 'consultations'

urlpatterns = [
    # Client URLs
    path('request/', views.request_consultation_view, name='request_consultation'),
    path('my-consultations/', views.client_consultation_list_view, name='client_consultation_list'),
    path('my-consultations/<int:consultation_id>/', views.client_consultation_detail_view, name='client_consultation_detail'),
    
    # Doctor URLs
    path('doctor/pending/', views.doctor_pending_requests_view, name='doctor_pending_requests'),
    path('doctor/my-consultations/', views.doctor_consultation_list_view, name='doctor_consultation_list'),
    path('doctor/my-consultations/<int:consultation_id>/', views.doctor_consultation_detail_view, name='doctor_consultation_detail'),
]