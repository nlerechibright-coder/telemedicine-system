from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClientRegistrationForm, CustomLoginForm


def register_view(request):
    """
    Handle client registration.
    If the user is already logged in, redirect them to the home page.
    If the form is submitted with valid data, create the user and log them in.
    Otherwise, display the empty registration form.
    """
    
    # If user is already logged in, they shouldn't be on the register page
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Form was submitted - process the data
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            
            # Log the user in automatically after registration
            login(request, user)
            
            # Show a success message
            messages.success(request, f'Welcome! Your account has been created successfully.')
            
            # Redirect to home page (we'll update this to client dashboard later)
            return redirect('home')
        else:
            # Form has errors - show them to the user
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show the empty form
        form = ClientRegistrationForm()
    
    # Render the registration template with the form
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    Supports login for all user types (Client, Doctor, Admin) using email and password.
    Redirects users to different pages based on their role.
    """
    
    # If user is already logged in, redirect them
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Form was submitted
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            
            # Log the user in
            login(request, user)
            
            # Show a welcome message
            messages.success(request, f'Welcome back, {user.email}!')
            
            # Redirect based on user role
            if user.is_doctor:
                return redirect('home')  # Will be updated to doctor dashboard later
            elif user.is_admin:
                return redirect('admin:index')  # Django admin panel
            else:
                return redirect('home')  # Will be updated to client dashboard later
        else:
            # Invalid credentials
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        # GET request - show the empty login form
        form = CustomLoginForm()
    
    # Render the login template with the form
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.
    Logs the user out and redirects them to the home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')