from django.urls import path
from . import views

# All URLs for the doctors app will start with 'doctors/'
# For example: /doctors/dashboard/, /doctors/profile/view/, /doctors/profile/edit/

app_name = 'doctors'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard_view, name='dashboard'),
    path('profile/view/', views.view_profile_view, name='view_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('availability/update/', views.update_availability_view, name='update_availability'),
]