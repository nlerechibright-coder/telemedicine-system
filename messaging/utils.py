"""
Utility functions for the messaging app.
Contains authorization helpers and other shared logic.
"""

from episodes.models import DoctorRequest


def can_access_chat(user, episode):
    if episode.client_id == user.id:
        return DoctorRequest.objects.filter(
            episode=episode,
            client=user,
            status=DoctorRequest.Status.ACCEPTED,
        ).exists()

    return DoctorRequest.objects.filter(
        episode=episode,
        doctor=user,
        status=DoctorRequest.Status.ACCEPTED
    ).exists()


def get_assigned_doctor(episode):
    """
    Get the doctor assigned to a health episode (via accepted DoctorRequest).
    """
    accepted_request = DoctorRequest.objects.filter(
        episode=episode,
        status=DoctorRequest.Status.ACCEPTED
    ).select_related('doctor').first()
    
    if accepted_request:
        return accepted_request.doctor
    
    return None