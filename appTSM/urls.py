from django.urls import path
from . import views

urlpatterns = [

# URLS DE INICIO DE LA APLICACION
# --------------------------------------------------------
    path('',views.index, name='index'),
    path('inicio',views.inicio, name='inicio'),

]