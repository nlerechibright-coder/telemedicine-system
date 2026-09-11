from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from episodes.models import DoctorRequest, HealthEpisode
from .models import Consultation, Message
from .forms import (
    ConsultationRequestForm, 
    ConsultationResponseForm, 
    MessageForm,
    DoctorNotesForm
)


# ============================================
# CLIENT VIEWS
# ============================================

@login_required
def request_consultation_view(request):
    """
    Client requests a consultation with a doctor.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Only clients can request consultations.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                episode = HealthEpisode.objects.create(
                    client=request.user,
                    title='Consultation Request',
                    status=HealthEpisode.Status.AWAITING_DOCTOR,
                )
                doctor_request = DoctorRequest.objects.create(
                    episode=episode,
                    client=request.user,
                    doctor=form.cleaned_data['doctor'],
                    reason=form.cleaned_data['reason'],
                )
            
            messages.success(request, 'Your consultation request has been sent successfully!')
            return redirect('episodes:client_request_detail', request_id=doctor_request.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConsultationRequestForm()
    
    return render(request, 'consultations/request_consultation.html', {'form': form})


@login_required
def client_consultation_list_view(request):
    """
    Client views all their consultations.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get all consultations for this client
    consultations = Consultation.objects.filter(client=request.user)
    
    return render(request, 'consultations/client_consultation_list.html', {
        'consultations': consultations,
    })


@login_required
def client_consultation_detail_view(request, consultation_id):
    """
    Client views a specific consultation and can send messages.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get the consultation (must belong to this client)
    consultation = get_object_or_404(Consultation, id=consultation_id, client=request.user)
    
    # Get all messages for this consultation
    messages_list = consultation.messages.all()
    
    # Message form (only if consultation is accepted)
    message_form = MessageForm()
    
    if request.method == 'POST' and 'send_message' in request.POST:
        if consultation.can_be_messaged:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.consultation = consultation
                message.sender = request.user
                message.save()
                messages.success(request, 'Message sent successfully!')
                return redirect('consultations:client_consultation_detail', consultation_id=consultation.id)
        else:
            messages.error(request, 'Messaging is not available for this consultation.')
    
    return render(request, 'consultations/client_consultation_detail.html', {
        'consultation': consultation,
        'messages_list': messages_list,
        'message_form': message_form,
    })


# ============================================
# DOCTOR VIEWS
# ============================================

@login_required
def doctor_pending_requests_view(request):
    """
    Doctor views all pending consultation requests.
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get all pending consultations for this doctor
    consultations = Consultation.objects.filter(doctor=request.user, status=Consultation.Status.PENDING)
    
    return render(request, 'consultations/doctor_pending_requests.html', {
        'consultations': consultations,
    })


@login_required
def doctor_consultation_list_view(request):
    """
    Doctor views all their consultations (excluding pending).
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get all consultations for this doctor (excluding pending)
    consultations = Consultation.objects.filter(doctor=request.user).exclude(status=Consultation.Status.PENDING)
    
    return render(request, 'consultations/doctor_consultation_list.html', {
        'consultations': consultations,
    })


@login_required
def doctor_consultation_detail_view(request, consultation_id):
    """
    Doctor views a specific consultation, can accept/reject, add notes, and send messages.
    """
    
    # Check if user is a doctor
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get the consultation (must belong to this doctor)
    consultation = get_object_or_404(Consultation, id=consultation_id, doctor=request.user)
    
    # Get all messages for this consultation
    messages_list = consultation.messages.all()
    
    # Forms
    response_form = ConsultationResponseForm(instance=consultation)
    notes_form = DoctorNotesForm(instance=consultation)
    message_form = MessageForm()
    
    if request.method == 'POST':
        # Handle accept/reject
        if 'respond_consultation' in request.POST:
            response_form = ConsultationResponseForm(request.POST, instance=consultation)
            if response_form.is_valid():
                response_form.save()
                messages.success(request, f'Consultation has been {consultation.get_status_display().lower()}.')
                return redirect('consultations:doctor_consultation_detail', consultation_id=consultation.id)
        
        # Handle notes update
        elif 'update_notes' in request.POST:
            notes_form = DoctorNotesForm(request.POST, instance=consultation)
            if notes_form.is_valid():
                notes_form.save()
                messages.success(request, 'Notes updated successfully!')
                return redirect('consultations:doctor_consultation_detail', consultation_id=consultation.id)
        
        # Handle message sending
        elif 'send_message' in request.POST:
            if consultation.can_be_messaged:
                message_form = MessageForm(request.POST)
                if message_form.is_valid():
                    message = message_form.save(commit=False)
                    message.consultation = consultation
                    message.sender = request.user
                    message.save()
                    messages.success(request, 'Message sent successfully!')
                    return redirect('consultations:doctor_consultation_detail', consultation_id=consultation.id)
            else:
                messages.error(request, 'Messaging is not available for this consultation.')
    
    return render(request, 'consultations/doctor_consultation_detail.html', {
        'consultation': consultation,
        'messages_list': messages_list,
        'response_form': response_form,
        'notes_form': notes_form,
        'message_form': message_form,
    })