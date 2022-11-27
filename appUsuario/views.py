from ast import Return
from asyncio.windows_events import NULL
from genericpath import exists
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from appGerente.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# Create your views here.
# ******** CONTROL DE REGISTRO DE USUARIOS  *******************************************************


def registrarse(request):
    '''
    Funcion para registrar o verificar usuarios
    '''

    context = {
        "titulo": "Registro"
    }

    if request.method == 'POST':
        tipoUsuario = request.POST['tipoUsuario']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        phone_number = request.POST['phone_number']
        user = NULL
        # VALIDACION DE CAMPOS
        ok = True
        if not email:
            context['alarma'] = 'Ingrese el correo electronico'
            ok = False

        if not password or len(password) < 5:
            context['alarma'] = 'Ingrese un password de 5 o mas caracteres'
            ok = False

        if password != confirmPassword:
            context['alarma'] = '¡ El password no coincide !'
            ok = False

        if ok and tipoUsuario == '2':
            existe = Finca.objects.filter(correoGerente=email).exists()
            if not existe:
                context['alarma'] = 'El correo no esta registrado'
            else:
                existe = Account.objects.filter(email=email).exists()

                if not existe:
                    # CREAR USUARIO
                    regGerente = Finca.objects.get(correoGerente=email)
                    username = email.split('@')[0]
                    user = Account.objects.create_user(first_name=regGerente.nombreGerente,
                                                       last_name=regGerente.apellidoGerente, username=username, email=email, password=password)
                    user.phone_number = phone_number
                    user.Finca = regGerente
                    user.rol = '2'
                    user.is_active = True
                    user.save()
                    context['mensaje'] = 'Gerente registrado con exito'
                else:
                    context['mensaje'] = 'El usuario no esta registrado o no es gerente de finca'

        elif tipoUsuario == '3':
            # Asistente de finca, buscar
            existe = Trabajador.objects.filter(
                emailTrabajador=email, rol='3').exists()
            if not existe:
                context['alarma'] = 'El correo del trabajador no esta registrado'
            else:
                existe = Account.objects.filter(email=email).exists()
                if not existe:
                    # CREAR USUARIO
                    regTrabajador = Trabajador.objects.get(
                        emailTrabajador=email)
                    # Buscar la finca
                    username = email.split('@')[0]
                    regFinca = regTrabajador.Finca
                    user = Account.objects.create_user(
                        first_name=regTrabajador.nombreTrabajador, last_name=regTrabajador.nombreTrabajador, email=email, username=username, password=password)
                    user.phone_number = phone_number
                    user.Finca = regFinca
                    user.rol = '3'
                    user.is_active = True
                    user.save()
                    context['mensaje'] = 'Asistente registrado con exito!'
                    # return redirect('ingresar')
                else:
                    context['alarma'] = 'El usuario ya esta registrado'
        else:
            context['alarma'] = 'Registro no permitido'

    return render(request, 'usuarios/registro.html', context)


# ******** CONTROL DE INGRESO DE USUARIOS  *******************************************************
def ingresar(request):
    '''
    Funcion para ingresar el usuario 
    '''
    context = {
        "titulo": "Ingresar"
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if not user:
            context['alarma'] = 'Su correo no se encuentra en la base de datos o contraseña incorrecta!!'
            return render(request, 'usuarios/ingresar.html', context)
        else:
            context['mensaje'] = 'Inicio sesión con exito !!'
            auth.login(request, user)
            return render(request, 'home.html', context)
    else:
        return render(request, 'usuarios/ingresar.html', context)


# ******** CONTROL DE SALIDA DE USUARIOS  *******************************************************
@login_required(login_url='http://localhost:8000/usuarios/ingresar/')
def salir(request):
    '''
    Funcion para que el usuario salga de sesión 
    '''
    context = {
        "titulo": "Salida"
    }
    auth.logout(request)
    return render(request, 'usuarios/salir.html', context)
