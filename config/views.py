from django.shortcuts import render
from episodes.models import DoctorRequest


def home_view(request):
    """
    Dynamic home page that shows role-specific quick stats and notifications.
    If the user is not logged in, it simply renders the static home page.
    """
    context = {}
    
    if request.user.is_authenticated:
        if request.user.is_client:
            # Client stats
            context['pending_consultations'] = DoctorRequest.objects.filter(
                client=request.user, 
                status=DoctorRequest.Status.PENDING
            ).count()
            
            context['active_consultations'] = DoctorRequest.objects.filter(
                client=request.user, 
                status=DoctorRequest.Status.ACCEPTED
            ).count()
            
        elif request.user.is_doctor:
            # Doctor stats
            context['pending_requests'] = DoctorRequest.objects.filter(
                doctor=request.user,
                status=DoctorRequest.Status.PENDING
            ).count()
            
            context['active_consultations'] = DoctorRequest.objects.filter(
                doctor=request.user,
                status=DoctorRequest.Status.ACCEPTED
            ).count()

    return render(request, 'home.html', context)