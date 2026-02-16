from django.urls import path
from . import views

urlpatterns = [

# URLS DE INICIO DE LA APLICACION
# --------------------------------------------------------
    path('',views.index, name='index'),
    path('inicio',views.inicio, name='inicio'),
    path('productos',views.productos,name='productos'),
    path('productoscliente',views.productosPublico,name='productosPublico'),
    path('productos/api/',views.productos_api,name='productos_api'),
    path('productos/crear',views.crearProducto,name='crearProducto'),
    path('productos/editar/<str:idproducto>',views.editarProducto,name='editarProducto'),
    path('productos/<int:idproducto>/eliminar-imagen/<str:nombre>',views.eliminarImagenProducto,name='eliminarImagenProducto'),
    path('registrarVenta', views.registrarVenta, name='registrarVenta'),
    path('buscar-producto/', views.buscarProductoPorCodigo, name='buscarProducto'),
    path('imprimir-venta/<int:venta_id>/', views.imprimirVenta, name='imprimirVenta'),

]