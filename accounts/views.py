from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from .forms import ClientRegistrationForm, CustomLoginForm
from .models import CustomUser


def register_view(request):
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
                return redirect('home') # Update to doctors:dashboard when ready
            elif user.is_admin:
                return redirect('admin:index')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'ALLOW_MANAGER_CREATION': getattr(settings, 'ALLOW_MANAGER_CREATION', False)
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


def setup_manager_view(request):
    """Temporary view to create the first and only management account."""
    if not getattr(settings, 'ALLOW_MANAGER_CREATION', False):
        return redirect('accounts:login')
    
    if CustomUser.objects.filter(role=CustomUser.Role.MANAGER).exists():
        messages.error(request, 'Management account already exists.')
        return redirect('accounts:login')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not email or not password:
            messages.error(request, 'Email and password are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                CustomUser.objects.create_user(
                    email=email, password=password, role=CustomUser.Role.MANAGER, is_active=True
                )
                messages.success(request, 'Management account created successfully. You can now log in.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                
    return render(request, 'accounts/setup_manager.html')