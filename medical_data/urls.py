from django.urls import path
from . import views

app_name = 'medical_data'

urlpatterns = [
    path('symptoms/', views.symptom_select_view, name='symptom_select'),
    path('symptoms/match/', views.symptom_match_view, name='symptom_match'),
]