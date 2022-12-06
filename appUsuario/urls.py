from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('registro/', views.registrarse, name="registro"),
    path('ingresar/', views.ingresar, name="ingresar"),
    path('salir/', views.salir, name="salir"),

    #****************************************************************************************************************
    path('reset/password_reset', auth_views.PasswordResetView.as_view(template_name='usuarios/cambiar_contraseña.html', email_template_name='usuarios/cambiar_contraseña_correo.html'), name="password_reset"),
    path('reset/password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/cambiar_contraseña_mensaje.html'), name="password_reset_done"),
    path('reset/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/cambiar_contraseña_confirmar.html'), name='password_reset_confirm'),
    path('reset/password_reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/cambiar_contraseña_completado.html'), name='password_reset_complete'),
]

    