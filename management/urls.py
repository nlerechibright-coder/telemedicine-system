from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/toggle/', views.user_toggle_active, name='user_toggle_active'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:doctor_id>/verify/', views.doctor_verify, name='doctor_verify'),
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('kb/', views.kb_list, name='kb_list'),
]