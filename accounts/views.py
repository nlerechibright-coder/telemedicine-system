from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ClientRegistrationForm, CustomLoginForm
from .models import CustomUser


def register_view(request):
    """
    Handle client registration.
    Strictly enforces CLIENT role for public registration.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # STRICTLY ENFORCE CLIENT ROLE FOR PUBLIC REGISTRATION
            user.role = CustomUser.Role.CLIENT
            user.save()
            
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login with role-based redirection.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.email}!')
            
            # Role-based redirection
            if user.is_manager:
                return redirect('management:dashboard')
            elif user.is_doctor:
                return redirect('home')  # Update to doctors:dashboard when ready
            elif user.is_admin:
                return redirect('admin:index')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')