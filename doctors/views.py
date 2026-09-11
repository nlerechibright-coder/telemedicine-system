from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import DoctorProfile
from .forms import DoctorProfileEditForm, DoctorAvailabilityForm
from episodes.models import DoctorRequest
from messaging.models import ChatMessage


@login_required
def doctor_dashboard_view(request):
    """
    Main dashboard for doctors.
    Shows their profile summary, availability status, and (later) pending requests.
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Only doctors can view this page.')
        return redirect('home')
    
    # Get the doctor's profile
    try:
        profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Your doctor profile is not set up. Please contact an administrator.')
        return redirect('home')
    
    # Prepare the availability form (pre-filled with current status)
    availability_form = DoctorAvailabilityForm(instance=profile)
    pending_requests = DoctorRequest.objects.filter(
        doctor=request.user,
        status=DoctorRequest.Status.PENDING,
    ).select_related('episode', 'client')
    active_consultations = DoctorRequest.objects.filter(
        doctor=request.user,
        status=DoctorRequest.Status.ACCEPTED,
    ).select_related('episode', 'client')
    unread_messages = ChatMessage.objects.filter(
        room__episode__doctor_requests__doctor=request.user,
        room__episode__doctor_requests__status=DoctorRequest.Status.ACCEPTED,
        is_read=False,
    ).exclude(sender=request.user).distinct().count()
    
    return render(request, 'doctors/dashboard.html', {
        'profile': profile,
        'availability_form': availability_form,
        'pending_requests': pending_requests,
        'active_consultations': active_consultations,
        'unread_messages': unread_messages,
    })


@login_required
def view_profile_view(request):
    """
    Doctor views their own professional profile.
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Only doctors can view this page.')
        return redirect('home')
    
    # Get the doctor's profile
    try:
        profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Your doctor profile is not set up. Please contact an administrator.')
        return redirect('home')
    
    return render(request, 'doctors/view_profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    """
    Doctor edits their own professional information (qualifications, bio, fee).
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied. Only doctors can edit this page.')
        return redirect('home')
    
    # Get the doctor's profile
    try:
        profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Your doctor profile is not set up. Please contact an administrator.')
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('doctors:view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorProfileEditForm(instance=profile)
    
    return render(request, 'doctors/edit_profile.html', {'form': form, 'profile': profile})


@login_required
@require_POST
def update_availability_view(request):
    """
    Doctor updates their availability status (AVAILABLE, BUSY, AWAY, OFFLINE).
    This is a POST-only endpoint for security (prevents accidental changes via URL).
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get the doctor's profile
    try:
        profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Your doctor profile is not set up.')
        return redirect('home')
    
    # Process the form
    form = DoctorAvailabilityForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, f'Your status has been updated to {profile.get_availability_status_display()}.')
    else:
        messages.error(request, 'Could not update status. Please try again.')
    
    return redirect('doctors:dashboard')