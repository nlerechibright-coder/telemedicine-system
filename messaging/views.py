from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from episodes.models import HealthEpisode, DoctorRequest
from .models import ChatRoom, ChatMessage
from .utils import can_access_chat, get_assigned_doctor
from .video import WhatsAppProviderError, build_whatsapp_link


@login_required
def chat_list_view(request):
    all_chat_rooms = ChatRoom.objects.select_related('episode', 'episode__client').all()
    
    chat_data = []
    for chat_room in all_chat_rooms:
        episode = chat_room.episode
        is_authorized = can_access_chat(request.user, episode)
        if not is_authorized:
            continue
        
        # Get the latest message
        latest_message = chat_room.messages.order_by('-sent_at').first()
        # Count unread messages (messages not sent by current user)
        unread_count = chat_room.messages.filter(
            is_read=False
        ).exclude(
            sender=request.user
        ).count()
        
        # Determine the other participant's name
        if request.user == episode.client:
            from .utils import get_assigned_doctor
            doctor = get_assigned_doctor(episode)
            other_participant_name = f"Dr. {doctor.email}" if doctor else "Doctor"
            participant_role = "Client"
        else:
            other_participant_name = episode.client.email
            participant_role = "Doctor"
        
        chat_data.append({
            'episode': episode,
            'chat_room': chat_room,
            'latest_message': latest_message,
            'unread_count': unread_count,
            'other_participant_name': other_participant_name,
            'participant_role': participant_role,
        })
    
    # Sort by latest message time (most recent first)
    chat_data.sort(
        key=lambda x: x['latest_message'].sent_at if x['latest_message'] else x['episode'].created_at,
        reverse=True
    )
    
    context = {
        'chat_data': chat_data,
    }
    
    return render(request, 'messaging/chat_list.html', context)


@login_required
def chat_view(request, episode_id):
    episode = get_object_or_404(HealthEpisode, id=episode_id)
    
    if not can_access_chat(request.user, episode):
        return HttpResponseForbidden("You are not authorized to access this chat.")
    
    chat_room = get_object_or_404(ChatRoom, episode=episode)
    messages = chat_room.messages.select_related('sender').order_by('sent_at')
    
    if request.user == episode.client:
        from .utils import get_assigned_doctor
        doctor = get_assigned_doctor(episode)
        other_participant_name = f"Dr. {doctor.email}" if doctor else "Doctor"
    else:
        other_participant_name = episode.client.email
    
    context = {
        'episode': episode,
        'chat_room': chat_room,
        'messages': messages,
        'other_participant_name': other_participant_name,
        'current_user': request.user,
    }
    
    return render(request, 'messaging/chat.html', context)


@login_required
def start_video_view(request, episode_id):
    episode = get_object_or_404(HealthEpisode, id=episode_id)
    assigned_doctor = get_assigned_doctor(episode)

    is_participant = (
        episode.client_id == request.user.id
        or (assigned_doctor is not None and assigned_doctor.id == request.user.id)
    )
    if not is_participant:
        return HttpResponseForbidden("You are not authorized to access this video consultation.")

    if episode.status != HealthEpisode.Status.IN_CONSULTATION:
        messages.error(request, 'Video consultation is only available for an active consultation.')
        return redirect('messaging:chat_view', episode_id=episode.id)

    target_profile = None
    message = ''
    if request.user == episode.client:
        doctor = get_assigned_doctor(episode)
        target_profile = getattr(doctor, 'doctor_profile', None)
        message = 'Hello Doctor, I am ready for our telemedicine consultation.'
    else:
        target_profile = getattr(episode.client, 'client_profile', None)
        message = 'Hello, I am ready for our telemedicine consultation.'

    if target_profile is None:
        messages.error(request, 'Video consultation is not available because the other participant profile is missing.')
        return redirect('messaging:chat_view', episode_id=episode.id)

    try:
        whatsapp_url = build_whatsapp_link(target_profile.whatsapp_number, message)
    except WhatsAppProviderError as error:
        messages.error(request, str(error))
        return redirect('messaging:chat_view', episode_id=episode.id)

    if episode.video_started_at is None:
        episode.video_started_at = timezone.now()
        episode.save(update_fields=['video_started_at', 'updated_at'])

    return redirect(whatsapp_url)


@login_required
@require_http_methods(["GET", "POST"])
def api_messages(request, episode_id):
    episode = get_object_or_404(HealthEpisode, id=episode_id)
    
    if not can_access_chat(request.user, episode):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    chat_room = get_object_or_404(ChatRoom, episode=episode)
    
    if request.method == 'GET':
        after_id = request.GET.get('after')
        
        if after_id:
            messages = chat_room.messages.filter(id__gt=after_id).select_related('sender').order_by('sent_at')
        else:
            messages = chat_room.messages.select_related('sender').order_by('sent_at')
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'sender_id': msg.sender.id,
                'sender_email': msg.sender.email,
                'sender_role': 'client' if msg.sender == episode.client else 'doctor',
                'content': msg.content,
                'sent_at': msg.sent_at.isoformat(),
                'is_read': msg.is_read,
            })
        
        return JsonResponse({'messages': messages_data})
    
    elif request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Message content cannot be empty'}, status=400)
        
        if len(content) > 5000:
            return JsonResponse({'error': 'Message is too long (max 5000 characters)'}, status=400)
        
        message = ChatMessage.objects.create(
            room=chat_room,
            sender=request.user,
            content=content
        )
        
        return JsonResponse({
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_email': message.sender.email,
            'sender_role': 'client' if message.sender == episode.client else 'doctor',
            'content': message.content,
            'sent_at': message.sent_at.isoformat(),
            'is_read': message.is_read,
        }, status=201)


@login_required
@require_http_methods(["POST"])
def api_mark_read(request, episode_id):
    episode = get_object_or_404(HealthEpisode, id=episode_id)
    
    if not can_access_chat(request.user, episode):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    chat_room = get_object_or_404(ChatRoom, episode=episode)
    
    unread_count = chat_room.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)
    
    return JsonResponse({
        'success': True,
        'marked_count': unread_count
    })