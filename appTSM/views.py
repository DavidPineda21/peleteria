from django.shortcuts import render
from django.contrib import messages
from notifications.models import Notification
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def inicio(request):
    try:
        User = get_user_model()
        grupo = Group.objects.get(name="administrador")
        usuariosDjango = grupo.user_set.all()
        nombreUsuario = request.session.get('nombre')
        for user in usuariosDjango:
            Notification.objects.create(
            recipient=user,
            actor=request.user,
            verb="",
            description=f"{nombreUsuario} ha realizado una nueva solicitud de equipos, Haga clic aquí para verla",
            data={"url": reverse("index")}
        )

        
    except User.DoesNotExist:
        print("ERROR: User not found in the database.")
    messages.success(request, 'espacio desactivado correctamente.')
    return render(request, 'inicio.html')