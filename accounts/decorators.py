from functools import wraps
from django.http import HttpResponseForbidden


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("شما هنوز وارد حساب کاربری خود نشده اید.")
            
            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("شما مجاز به دسترسی به این صفحه نیستید.")
        return _wrapped_view
    return decorator