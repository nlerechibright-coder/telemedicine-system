from django.urls import path
from . import views

# All URLs for the clients app will start with 'clients/'
# For example: /clients/profile/complete/, /clients/profile/view/, /clients/profile/edit/

app_name = 'clients'

urlpatterns = [
    path('profile/complete/', views.complete_profile_view, name='complete_profile'),
    path('profile/view/', views.view_profile_view, name='view_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]