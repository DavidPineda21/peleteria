from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')


def inicio(request):
    messages.success(request, 'espacio desactivado correctamente.')
    return render(request, 'inicio.html')