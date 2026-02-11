from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps
import time

def permisosRequeridos(*permisos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Si no está logueado → enviar con ?next=
            if not request.user.is_authenticated:
                login_url = reverse('login')
                return redirect(f"{login_url}?next={request.path}")
            
            if any([request.user.has_perm(permiso) for permiso in permisos]):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(f"{reverse('accesoRestringido')}")  # Redirige a la página accesoRestringido si no tiene los permisos necesarios
        return _wrapped_view
    return decorator
