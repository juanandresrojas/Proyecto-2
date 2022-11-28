from django.urls import path
from . import views

urlpatterns = [
    path('lotes/', views.editarLotes, name="lotes"),
    path('cultivos/', views.editarCultivos, name='cultivos'),
    path('trabajadores/', views.editarTrabajador, name='trabajadores'),
    path('equipoFinca/', views.editarEquipoFinca, name='equipoFinca'),
    path('indirectos/', views.editarIndirectos, name='indirectos'),
   
]