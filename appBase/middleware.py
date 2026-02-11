from django.shortcuts import redirect
from django.urls import reverse

# class ForcePasswordChangeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             # Revisar la variable de sesión en vez de request.user
#             cambio_contrasena = request.session.get("cambiocontrasena", False)
            
#             if cambio_contrasena:
#                 cambiar_url = reverse('change_password')
#                 if request.path != cambiar_url:
#                     return redirect('change_password')

#         return self.get_response(request)

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cambio_contrasena = request.session.get("cambiocontrasena", False)
            cambiar_url = reverse('change_password')
            login_url = reverse('login')
            logout_url = reverse('logout')
            # Solo redirige si NO está en login ni logout
            if cambio_contrasena and request.path not in [cambiar_url, login_url, logout_url]:
                return redirect('change_password')
        return self.get_response(request)