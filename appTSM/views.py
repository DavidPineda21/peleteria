from django.shortcuts import render
from django.contrib import messages
from notifications.models import Notification
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from utils.decorators import permisosRequeridos
from django.http import JsonResponse

from .models import clsProductos

# Importamos modulos y librerias necesarias para el paginador utilizado
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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



# @permisosRequeridos('appTSM.view_clsactivostipendientes')
def productos(request):
    tipoproducto = list(clsProductos.objects.values_list("tipoproducto", flat=True).distinct())
    color = list(clsProductos.objects.values_list("color", flat=True).distinct())
    precioxm = list(clsProductos.objects.values_list("precioxm", flat=True).distinct())

    filtros = {
        'tipoproductos': tipoproducto,
        'colores': color,
        'precioxms': precioxm,
    }
    return render(request, 'productos/productos.html', filtros)

# @permisosRequeridos('appTSM.view_clsactivostipendientes')
def productos_api(request):
    page = int (request.GET.get('page', 1))
    productos = clsProductos.objects.all().order_by('idproducto')

    # Filtros acumulables

    tipoproducto = [f for f in request.GET.getlist('tipoproducto') if f.strip()] # limpia vacíos
    if tipoproducto:
        productos = productos.filter(tipoproducto__in=tipoproducto)
    color = [f for f in request.GET.getlist('color') if f.strip()] # limpia vacíos
    if color:
        productos = productos.filter(color__in=color)
    precioxm = [f for f in request.GET.getlist('precioxm') if f.strip()] # limpia vacíos
    if precioxm:
        productos = productos.filter(precioxm__in=precioxm)

    


    request.session['productosFiltradas'] = list(productos.values_list('idproducto', flat=True))

    paginator = Paginator(productos, 15)
    page_obj = paginator.get_page(page)

    data = list(page_obj.object_list.values(
        'idproducto',
        'tipoproducto',
        'nombre',
        'color',
        'descripcion',
        'precio',
        'precioxm',
        'stock',
    ))

    return JsonResponse({
        'datos': data,
        'total': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })