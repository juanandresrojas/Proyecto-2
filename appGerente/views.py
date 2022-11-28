from django.shortcuts import render
from multiprocessing import context
from .models import *
from appAdmin.models import *
from appUsuario.models import *
from django.http import JsonResponse
import json


# Create your views here.
def editarCultivos(request):
    # consultar cultivos
    regFinca = request.user.Finca

    # consultar los datos
    listaLotes = Lote.objects.filter(finca=regFinca).values()
    listaCultivos = Cultivo.objects.all().values('id', 'observacCultivo').values()
    listaProductos = Producto.objects.filter(finca=regFinca).values()
    listaMedidas = UnidadMedida.objects.all().values(
        'id', 'descripUnidadMedida').values()

    # Armar context
    context = {
        'titulo': 'Cultivos',
        'nombreForm': 'Consultar y Editar Cultivos',
        'ruta': 'cultivos',
        'listaCultivos': listaCultivos,
        'listaLotes': listaLotes,
        'listaProductos': listaProductos,
        'listaMedidas': listaMedidas,

    }

    # Armar retorno
    return render(request, 'administradorForm/cultivosForm.html', context)
# ******************************************************************************************************************


def editarLotes(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    conjuntoLotes = Lote.objects.filter(finca=regFinca).values(
        'id', 'descripLote', 'unidadMedida__id')
    listaMedidas = UnidadMedida.objects.all().values('id', 'descripUnidadMedida')

    # Armar context
    context = {
        'titulo': 'Lotes',
        'nombreForm': 'Consultar y Editar Lotes',
        'ruta': 'lotes',
        'conjuntoLotes': conjuntoLotes,
        'listaMedidas': listaMedidas,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regLote = Lote.objects.get(id=id)
            # Respuesta JSON
            data = {
                # 'listaLotes': regLote.listaLotes,
                'observacLote': regLote.observacLote,
                'unidadMedida': regLote.unidadMedida.id,
                'descripLote': regLote.descripLote,
                'areaLote': regLote.areaLote,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['conjuntoLotes'])
        observacLote = request.POST['observacLote']
        listaMedidas = int(request.POST['listaMedidas'])
        descripLote = request.POST['descripLote']
        areaLote = request.POST['areaLote']

        if len(observacLote) > 0 and len(descripLote) > 0 and len(areaLote) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = Lote.objects.filter(id=id).exists()
                if existe:
                    regUnidad = UnidadMedida.objects.get(id=listaMedidas)
                    regLote = Lote.objects.get(id=id)
                    regLote.unidadMedida = regUnidad
                    regLote.observacLote = observacLote
                    regLote.descripLote = descripLote
                    regLote.areaLote = areaLote
                    regLote.finca = regFinca
                    regLote.save()
                    context['mensaje'] = 'Lote modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regUnidad = UnidadMedida.objects.get(id=listaMedidas)
                regLote = Lote(unidadMedida=regUnidad, observacLote=observacLote,
                               descripLote=descripLote, areaLote=areaLote, finca=regFinca)
                regLote.save()
                context['mensaje'] = 'Lote creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'asistenteForm/lotesForm.html', context)

# *****************************************************************************************************************


def editarTrabajador(request):
    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaTrabajadores = Trabajador.objects.filter(finca=regFinca).values()

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Trabajadores',
        'ruta': 'trabajadores',
        'nombreForm': 'Editar y consultar trabajadores',
        'ruta': 'trabajadores',
        'listaTrabajadores': listaTrabajadores

    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regtrabajador = Trabajador.objects.get(id=id)
            # Respuesta JSON
            data = {
                'nombreTrabajador': regtrabajador.nombreTrabajador,
                'telefonoTrabajador': regtrabajador.telefonoTrabajador,
                'nitTrabajador': regtrabajador.nitTrabajador,
                'emailTrabajador': regtrabajador.emailTrabajador,
                'costoHoraTrabajador': regtrabajador.costoHoraTrabajador,
                'rol': regtrabajador.rol,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        id = int(request.POST['listaTrabajador'])
        nombreTrabajador = request.POST['nombreTrabajador']
        telefonoTrabajador = request.POST['telefonoTrabajador']
        nitTrabajador = request.POST['nitTrabajador']
        emailTrabajador = request.POST['emailTrabajador']
        costoHoraTrabajador = request.POST['costoHoraTrabajador']
        rol = request.POST['rol']
        if len(nombreTrabajador) > 0 and len(telefonoTrabajador) > 0 and len(nitTrabajador) > 0 and len(emailTrabajador) > 0 and len(costoHoraTrabajador) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = Trabajador.objects.filter(id=id).exists()
                if existe:
                    regtrabajador = Trabajador.objects.get(id=id)
                    regtrabajador.nombreTrabajador = nombreTrabajador
                    regtrabajador.telefonoTrabajador = telefonoTrabajador
                    regtrabajador.nitTrabajador = nitTrabajador
                    regtrabajador.emailTrabajador = emailTrabajador
                    regtrabajador.costoHoraTrabajador = costoHoraTrabajador
                    regtrabajador.rol = rol
                    regtrabajador.finca = regFinca
                    regtrabajador.save()
                    context['mensaje'] = 'Trabajador modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                # CREAR REGISTRO
                regtrabajador = Trabajador(nombreTrabajador=nombreTrabajador, nitTrabajador=nitTrabajador, telefonoTrabajador=telefonoTrabajador,
                                           emailTrabajador=emailTrabajador, costoHoraTrabajador=costoHoraTrabajador, rol=rol, finca=regFinca,)
                regtrabajador.save()
                context['mensaje'] = 'Trabajador creado'
        else:
            context['alarma'] = 'Debe de diligenciar todos los datos'
    # -- en cualquier caso...
    # context['form'] = TrabajadorForm()
    return render(request, 'administradorForm/trabajadoresForm.html', context)

# *****************************************************************************************************************


def editarEquipoFinca(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    listaEquipoFinca = EquipoFinca.objects.filter(finca=regFinca).values(
        'id', 'existenciaEquipo')

    # Armar context
    context = {
        'titulo': 'Equipo de Finca',
        'nombreForm': 'Consultar y Editar Equipo de Finca',
        'ruta': 'equipoFinca',
        'listaEquipoFinca': listaEquipoFinca
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regEquipoFinca = EquipoFinca.objects.get(id=id)
            # Respuesta JSON
            data = {
                # 'listaLotes': regLote.listaLotes,
                'existenciaEquipo': regEquipoFinca.existenciaEquipo,
                'valorUnitarioEquipo': regEquipoFinca.valorUnitarioEquipo,
                'deprecEquipo': regEquipoFinca.deprecEquipo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['listaEquipoFinca'])
        existenciaEquipo = request.POST['existenciaEquipo']
        valorUnitarioEquipo = request.POST['valorUnitarioEquipo']
        deprecEquipo = request.POST['deprecEquipo']

        if len(existenciaEquipo) > 0 and len(valorUnitarioEquipo) > 0 and len(deprecEquipo) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = EquipoFinca.objects.filter(id=id).exists()
                if existe:
                    regEquipo = Equipo.objects.get(id=id)
                    regEquipoFinca = EquipoFinca.objects.get(id=id)
                    regEquipoFinca.existenciaEquipo = existenciaEquipo
                    regEquipoFinca.valorUnitarioEquipo = valorUnitarioEquipo
                    regEquipoFinca.deprecEquipo = deprecEquipo
                    regEquipoFinca.finca = regFinca
                    regEquipoFinca.equipo = regEquipo
                    regEquipoFinca.save()
                    context['mensaje'] = 'Equipo modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regEquipoFinca = EquipoFinca(existenciaEquipo=existenciaEquipo,
                                             valorUnitarioEquipo=valorUnitarioEquipo,
                                             deprecEquipo=deprecEquipo, finca=regFinca,
                                             equipo=regEquipo)
                regEquipoFinca.save()
                context['mensaje'] = 'Equipo de finca creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'administradorForm/equipoFincaForm.html', context)

# *****************************************************************************************************************


def editarIndirectos(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    listaIndirectos = Indirecto.objects.filter(finca=regFinca).values(
        'id', 'observacPago')

    # Armar context
    context = {
        'titulo': 'Costos Indirectos',
        'nombreForm': 'Consultar y Editar Costos Indirectos',
        'ruta': 'indirectos',
        'listaIndirectos': listaIndirectos
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE INDIRECTO
            regIndirecto = Indirecto.objects.get(id=id)
            # Respuesta JSON
            data = {
                'fechaPago': regIndirecto.fechaPago,
                'numFactura': regIndirecto.numFactura,
                'observacPago': regIndirecto.observacPago,
                'valorPagado': regIndirecto.valorPagado,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['listaIndirectos'])
        fechaPago = request.POST['fechaPago']
        numFactura = request.POST['numFactura']
        observacPago = request.POST['observacPago']
        valorPagado = request.POST['valorPagado']

        if len(fechaPago) > 0 and len(numFactura) > 0 and len(observacPago) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = Indirecto.objects.filter(id=id).exists()
                if existe:
                    regEquipoFinca = Indirecto.objects.get(id=id)
                    regEquipoFinca.fechaPago = fechaPago
                    regEquipoFinca.numFactura = numFactura
                    regEquipoFinca.observacPago = observacPago
                    regEquipoFinca.valorPagado = valorPagado
                    regEquipoFinca.finca = regFinca
                    regEquipoFinca.save()
                    context['mensaje'] = 'Pago indirecto modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regEquipoFinca = Indirecto(fechaPago=fechaPago,
                                           numFactura=numFactura,
                                           observacPago=observacPago, finca=regFinca,
                                           valorPagado=valorPagado)
                regEquipoFinca.save()
                context['mensaje'] = 'Pago indirecto creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'administradorForm/indirectosForm.html', context)
