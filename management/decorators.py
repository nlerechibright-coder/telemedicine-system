from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def management_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        # Server-side check for the explicit MANAGER role
        if not getattr(request.user, 'is_manager', False):
            messages.error(request, 'Access Denied: Management privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view