from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from .decorators import management_role_required
from doctors.models import DoctorProfile, Specialty
from consultations.models import Consultation
from knowledge_base.models import Article, Category

User = get_user_model()

@management_role_required
def dashboard(request):
    context = {
        'total_clients': User.objects.filter(role=User.Role.CLIENT).count(),
        'total_doctors': User.objects.filter(role=User.Role.DOCTOR).count(),
        'pending_doctors': DoctorProfile.objects.filter(is_verified=False).count(),
        'verified_doctors': DoctorProfile.objects.filter(is_verified=True).count(),
        'total_consultations': Consultation.objects.count(),
        'pending_consultations': Consultation.objects.filter(status=Consultation.Status.PENDING).count(),
        'total_articles': Article.objects.count(),
        'recent_users': User.objects.exclude(role=User.Role.MANAGER).order_by('-date_joined')[:5],
        'recent_consultations': Consultation.objects.select_related('client', 'doctor').order_by('-created_at')[:5],
    }
    return render(request, 'management/dashboard.html', context)

@management_role_required
def user_list(request):
    users = User.objects.exclude(role=User.Role.MANAGER).order_by('-date_joined')
    search_query = request.GET.get('q', '')
    if search_query:
        users = users.filter(email__icontains=search_query)
    return render(request, 'management/user_list.html', {'users': users, 'search_query': search_query})

@management_role_required
def user_toggle_active(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'User {user.email} has been {"activated" if user.is_active else "deactivated"}.')
    return redirect('management:user_list')

@management_role_required
def doctor_list(request):
    doctors = User.objects.filter(role=User.Role.DOCTOR).select_related('doctor_profile', 'doctor_profile__specialty').order_by('-date_joined')
    search_query = request.GET.get('q', '')
    if search_query:
        doctors = doctors.filter(Q(email__icontains=search_query) | Q(doctor_profile__license_number__icontains=search_query))
    return render(request, 'management/doctor_list.html', {'doctors': doctors, 'search_query': search_query})

@management_role_required
def doctor_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        specialty_id = request.POST.get('specialty')
        license_number = request.POST.get('license_number')
        qualifications = request.POST.get('qualifications')
        consultation_fee = request.POST.get('consultation_fee')
        
        try:
            with transaction.atomic():
                # Create User
                user = User.objects.create_user(email=email, password=password, role=User.Role.DOCTOR, is_active=True)
                # Create Profile
                specialty = Specialty.objects.get(id=specialty_id)
                DoctorProfile.objects.create(
                    user=user, specialty=specialty, license_number=license_number,
                    qualifications=qualifications, consultation_fee=consultation_fee, is_verified=True
                )
            messages.success(request, f'Doctor {email} created successfully. Please provide them with their credentials securely.')
            return redirect('management:doctor_list')
        except Exception as e:
            messages.error(request, f'Error creating doctor: {str(e)}')
            
    return render(request, 'management/doctor_create.html', {'specialties': Specialty.objects.all()})

@management_role_required
def doctor_verify(request, doctor_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        profile = get_object_or_404(DoctorProfile, user_id=doctor_id)
        profile.is_verified = (action == 'verify')
        profile.save()
        messages.success(request, f'Doctor verification {"approved" if profile.is_verified else "revoked"}.')
    return redirect('management:doctor_list')

@management_role_required
def consultation_list(request):
    consultations = Consultation.objects.select_related('client', 'doctor').order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        consultations = consultations.filter(status=status_filter)
    return render(request, 'management/consultation_list.html', {'consultations': consultations, 'status_filter': status_filter})

@management_role_required
def kb_list(request):
    articles = Article.objects.select_related('category', 'author').order_by('-created_at')
    return render(request, 'management/kb_list.html', {'articles': articles})