from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.registrarse, name="registro"),
    path('ingresar/', views.ingresar, name="ingresar"),
    path('salir/', views.salir, name="salir"),
]

   