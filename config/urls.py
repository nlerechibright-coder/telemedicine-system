"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import our dynamic home view
from .views import home_view

urlpatterns = [
    # Django Admin Interface
    path('admin/', admin.site.urls),
    
    # Accounts App (Registration, Login, Logout)
    path('accounts/', include('accounts.urls')),
    
    # Clients App (Profile management)
    path('clients/', include('clients.urls')),
    
    # Doctors App (Dashboard, Profile, Availability)
    path('doctors/', include('doctors.urls')),
    
    # Knowledge Base App (Health Articles)
    path('knowledge/', include('knowledge_base.urls')),
    
    # Consultations App (Requests, Messaging, History)
    path('consultations/', include('consultations.urls')),
    
    # Medical Data App (Symptom Checker & Matching Engine)
    path('medical/', include('medical_data.urls')),
    
    # Episodes App (Health Episodes & Doctor Requests)
    path('episodes/', include('episodes.urls')),
    
    # Messaging App (Chat)
    path('messaging/', include('messaging.urls')),
    
    # Dynamic Home Page (Shows role-specific stats and notifications)
    path('', home_view, name='home'),
]

# Serve media files during development (when DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)