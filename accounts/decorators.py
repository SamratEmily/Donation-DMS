from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            raise PermissionDenied("You must be an admin to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def donor_required(view_func):
    """
    Decorator to restrict access to donor users only.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_donor():
            raise PermissionDenied("You must be a donor to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def volunteer_required(view_func):
    """
    Decorator to restrict access to volunteer users only.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_volunteer():
            raise PermissionDenied("You must be a volunteer to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


