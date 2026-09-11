from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClientProfile
from .forms import ClientProfileForm


@login_required
def complete_profile_view(request):
    """
    View for clients to complete their profile for the first time.
    Only accessible to users with the CLIENT role who don't have a profile yet.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Only clients can complete a profile.')
        return redirect('home')
    
    # Check if profile already exists
    if hasattr(request.user, 'client_profile'):
        messages.info(request, 'You have already completed your profile.')
        return redirect('clients:view_profile')
    
    if request.method == 'POST':
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            # Create the profile but don't save to database yet
            profile = form.save(commit=False)
            # Link it to the current user
            profile.user = request.user
            # Now save to database
            profile.save()
            
            messages.success(request, 'Your profile has been created successfully!')
            return redirect('clients:view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientProfileForm()
    
    return render(request, 'clients/complete_profile.html', {'form': form})


@login_required
def view_profile_view(request):
    """
    View for clients to see their profile information.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Only clients can view a client profile.')
        return redirect('home')
    
    # Get or create the profile
    try:
        profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile first.')
        return redirect('clients:complete_profile')
    
    return render(request, 'clients/view_profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    """
    View for clients to edit their existing profile.
    """
    
    # Check if user is a client
    if not request.user.is_client:
        messages.error(request, 'Only clients can edit a client profile.')
        return redirect('home')
    
    # Get the profile (or redirect if it doesn't exist)
    try:
        profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile first.')
        return redirect('clients:complete_profile')
    
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('clients:view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientProfileForm(instance=profile)
    
    return render(request, 'clients/edit_profile.html', {'form': form, 'profile': profile})