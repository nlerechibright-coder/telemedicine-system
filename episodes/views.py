from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseForbidden
from medical_data.models import Symptom, Condition, ConditionSymptom
from episodes.models import HealthEpisode, EpisodeSymptom, EpisodeConditionMatch, DoctorRequest
from episodes.forms import DoctorRequestForm, DoctorResponseForm


@login_required
def symptom_select_view(request):
    if not request.user.is_client:
        messages.error(request, 'Only clients can use the symptom checker.')
        return redirect('home')
    
    symptoms = Symptom.objects.all().order_by('name')
    red_flag_symptoms = symptoms.filter(is_red_flag=True)
    normal_symptoms = symptoms.filter(is_red_flag=False)
    
    return render(request, 'medical_data/symptom_select.html', {
        'red_flag_symptoms': red_flag_symptoms,
        'normal_symptoms': normal_symptoms,
    })


@login_required
def symptom_match_view(request):
    if not request.user.is_client:
        messages.error(request, 'Only clients can use the symptom checker.')
        return redirect('home')
    
    selected_symptom_ids = request.POST.getlist('symptoms')
    
    if not selected_symptom_ids:
        messages.warning(request, 'Please select at least one symptom.')
        return redirect('medical_data:symptom_select')
    
    selected_symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)
    
    red_flag_symptoms = selected_symptoms.filter(is_red_flag=True)
    emergency_messages = []
    has_emergency = False
    
    if red_flag_symptoms.exists():
        has_emergency = True
        for symptom in red_flag_symptoms:
            if symptom.emergency_message:
                emergency_messages.append({
                    'symptom_name': symptom.name,
                    'message': symptom.emergency_message,
                })
    
    episode_status = HealthEpisode.Status.EMERGENCY if has_emergency else HealthEpisode.Status.MATCHING
    symptom_names = [s.name for s in selected_symptoms[:3]]
    title_suffix = "..." if len(selected_symptoms) > 3 else ""
    episode_title = f"Symptom Check: {', '.join(symptom_names)}{title_suffix}"
    
    with transaction.atomic():
        episode = HealthEpisode.objects.create(
            client=request.user,
            title=episode_title,
            status=episode_status
        )
        
        for symptom in selected_symptoms:
            EpisodeSymptom.objects.create(
                episode=episode,
                symptom=symptom,
                reported_severity=EpisodeSymptom.Severity.MODERATE
            )
        
        matching_rules = ConditionSymptom.objects.filter(
            symptom__in=selected_symptoms
        ).select_related('condition', 'symptom')
        
        condition_scores = {}
        
        for rule in matching_rules:
            condition_id = rule.condition_id
            
            if condition_id not in condition_scores:
                condition_scores[condition_id] = {
                    'condition': rule.condition,
                    'total_score': 0,
                    'matched_symptoms': [],
                    'matched_symptom_ids': set(),
                }
            
            condition_scores[condition_id]['total_score'] += rule.weight
            condition_scores[condition_id]['matched_symptoms'].append({
                'name': rule.symptom.name,
                'weight': rule.weight,
                'is_core': rule.is_core,
            })
            condition_scores[condition_id]['matched_symptom_ids'].add(rule.symptom_id)
        
        sorted_conditions = []
        
        for condition_id, data in condition_scores.items():
            total_symptoms_for_condition = ConditionSymptom.objects.filter(
                condition_id=condition_id
            ).count()
            
            matched_count = len(data['matched_symptom_ids'])
            coverage = round((matched_count / total_symptoms_for_condition) * 100, 1) if total_symptoms_for_condition > 0 else 0.0
            
            data['coverage'] = coverage
            
            EpisodeConditionMatch.objects.create(
                episode=episode,
                condition=data['condition'],
                match_score=data['total_score'],
                coverage_percentage=coverage
            )
            
            data['articles'] = data['condition'].articles.filter(is_published=True)
            sorted_conditions.append(data)
        
        sorted_conditions.sort(key=lambda x: x['total_score'], reverse=True)
    
    return render(request, 'medical_data/symptom_match_results.html', {
        'episode': episode,
        'selected_symptoms': selected_symptoms,
        'emergency_messages': emergency_messages,
        'has_emergency': has_emergency,
        'matched_conditions': sorted_conditions,
        'no_matches': len(sorted_conditions) == 0,
    })


@login_required
def request_doctor_view(request, episode_id):
    if not request.user.is_client:
        messages.error(request, 'Only clients can request doctor consultations.')
        return redirect('home')
    
    episode = get_object_or_404(HealthEpisode, id=episode_id, client=request.user)
    
    if episode.status not in [HealthEpisode.Status.MATCHING, HealthEpisode.Status.AWAITING_DOCTOR]:
        messages.error(request, 'This episode is not in a state that allows doctor requests.')
        return redirect('episodes:episode_detail', episode_id=episode.id)
    
    if request.method == 'POST':
        form = DoctorRequestForm(request.POST, episode=episode, client=request.user)
        if form.is_valid():
            doctor_request = form.save()
            messages.success(request, 'Your doctor request has been submitted successfully!')
            return redirect('episodes:client_request_detail', request_id=doctor_request.id)
    else:
        form = DoctorRequestForm(episode=episode, client=request.user)
    
    return render(request, 'episodes/request_doctor.html', {
        'form': form,
        'episode': episode,
    })


@login_required
def client_request_list_view(request):
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    requests = DoctorRequest.objects.filter(client=request.user).select_related('episode', 'doctor', 'requested_specialty')
    
    return render(request, 'episodes/client_request_list.html', {
        'requests': requests,
    })


@login_required
def client_request_detail_view(request, request_id):
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor_request = get_object_or_404(DoctorRequest, id=request_id, client=request.user)
    
    return render(request, 'episodes/client_request_detail.html', {
        'doctor_request': doctor_request,
    })


@login_required
def doctor_pending_requests_view(request):
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Show requests specifically for this doctor, OR requests made by specialty that are still pending
    pending_requests = DoctorRequest.objects.filter(
        status=DoctorRequest.Status.PENDING
    ).filter(
        doctor=request.user
    ).select_related('episode', 'client')
    
    # Also include specialty-based requests (where doctor is null)
    specialty_requests = DoctorRequest.objects.filter(
        status=DoctorRequest.Status.PENDING,
        doctor__isnull=True,
        requested_specialty__isnull=False
    ).select_related('episode', 'client')
    
    # Combine and remove duplicates
    all_pending = (pending_requests | specialty_requests).distinct()
    
    return render(request, 'episodes/doctor_pending_requests.html', {
        'pending_requests': all_pending,
    })


@login_required
def doctor_request_detail_view(request, request_id):
    print("="*60)
    print(f"DEBUG doctor_request_detail_view: user={request.user.email} (ID: {request.user.id}), request_id={request_id}")
    
    if not request.user.is_doctor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Allow access if the request is for this doctor OR if it's a specialty request (doctor is null)
    doctor_request = get_object_or_404(
        DoctorRequest.objects.filter(
            id=request_id
        ).filter(
            doctor=request.user
        ) | DoctorRequest.objects.filter(
            id=request_id,
            doctor__isnull=True
        )
    )
    print(f"DEBUG: Found doctor_request: {doctor_request.id}, status: {doctor_request.status}, doctor_id: {doctor_request.doctor_id}")
    
    if doctor_request.status != DoctorRequest.Status.PENDING:
        messages.info(request, 'This request has already been responded to.')
        return redirect('episodes:doctor_request_detail', request_id=doctor_request.id)
    
    if request.method == 'POST':
        print("DEBUG: POST request received")
        form = DoctorResponseForm(request.POST, instance=doctor_request)
        print(f"DEBUG: form.is_valid() = {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: form.errors = {form.errors}")
            print(f"DEBUG: form.non_field_errors = {form.non_field_errors}")
        
        if form.is_valid():
            print("DEBUG: Form is valid, saving...")
            instance = form.save(commit=False)
            
            # CRITICAL FIX: If the doctor is accepting a request that was made by specialty (doctor is null),
            # we MUST assign this doctor to the request so they can access the chat.
            if instance.status == DoctorRequest.Status.ACCEPTED and not instance.doctor_id:
                instance.doctor = request.user
                print(f"DEBUG: Auto-assigned doctor {request.user.email} (ID: {request.user.id}) to request {instance.id}")
            
            instance.save()
            print("DEBUG: Form saved successfully.")
            
            if instance.status == DoctorRequest.Status.ACCEPTED:
                messages.success(request, 'You have accepted this consultation request.')
            else:
                messages.info(request, 'You have rejected this consultation request.')
            
            return redirect('episodes:doctor_pending_requests')
    else:
        form = DoctorResponseForm(instance=doctor_request)
    
    episode = doctor_request.episode
    episode_symptoms = episode.episode_symptoms.select_related('symptom')
    episode_matches = episode.condition_matches.select_related('condition')[:5]
    
    return render(request, 'episodes/doctor_request_detail.html', {
        'doctor_request': doctor_request,
        'form': form,
        'episode': episode,
        'episode_symptoms': episode_symptoms,
        'episode_matches': episode_matches,
    })


@login_required
def episode_list_view(request):
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    episodes = HealthEpisode.objects.filter(client=request.user).prefetch_related(
        'episode_symptoms', 'condition_matches', 'doctor_requests'
    )
    
    return render(request, 'episodes/episode_list.html', {
        'episodes': episodes,
    })


@login_required
def episode_detail_view(request, episode_id):
    if not request.user.is_client:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    episode = get_object_or_404(HealthEpisode, id=episode_id, client=request.user)
    
    symptoms = episode.episode_symptoms.select_related('symptom')
    matches = episode.condition_matches.select_related('condition')
    requests = episode.doctor_requests.select_related('doctor', 'requested_specialty')
    
    return render(request, 'episodes/episode_detail.html', {
        'episode': episode,
        'symptoms': symptoms,
        'matches': matches,
        'requests': requests,
    })