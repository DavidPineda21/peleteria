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
import os
from barcode import Code128
from barcode.writer import ImageWriter
from django.db import transaction
from django.template.loader import render_to_string

from .models import clsProductos
from .models import clsVentas
from .models import clsDetalleVenta
from appBase.models import clsUsuarios


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
        # for user in usuariosDjango:
        #     Notification.objects.create(
        #     recipient=user,
        #     actor=request.user,
        #     verb="",
        #     description=f"{nombreUsuario} ha realizado una nueva solicitud de equipos, Haga clic aquí para verla",
        #     data={"url": reverse("index")}
        # )

        
    except User.DoesNotExist:
        print("ERROR: User not found in the database.")
    return render(request, 'inicio.html')



# @login_required
@permisosRequeridos('appTSM.view_clsproductos')
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
    if request.user.groups.filter(name__in=['administrador']).exists():
        productos = clsProductos.objects.all().order_by('idproducto')
    else:
        productos = clsProductos.objects.filter(stock__gt=0).order_by('idproducto')

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

    paginator = Paginator(productos, 4)
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
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and 'barcode' not in archivo.lower():
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


@permisosRequeridos('appTSM.add_clsproductos')
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

                # 3️⃣ Generar código de barras
                codigo = Code128(
                    str(producto.idproducto),
                    writer=ImageWriter()
                )

                ruta_barcode = os.path.join(
                    ruta_producto,
                    f'barcode_{producto.idproducto}'
                )

                codigo.save(
                    ruta_barcode,
                    {
                        'module_width': 0.2,
                        'module_height': 15,
                        'font_size': 10,
                        'text_distance': 5,
                        'quiet_zone': 6,
                    }
                )

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
                return redirect('productosPublico')

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


@permisosRequeridos('appTSM.change_clsproductos')
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
        for archivo in os.listdir(ruta_producto):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                imagenes_existentes.append({
                    'url': f"{settings.MEDIA_URL}{producto.idproducto}/{archivo}",
                    'nombre': archivo
                })

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
                return redirect('productosPublico')

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
        'imagenes': imagenes_existentes,
        'MEDIA_URL': settings.MEDIA_URL,  # 👈 CLAVE
    }

    return render(request, 'productos/crearProductos.html', context)


@permisosRequeridos('appTSM.change_clsproductos')
def eliminarImagenProducto(request, idproducto, nombre):

    ruta_imagen = os.path.join(
        settings.MEDIA_ROOT,
        str(idproducto),
        nombre
    )

    try:
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
            messages.success(request, 'Imagen eliminada correctamente.')
        else:
            messages.error(request, 'La imagen no existe.')

    except Exception as e:
        messages.error(request, f'Error al eliminar la imagen: {str(e)}')

    return redirect('editarProducto', idproducto=idproducto)


@permisosRequeridos('appTSM.add_clsventas')
def buscarProductoPorCodigo(request):
    codigo = request.GET.get('codigo')

    try:
        producto = clsProductos.objects.get(idproducto=codigo)

        return JsonResponse({
            "id": producto.idproducto,
            "nombre": producto.nombre,
            "precio": float(producto.precio or 0),
            "stock": producto.stock or 0
        })

    except clsProductos.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"})


@permisosRequeridos('appTSM.add_clsventas')
@transaction.atomic
def registrarVenta(request):

    if request.method == "POST":
        try:
            usuario = get_object_or_404(
                clsUsuarios,
                idusuario=request.user.username
            )

            productos = request.POST.getlist('producto_id[]')
            cantidades = request.POST.getlist('cantidad[]')

            productos_obj = []
            total_venta = 0

            for producto_id, cantidad in zip(productos, cantidades):

                producto = clsProductos.objects.select_for_update().get(
                    idproducto=producto_id
                )

                cantidad = int(cantidad)

                if (producto.stock or 0) < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre}"
                    )

                productos_obj.append((producto, cantidad))

            venta = clsVentas.objects.create(idusuario=usuario)

            for producto, cantidad in productos_obj:

                precio = producto.precio or 0
                subtotal = precio * cantidad

                clsDetalleVenta.objects.create(
                    idventa=venta,
                    idproducto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal
                )

                producto.stock -= cantidad
                producto.save()

                total_venta += subtotal

            venta.total = total_venta
            venta.save()
            messages.success(request, 'Venta registrada correctamente.')

            # 🔥 Renderizamos el ticket como string
            detalles = clsDetalleVenta.objects.filter(idventa=venta)

            ticket_html = render_to_string(
                "ventas/ticket.html",
                {
                    "venta": venta,
                    "detalles": detalles
                }
            )

            return JsonResponse({
                "success": True,
                "ticket": ticket_html
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return render(request, "ventas/RegistrarVenta.html")

def imprimirVenta(request, venta_id):

    venta = get_object_or_404(clsVentas, idventa=venta_id)
    detalles = clsDetalleVenta.objects.filter(idventa=venta)

    return render(request, "ventas/ticket.html", {
        "venta": venta,
        "detalles": detalles
    })