from django.shortcuts import render,redirect
from notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django import forms
from captcha.fields import CaptchaField
from django.views.decorators.cache import never_cache, cache_control
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db import connections
from django.contrib.auth.decorators import login_required
from .models import clsUsuarios

class LoginFormWithCaptcha(forms.Form):
    idusuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    contrasena = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    captcha = CaptchaField()


# -----------------------------------------------------------------------------------------------------------------
# Definir la vista del login
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    # 🚨 1. Si el usuario ya está autenticado, redirigirlo SIEMPRE antes de cualquier cosa
    if request.user.is_authenticated:
        return redirect('inicio')

    intentosFallidos = request.session.get('intentosFallidos', 0)  # Obtener intentos fallidos

    if request.method == 'POST':
        idusuario = request.POST.get('idusuario').upper()
        contrasena = request.POST.get('contrasena')

        # Si ha fallado más de 3 veces, requerimos CAPTCHA
        if intentosFallidos >= 3:
            form = LoginFormWithCaptcha(request.POST)
            if not form.is_valid():
                messages.error(request, "CAPTCHA ha sido ingresado incorrecto")
                return render(request, 'login.html', {"form": form})
        else:
            form = None

        user = authenticate(request, idusuario=idusuario, contrasena=contrasena)

        if user is not None:
            auth_login(request, user)
            request.session['intentosFallidos'] = 0  # Reiniciar intentos fallidos

            # 1. Obtener la URL a la que quería ir antes de iniciar sesión
            next_url = request.GET.get('next')

            if request.user.groups.filter(name='concejales').exists() or idusuario=='ESCUELAINTELIGENTE':
                return redirect('escuelainteligente')
            
            # 3. Si existe `next`, enviarlo allá
            if next_url:
                return redirect(next_url)
    
            return redirect('inicio')
        else:
            request.session['intentosFallidos'] = intentosFallidos + 1  # Incrementar intentos fallidos
            return redirect('login')

    else:
        if request.user.is_authenticated:
            return redirect('inicio')

    # Si ha fallado más de 3 veces, mostramos el formulario con CAPTCHA
    form = LoginFormWithCaptcha() if intentosFallidos >= 3 else None
    return render(request, 'login.html', {"form": form})


# -----------------------------------------------------------------------------------------------------------------
# Definir la vista del logout
def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout

# Definir la funcion para el cifrado de la contraseña
def encrypt_password(password):
    """
    Encrypt the password using PostgreSQL's crypt function.
    """
    with connections['default'].cursor() as cursor:
        query = "SELECT crypt(%s, gen_salt('bf'))"
        cursor.execute(query, [password])
        encrypted_password = cursor.fetchone()[0]
    return encrypted_password


# Definir la vista de cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        # Obtener los datos para verificar si es posible reestablecer la contraseña
        contrasenaActual = request.POST.get('current-password')
        nuevaContrasena = request.POST.get('new-password')
        confirmarNuevaContrasena = request.POST.get('confirm-password')
        usuario_id = request.session.get('usuario')
        user = clsUsuarios.objects.get(idusuario=usuario_id)

        try:
            with connections['default'].cursor() as cursor:
                query = """
                    SELECT crypt(%s, %s) = %s
                """
                cursor.execute(query, [contrasenaActual, user.contrasena, user.contrasena])

                resultado = cursor.fetchone()
            
            if resultado[0]:
                if nuevaContrasena==confirmarNuevaContrasena:
                    contrasenaCifrada = encrypt_password(nuevaContrasena)
                    user.contrasena=contrasenaCifrada
                    user.cambiocontrasena=False
                    request.session['cambiocontrasena']=False
                    user.save()
                    messages.success(request, 'Contraseña cambiada exitosamente!')
                    return redirect('inicio')  # Redirect to the login page after logout
                else:
                    messages.error(request, 'Las contraseñas no coinciden')
                    return redirect('change_password')
            else:
                messages.error(request, 'Contraseña actual incorrecta')
                return redirect('change_password')

        except clsUsuarios.DoesNotExist:
            messages.error(f"No se encontro el usuario al que se le va a cambiar la contraseña")

        except Exception as e:
            messages.error(request, f"Error durante cambio de contraseña")
    
    return render(request, 'change_password.html')
# -----------------------------------------------------------------------------------------------------------------
@require_POST
def mark_notifications_as_read(request):
    # Marca todas las notificaciones no leídas como leídas
    Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
    return JsonResponse({'success': True})


# -----------------------------------------------------------------------------------------------------------------
@require_POST
def mark_notification_as_read(request):
    import json
    data = json.loads(request.body)
    notification_id = data.get('id')
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.unread = False
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


