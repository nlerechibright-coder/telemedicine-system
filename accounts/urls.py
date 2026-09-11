from django.urls import path
from . import views

# All URLs for the accounts app will start with 'accounts/'
# For example: /accounts/register/, /accounts/login/, /accounts/logout/

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]