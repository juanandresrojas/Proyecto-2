from django.contrib import admin
from django.urls import path
from . import views
from.forms import *

urlpatterns = [
    path('horas/', views.editarHoras, name="categHoras"),
    path('hora/', views.consultarHora),
    # *************************************************************
    path('materiales/', views.editarMateriales, name="categMaterial" ),
    path('material/', views.consultarMaterial),
    # *************************************************************
    path('proveedores/', views.editarProvedores, name="proveedor"),
    path('proveedor/', views.consultarProveedor),
    # *************************************************************
    path('medidas/', views.editarMedida, name="unidadMedida"),
    path('medida/', views.consultarMedida),
    # *************************************************************
    path('equipos/', views.editarEquipos, name="equipos"),

    # *************************************************************
    path('insumos/', views.editarInsumos, name="insumos"),

    # *************************************************************


]