from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from notifications.models import Notification
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from utils.decorators import permisosRequeridos
from django.http import JsonResponse
import os
from django.conf import settings
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import clsProductos


from .forms import frmProductos
# Importamos modulos y librerias necesarias para el paginador utilizado
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger('django')

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
    page = int(request.GET.get('page', 1))
    productos = clsProductos.objects.all().order_by('idproducto')

    # Filtros acumulables
    tipoproducto = [f for f in request.GET.getlist('tipoproducto') if f.strip()]
    if tipoproducto:
        productos = productos.filter(tipoproducto__in=tipoproducto)

    color = [f for f in request.GET.getlist('color') if f.strip()]
    if color:
        productos = productos.filter(color__in=color)

    precioxm = [f for f in request.GET.getlist('precioxm') if f.strip()]
    if precioxm:
        productos = productos.filter(precioxm__in=precioxm)

    request.session['productosFiltradas'] = list(
        productos.values_list('idproducto', flat=True)
    )

    paginator = Paginator(productos, 15)
    page_obj = paginator.get_page(page)

    productos_list = []

    for producto in page_obj.object_list:
        producto_dict = {
            'idproducto': producto.idproducto,
            'tipoproducto': producto.tipoproducto,
            'nombre': producto.nombre,
            'color': producto.color,
            'descripcion': producto.descripcion,
            'precio': producto.precio,
            'precioxm': producto.precioxm,
            'stock': producto.stock,
            'fotos': []
        }

        # 📁 Ruta física en el servidor
        carpeta_fotos = os.path.join(settings.MEDIA_ROOT, str(producto.idproducto))

        if os.path.isdir(carpeta_fotos):
            archivos = os.listdir(carpeta_fotos)
            for archivo in archivos:
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    # URL pública para el navegador
                    url = f"{settings.MEDIA_URL}{producto.idproducto}/{archivo}"
                    producto_dict['fotos'].append(url)

        productos_list.append(producto_dict)

    return JsonResponse({
        'datos': productos_list,
        'total': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


    # @permisosRequeridos('appTSM.view_clsactivostipendientes')
def productosPublico(request):
    tipoproducto = list(clsProductos.objects.values_list("tipoproducto", flat=True).distinct())
    color = list(clsProductos.objects.values_list("color", flat=True).distinct())
    precioxm = list(clsProductos.objects.values_list("precioxm", flat=True).distinct())

    filtros = {
        'tipoproductos': tipoproducto,
        'colores': color,
        'precioxms': precioxm,
    }
    return render(request, 'productos/productoscliente.html', filtros)


# @permisosRequeridos('appTSM.add_clsproductos')
def crearProducto(request):
    if request.method == 'POST':
        formulario = frmProductos(request.POST, request.FILES)
        if formulario.is_valid():
            try:
                # Guardar primero el producto
                producto = formulario.save()

                # Crear carpeta en media con el idproducto
                ruta_producto = os.path.join(
                    settings.MEDIA_ROOT,
                    str(producto.idproducto)
                )

                os.makedirs(ruta_producto, exist_ok=True)

                # 3️⃣ Obtener imágenes del formulario
                imagenes = request.FILES.getlist('imagenes')

                for img in imagenes:
                    # Validación extra (seguridad)
                    if not img.content_type.startswith('image/'):
                        continue

                    # Ruta final del archivo
                    ruta_archivo = os.path.join(
                        str(producto.idproducto),
                        img.name
                    )

                    # Guardar archivo
                    default_storage.save(
                        ruta_archivo,
                        ContentFile(img.read())
                    )

                messages.success(request, 'Producto creado correctamente.')
                return redirect('productos')

            except Exception as e:
                messages.error(request, f'Error al intentar crear el producto: {str(e)}')
                logger.error("Error al crear producto: %s", str(e))

        else:
            messages.error(request, 'Formulario no válido.')
    else:
        formulario = frmProductos()

    context = {
        'form': formulario
    }

    return render(request, 'productos/crearProductos.html', context)


# @permisosRequeridos('appTSM.change_clsproductos')
def editarProducto(request, idproducto):

    producto = get_object_or_404(clsProductos, idproducto=idproducto)

    # 📁 Ruta de la carpeta del producto
    ruta_producto = os.path.join(
        settings.MEDIA_ROOT,
        str(producto.idproducto)
    )

    os.makedirs(ruta_producto, exist_ok=True)

    # 📷 Listar imágenes existentes
    imagenes_existentes = []
    if os.path.exists(ruta_producto):
        imagenes_existentes = [
            f"{producto.idproducto}/{archivo}"
            for archivo in os.listdir(ruta_producto)
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]

    if request.method == 'POST':
        formulario = frmProductos(
            request.POST,
            request.FILES,
            instance=producto
        )

        if formulario.is_valid():
            try:
                # 1️⃣ Guardar cambios del producto
                formulario.save()

                # 2️⃣ Guardar nuevas imágenes (si llegan)
                imagenes = request.FILES.getlist('imagenes')

                for img in imagenes:
                    if not img.content_type.startswith('image/'):
                        continue

                    ruta_archivo = os.path.join(
                        str(producto.idproducto),
                        img.name
                    )

                    default_storage.save(
                        ruta_archivo,
                        ContentFile(img.read())
                    )

                messages.success(request, 'Producto actualizado correctamente.')
                return redirect('productos')

            except Exception as e:
                messages.error(request, f'Error al actualizar el producto: {str(e)}')
                logger.error("Error al editar producto", exc_info=True)

        else:
            messages.error(request, 'Formulario no válido.')

    else:
        formulario = frmProductos(instance=producto)

    context = {
        'form': formulario,
        'producto': producto,
        'imagenes': imagenes_existentes
    }

    return render(request, 'productos/crearProductos.html', context)