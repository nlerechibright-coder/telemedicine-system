import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from .models import Symptom, Condition, ConditionSymptom

logger = logging.getLogger(__name__)


@login_required
@never_cache
def symptom_select_view(request):
    """
    Display all symptoms for the client to select.
    Symptoms are grouped alphabetically for easy browsing.
    """
    
    # Only clients can access the symptom checker
    if not request.user.is_client:
        messages.error(request, 'Only clients can use the symptom checker.')
        return redirect('home')
    
    # Get all symptoms ordered alphabetically
    symptoms = Symptom.objects.all().order_by('name')
    
    # Separate red-flag symptoms for prominent display
    red_flag_symptoms = symptoms.filter(is_red_flag=True)
    normal_symptoms = symptoms.filter(is_red_flag=False)
    logger.info(
        'Symptom checker loaded for client %s: %d normal, %d red-flag symptoms',
        request.user.pk,
        normal_symptoms.count(),
        red_flag_symptoms.count(),
    )
    
    return render(request, 'medical_data/symptom_select.html', {
        'red_flag_symptoms': red_flag_symptoms,
        'normal_symptoms': normal_symptoms,
    })


@login_required
def symptom_match_view(request):
    """
    Process selected symptoms and display matching conditions.
    Uses a rule-based matching engine with weighted scoring.
    """
    
    # Only clients can access the symptom checker
    if not request.user.is_client:
        messages.error(request, 'Only clients can use the symptom checker.')
        return redirect('home')
    
    # Get selected symptom IDs from POST data
    selected_symptom_ids = request.POST.getlist('symptoms')
    
    # Validate that at least one symptom was selected
    if not selected_symptom_ids:
        messages.warning(request, 'Please select at least one symptom.')
        return redirect('medical_data:symptom_select')
    
    # Fetch the selected symptoms
    selected_symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)
    
    # =========================================================================
    # RED FLAG DETECTION
    # =========================================================================
    red_flag_symptoms = selected_symptoms.filter(is_red_flag=True)
    emergency_messages = []
    
    if red_flag_symptoms.exists():
        for symptom in red_flag_symptoms:
            if symptom.emergency_message:
                emergency_messages.append({
                    'symptom_name': symptom.name,
                    'message': symptom.emergency_message,
                })
    
    # =========================================================================
    # RULE-BASED MATCHING ENGINE
    # =========================================================================
    # Query all ConditionSymptom rules where the symptom is in the selected list
    matching_rules = ConditionSymptom.objects.filter(
        symptom__in=selected_symptoms
    ).select_related('condition', 'symptom')
    
    # Group rules by condition and calculate scores
    condition_scores = {}
    
    for rule in matching_rules:
        condition_id = rule.condition_id
        
        if condition_id not in condition_scores:
            # Initialize condition entry
            condition_scores[condition_id] = {
                'condition': rule.condition,
                'total_score': 0,
                'matched_symptoms': [],
                'matched_symptom_ids': set(),
            }
        
        # Add weight to total score
        condition_scores[condition_id]['total_score'] += rule.weight
        
        # Track matched symptoms
        condition_scores[condition_id]['matched_symptoms'].append({
            'name': rule.symptom.name,
            'weight': rule.weight,
            'is_core': rule.is_core,
        })
        condition_scores[condition_id]['matched_symptom_ids'].add(rule.symptom_id)
    
    # Calculate coverage for each condition
    for condition_id, data in condition_scores.items():
        # Get total number of symptoms defined for this condition
        total_symptoms_for_condition = ConditionSymptom.objects.filter(
            condition_id=condition_id
        ).count()
        
        matched_count = len(data['matched_symptom_ids'])
        
        # Coverage = (matched symptoms / total symptoms for this condition) * 100
        if total_symptoms_for_condition > 0:
            data['coverage'] = round((matched_count / total_symptoms_for_condition) * 100, 1)
        else:
            data['coverage'] = 0
    
    # Sort conditions by total_score descending
    sorted_conditions = sorted(
        condition_scores.values(),
        key=lambda x: x['total_score'],
        reverse=True
    )
    
    # Fetch linked KB articles for each condition
    for condition_data in sorted_conditions:
        condition = condition_data['condition']
        # Get published articles linked to this condition
        articles = condition.articles.filter(is_published=True)
        condition_data['articles'] = articles
    
    # =========================================================================
    # RENDER RESULTS
    # =========================================================================
    return render(request, 'medical_data/symptom_match_results.html', {
        'selected_symptoms': selected_symptoms,
        'emergency_messages': emergency_messages,
        'has_emergency': len(emergency_messages) > 0,
        'matched_conditions': sorted_conditions,
        'no_matches': len(sorted_conditions) == 0,
    })


@staff_member_required
def seed_db_temp_view(request):
    """
    Temporary view to seed the database via browser. 
    MUST BE REMOVED AFTER USE FOR SECURITY.
    """
    try:
        call_command('seed_symptoms')
        return HttpResponse(
            "<h1>✅ Success!</h1>"
            "<p>79 symptoms have been seeded into the production database.</p>"
            "<p><strong>IMPORTANT:</strong> Please delete this code from views.py and urls.py now for security.</p>"
            "<a href='/medical/symptoms/'>Go to Symptom Checker</a>"
        )
    except Exception as e:
        return HttpResponse(f"<h1>❌ Error</h1><p>{e}</p>")