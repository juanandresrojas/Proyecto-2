from django.urls import path
from . import views

urlpatterns = [
    path('lotes/', views.editarLotes, name="lotes"),
    path('cultivos/', views.editarCultivos, name='cultivos'),
    path('trabajadores/', views.editarTrabajador, name='trabajadores'),
    path('equipoFinca/', views.editarEquipoFinca, name='equipoFinca'),
    path('indirectos/', views.editarIndirectos, name='indirectos'),
    path('insumoFinca/', views.editarInsumoFinca, name='insumoFinca'),
    path('productos/', views.editarProductos, name='productos'),
    path('clientes/', views.editarClientes, name='clientes'),
    path('compraEquipo/', views.editarCompraEquipo, name='compraEquipo'),
   
]