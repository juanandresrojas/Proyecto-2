"""ProyectoJuan2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from . import views 

# PARA CAMBIAR TITULOS EN MODULO DE DJANGO
admin.site.site_header = 'Sistema Evaluador de Costos para Mypimes Agricolas - módulo Administrativo '
admin.site.index_title = 'Modulos y Tablas '  # DEFAULT:" Site Administration"
admin.site.site_title = 'HTML title from administration'  #DEFAULT: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('usuarios/', include('appUsuario.urls')),
    path('gerentes/', include('appGerente.urls')),
    path('administracion/', include('appAdmin.urls')),
]
