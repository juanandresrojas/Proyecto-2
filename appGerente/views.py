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
    listaLotes = Lote.objects.filter(finca=regFinca)
    listaCultivos = Cultivo.objects.prefetch_related('lote').filter(lote__finca=regFinca).values('id', 'observacCultivo', 'lote__id', 'unidadMedida__id', 'producto__id')
    listaProductos = Producto.objects.filter(finca=regFinca)
    listaMedidas = UnidadMedida.objects.all()
    context = {
        'titulo': 'Cultivos',
        'nombreForm': 'Consultar y Editar Cultivos',
        'ruta': 'cultivos',
        'listaCultivos': listaCultivos,
        'listaLotes': listaLotes,
        'listaProductos': listaProductos,
        'listaMedidas': listaMedidas,

    }
        # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE CULTIVO
            regCultivo = Cultivo.objects.get(id=id)
            # Respuesta JSON
            data = {
                'lote': regCultivo.lote.id,
                'unidadMedida': regCultivo.unidadMedida.id,
                'producto': regCultivo.producto.id,
                'fechaSiembra': regCultivo.fechaSiembra,
                'fechaCosecha': regCultivo.fechaCosecha,
                'cantidadCosecha': regCultivo.cantidadCosecha,
                'observacCultivo': regCultivo.observacCultivo,
                'activo': regCultivo.activo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaCultivo = int(request.POST['listaCultivos'])
        listaLotes = int(request.POST['listaLotes'])  # ID del lote
        listaProductos = int(request.POST['listaProductos'])  # ID del producto
        listaMedidas = int(request.POST['listaMedidas'])  # ID de medidas
        activo = bool(request.POST['activo'])
        fechaSiembra = request.POST['fechaSiembra']
        fechaCosecha = request.POST['fechaCosecha']
        cantidadCosecha = request.POST['cantidadCosecha']
        observacCultivo = request.POST['observacCultivo']

        regLote = Lote.objects.get(id=listaLotes)
        regProducto = Producto.objects.get(id=listaProductos)
        regMedidas = UnidadMedida.objects.get(id=listaMedidas)

        # SI cultivo == 0, entonces crear 
        if listaCultivo == 0:
            regCultivo = Cultivo(lote=regLote, producto=regProducto, activo=activo, unidadMedida=regMedidas, fechaSiembra=fechaSiembra,
                                 fechaCosecha=fechaCosecha, cantidadCosecha=cantidadCosecha, observacCultivo=observacCultivo)
            context['mensaje'] = 'Cultivo creado'
            regCultivo.save()
        else:
            # sino, modifica 
            regCultivo = Cultivo.objects.get(id=listaCultivo)
            regCultivo.lote = regLote
            regCultivo.producto = regProducto
            regCultivo.activo = activo
            regCultivo.unidadMedida = regMedidas
            regCultivo.fechaSiembra = fechaSiembra
            regCultivo.fechaCosecha = fechaCosecha
            regCultivo.cantidadCosecha = cantidadCosecha
            regCultivo.observacCultivo = observacCultivo
            context['mensaje'] = 'Cultivo modificado'
            regCultivo.save()

    # Armar retorno
    return render(request, 'gerenteForm/cultivosForm.html', context)
# ******************************************************************************************************************

def editarLotes(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    conjuntoLotes = Lote.objects.filter(finca=regFinca).values('id', 'descripLote', 'unidadMedida__id')
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
    return render(request, 'gerenteForm/trabajadoresForm.html', context)

# *****************************************************************************************************************

def editarEquipoFinca(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    listaEquipoFinca = EquipoFinca.objects.filter(finca=regFinca).values('id', 'descripEquipoFinca', 'equipo__id')
    listaEquipos = Equipo.objects.all().values('id', 'descripEquipo')

    # Armar context
    context = {
        'titulo': 'Equipo de Finca',
        'nombreForm': 'Consultar y Editar Equipo de Finca',
        'ruta': 'equipoFinca',
        'listaEquipoFinca': listaEquipoFinca,
        'listaEquipos': listaEquipos,
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
                'descripEquipoFinca': regEquipoFinca.descripEquipoFinca,
                'equipo': regEquipoFinca.equipo.id,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['listaEquipoFinca'])
        listaEquipos = int(request.POST['listaEquipos'])
        existenciaEquipo = request.POST['existenciaEquipo']
        valorUnitarioEquipo = request.POST['valorUnitarioEquipo']
        deprecEquipo = request.POST['deprecEquipo']
        descripEquipoFinca= request.POST['descripEquipoFinca']

        if len(existenciaEquipo) > 0 and len(valorUnitarioEquipo) > 0 and len(deprecEquipo) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = EquipoFinca.objects.filter(id=id).exists()
                if existe:
                    regEquipo = Equipo.objects.get(id=listaEquipos)
                    regEquipoFinca = EquipoFinca.objects.get(id=id)
                    regEquipoFinca.existenciaEquipo = existenciaEquipo
                    regEquipoFinca.valorUnitarioEquipo = valorUnitarioEquipo
                    regEquipoFinca.deprecEquipo = deprecEquipo
                    regEquipoFinca.descripEquipoFinca = descripEquipoFinca
                    regEquipoFinca.finca = regFinca
                    regEquipoFinca.equipo = regEquipo
                    regEquipoFinca.save()
                    context['mensaje'] = 'Equipo modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regEquipo = Equipo.objects.get(id=listaEquipos)
                regEquipoFinca = EquipoFinca(existenciaEquipo=existenciaEquipo,
                                             equipo=regEquipo,
                                             valorUnitarioEquipo=valorUnitarioEquipo,
                                             deprecEquipo=deprecEquipo, finca=regFinca, descripEquipoFinca=descripEquipoFinca)
                regEquipoFinca.save()
                context['mensaje'] = 'Equipo de finca creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'gerenteForm/equipoFincaForm.html', context)

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
    return render(request, 'gerenteForm/indirectosForm.html', context)

#*****************************************************************************************************************

def editarInsumoFinca(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    listaInsumosFinca = InsumoFinca.objects.filter(finca=regFinca).values('id', 'descripInsumoFinca', 'insumo__id', 'unidadmedida__id')
    listaInsumos = Insumo.objects.all().values('id', 'descripInsumo')
    listaUnidades = UnidadMedida.objects.all().values('id', 'descripUnidadMedida')

    # Armar context
    context = {
        'titulo': 'Insumo de Finca',
        'nombreForm': 'Consultar y Editar Equipo de Finca',
        'ruta': 'insumoFinca',
        'listaInsumosFinca': listaInsumosFinca,
        'listaInsumos': listaInsumos,
        'listaUnidades': listaUnidades,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE INSUMO
            regInsumoFinca = InsumoFinca.objects.get(id=id)
            # Respuesta JSON
            data = {
                'insumo': regInsumoFinca.insumo.id,
                'unidadmedida': regInsumoFinca.unidadmedida.id,
                'existenciaInsumo': regInsumoFinca.existenciaInsumo,
                'valorUnitarioInsumo': regInsumoFinca.valorUnitarioInsumo,
                'descripInsumoFinca': regInsumoFinca.descripInsumoFinca,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['listaInsumosFinca'])
        listaInsumos = int(request.POST['listaInsumos'])
        listaUnidades = int(request.POST['listaUnidades'])
        existenciaInsumo = request.POST['existenciaInsumo']
        valorUnitarioInsumo = request.POST['valorUnitarioInsumo']
        descripInsumoFinca= request.POST['descripInsumoFinca']

        if len(existenciaInsumo) > 0 and len(valorUnitarioInsumo) > 0 and len(descripInsumoFinca) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = InsumoFinca.objects.filter(id=id).exists()
                if existe:
                    regInsumo = Insumo.objects.get(id=listaInsumos)
                    regMedida = UnidadMedida.objects.get(id=listaUnidades)
                    regInsumoFinca = InsumoFinca.objects.get(id=id)
                    regInsumoFinca.insumo = regInsumo
                    regInsumoFinca.finca = regFinca
                    regInsumoFinca.existenciaInsumo = existenciaInsumo
                    regInsumoFinca.valorUnitarioInsumo = valorUnitarioInsumo
                    regInsumoFinca.descripInsumoFinca = descripInsumoFinca
                    regInsumoFinca.unidadmedida = regMedida
                    regInsumoFinca.save()
                    context['mensaje'] = 'Insumo de finca modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regInsumo = Insumo.objects.get(id=listaInsumos)
                regMedida = UnidadMedida.objects.get(id=listaUnidades)
                regInsumoFinca = InsumoFinca(insumo=regInsumo, existenciaInsumo=existenciaInsumo,
                                             valorUnitarioInsumo=valorUnitarioInsumo,
                                             unidadmedida=regMedida, finca=regFinca, descripInsumoFinca=descripInsumoFinca)
                regInsumoFinca.save()
                context['mensaje'] = 'Insumo de finca creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'gerenteForm/insumoFincaForm.html', context)

#*****************************************************************************************************************
def editarProductos(request):

    # consultar lotes
    regFinca = request.user.Finca

    # consultar los datos
    listaProductos = Producto.objects.filter(finca=regFinca).values('id', 'descripProducto', 'unidadMedida__id')
    listaMedidas = UnidadMedida.objects.all().values('id', 'descripUnidadMedida')

    # Armar context
    context = {
        'titulo': 'Productos',
        'nombreForm': 'Consultar y editar Productos',
        'ruta': 'productos',
        'listaProductos': listaProductos,
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
            regProducto = Producto.objects.get(id=id)
            # Respuesta JSON
            data = {
                'descripProducto': regProducto.descripProducto,
                'unidadMedida': regProducto.unidadMedida.id,
                'existenciaProducto': regProducto.existenciaProducto,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        # Validar datos del formulario
        id = int(request.POST['listaProductos'])
        descripProducto = request.POST['descripProducto']
        listaMedidas = int(request.POST['listaMedidas'])
        existenciaProducto = request.POST['existenciaProducto']

        if len(descripProducto) > 0 and len(existenciaProducto) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = Producto.objects.filter(id=id).exists()
                if existe:
                    regUnidad = UnidadMedida.objects.get(id=listaMedidas)
                    regProducto = Producto.objects.get(id=id)
                    regProducto.unidadMedida = regUnidad
                    regProducto.descripProducto = descripProducto
                    regProducto.existenciaProducto = existenciaProducto
                    regProducto.finca = regFinca
                    regProducto.save()
                    context['mensaje'] = 'Producto modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regUnidad = UnidadMedida.objects.get(id=listaMedidas)
                regProducto = Producto(unidadMedida=regUnidad, descripProducto=descripProducto,
                            existenciaProducto=existenciaProducto, finca=regFinca)
                regProducto.save()
                context['mensaje'] = 'Producto creado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']
   # Renderizar
    return render(request, 'gerenteForm/productoForm.html', context)

#*****************************************************************************************************************

def editarCompraEquipo(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaCompraEquipo = CompraEquipo.objects. prefetch_related('equipoFinca').filter(equipoFinca__finca=regFinca).values('id', 'numFactura', 'equipo__id', 'equipoFinca__id', 'proveedor__id')
    listaEquipo = Equipo.objects.all().values('id', 'descripEquipo')
    listaEquipoFinca = EquipoFinca.objects.filter(finca=regFinca).values('id', 'descripEquipoFinca')
    listaProveedores = Proveedor.objects.all().values('id', 'nombreProveedor')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Compra de Equipos',
        'ruta': 'compraEquipo',
        'nombreForm': 'Ingresar compra de Equipo',
        'listaCompraEquipo': listaCompraEquipo,
        'listaEquipo': listaEquipo,
        'listaEquipoFinca': listaEquipoFinca,
        'listaProveedores': listaProveedores,

    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regCompraEquipo = CompraEquipo.objects.get(id=id)
            # Respuesta JSON
            data = {
                'equipo': regCompraEquipo.equipo.id,
                'equipoFinca': regCompraEquipo.equipoFinca.id,
                'proveedor': regCompraEquipo.proveedor.id,
                'fechaCompraEquipo': regCompraEquipo.fechaCompraEquipo,
                'numFactura': regCompraEquipo.numFactura,
                'cantidadCompraEquipo': regCompraEquipo.cantidadCompraEquipo,
                'valorCompraEquipo': regCompraEquipo.valorCompraEquipo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaCompraEquipo = int(request.POST['listaCompraEquipo'])
        listaEquipo = int(request.POST['listaEquipo'])
        listaEquipoFinca = int(request.POST['listaEquipoFinca'])
        listaProveedores = int(request.POST['listaProveedores'])
        fechaCompraEquipo = request.POST['fechaCompraEquipo']
        numFactura = request.POST['numFactura']
        cantidadCompraEquipo = request.POST['cantidadCompraEquipo']
        valorCompraEquipo = request.POST['valorCompraEquipo']

        regEquipo = Equipo.objects.get(id=listaEquipo)
        regEquipoFinca = EquipoFinca.objects.get(id=listaEquipoFinca)
        regProveedores = Proveedor.objects.get(id=listaProveedores)

        # SI compra de quipo == 0, entonces crear 
        if listaCompraEquipo == 0:
            regCompraEquipo = CompraEquipo(equipo=regEquipo, equipoFinca=regEquipoFinca, proveedor=regProveedores, fechaCompraEquipo=fechaCompraEquipo, numFactura=numFactura,
                                 cantidadCompraEquipo=cantidadCompraEquipo, valorCompraEquipo=valorCompraEquipo)
            context['mensaje'] = 'Compra de Equipo registrada'
            regCompraEquipo.save()
        else:
            # sino, modifica 
            regCompraEquipo = CompraEquipo.objects.get(id=listaCompraEquipo)
            regCompraEquipo.equipo = regEquipo
            regCompraEquipo.equipoFinca = regEquipoFinca
            regCompraEquipo.proveedor = regProveedores
            regCompraEquipo.fechaCompraEquipo = fechaCompraEquipo
            regCompraEquipo.numFactura = numFactura
            regCompraEquipo.cantidadCompraEquipo = cantidadCompraEquipo
            regCompraEquipo.valorCompraEquipo = valorCompraEquipo
            context['mensaje'] = 'Compra de Equipo modificada'
            regCompraEquipo.save()
    return render(request, 'asistenteForm/compraEquipoForm.html', context)

#*****************************************************************************************************************

def editarClientes(request):
    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaClientes = Cliente.objects.filter(finca=regFinca).values()

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Clientes',
        'ruta': 'clientes',
        'nombreForm': 'Editar y consultar Clientes',
        'listaClientes': listaClientes

    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regCliente = Cliente.objects.get(id=id)
            # Respuesta JSON
            data = {
                'nombreCliente': regCliente.nombreCliente,
                'nitCliente': regCliente.nitCliente,
                'telefonoCliente': regCliente.telefonoCliente,
                'correoCliente': regCliente.correoCliente,
                'direccionCliente': regCliente.direccionCliente,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        id = int(request.POST['listaClientes'])
        nombreCliente = request.POST['nombreCliente']
        nitCliente = request.POST['nitCliente']
        telefonoCliente = request.POST['telefonoCliente']
        correoCliente = request.POST['correoCliente']
        direccionCliente = request.POST['direccionCliente']
        if len(nombreCliente) > 0 and len(nitCliente) > 0 and len(telefonoCliente) > 0 and len(correoCliente) > 0 and len(direccionCliente) > 0:
            if id > 0:
                # MODIFICAR REGISTRO
                existe = Cliente.objects.filter(id=id).exists()
                if existe:
                    regCliente = Cliente.objects.get(id=id)
                    regCliente.nombreCliente = nombreCliente
                    regCliente.nitCliente = nitCliente
                    regCliente.telefonoCliente = telefonoCliente
                    regCliente.correoCliente = correoCliente
                    regCliente.direccionCliente = direccionCliente
                    regCliente.finca = regFinca
                    regCliente.save()
                    context['mensaje'] = 'Cliente modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                # CREAR REGISTRO
                regCliente = Cliente(nombreCliente=nombreCliente, telefonoCliente=telefonoCliente, nitCliente=nitCliente,
                                           correoCliente=correoCliente, direccionCliente=direccionCliente,  finca=regFinca,)
                regCliente.save()
                context['mensaje'] = 'Cliente creado'
        else:
            context['alarma'] = 'Debe de diligenciar todos los datos'
    # -- en cualquier caso...
    return render(request, 'gerenteForm/clientesForm.html', context)

#*****************************************************************************************************************

def editarCompraInsumo(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaCompraInsumo = CompraInsumo.objects. prefetch_related('insumoFinca').filter(insumoFinca__finca=regFinca).values('id', 'numFactura', 'insumo__id', 'insumoFinca__id', 'proveedor__id')
    listaInsumo = Insumo.objects.all().values('id', 'descripInsumo')
    listaInsumoFinca = InsumoFinca.objects.filter(finca=regFinca).values('id', 'descripInsumoFinca')
    listaProveedores = Proveedor.objects.all().values('id', 'nombreProveedor')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Compra de Insumos',
        'ruta': 'CompraInsumo',
        'nombreForm': 'Ingresar compra de Insumos',
        'listaCompraInsumo': listaCompraInsumo,
        'listaInsumo': listaInsumo,
        'listaInsumoFinca': listaInsumoFinca,
        'listaProveedores': listaProveedores,

    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regCompraInsumo = CompraInsumo.objects.get(id=id)
            # Respuesta JSON
            data = {
                'insumo': regCompraInsumo.insumo.id,
                'insumoFinca': regCompraInsumo.insumoFinca.id,
                'proveedor': regCompraInsumo.proveedor.id,
                'cantidadCompraInsumo': regCompraInsumo.cantidadCompraInsumo,
                'fechaCompraInsumo': regCompraInsumo.fechaCompraInsumo,
                'numFactura': regCompraInsumo.numFactura,
                'valorCompraInsumo': regCompraInsumo.valorCompraInsumo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaCompraInsumo = int(request.POST['listaCompraInsumo'])
        listaInsumo = int(request.POST['listaInsumo'])
        listaInsumoFinca = int(request.POST['listaInsumoFinca'])
        listaProveedores = int(request.POST['listaProveedores'])
        cantidadCompraInsumo = request.POST['cantidadCompraInsumo']
        fechaCompraInsumo = request.POST['fechaCompraInsumo']
        numFactura = request.POST['numFactura']
        valorCompraInsumo = request.POST['valorCompraInsumo']

        regInsumo = Insumo.objects.get(id=listaInsumo)
        regInsumoFinca = InsumoFinca.objects.get(id=listaInsumoFinca)
        regProveedores = Proveedor.objects.get(id=listaProveedores)

        # SI compra de quipo == 0, entonces crear 
        if listaCompraInsumo == 0:
            regCompraInsumo = CompraInsumo(insumo=regInsumo, insumoFinca=regInsumoFinca, proveedor=regProveedores, cantidadCompraInsumo=cantidadCompraInsumo, fechaCompraInsumo=fechaCompraInsumo,
                                 numFactura=numFactura, valorCompraInsumo=valorCompraInsumo)
            context['mensaje'] = 'Compra de Insumo registrada'
            regCompraInsumo.save()
        else:
            # sino, modifica 
            regCompraInsumo = CompraInsumo.objects.get(id=listaCompraInsumo)
            regCompraInsumo.insumo = regInsumo
            regCompraInsumo.insumoFinca = regInsumoFinca
            regCompraInsumo.proveedor = regProveedores
            regCompraInsumo.cantidadCompraInsumo = cantidadCompraInsumo
            regCompraInsumo.fechaCompraInsumo = fechaCompraInsumo
            regCompraInsumo.numFactura = numFactura
            regCompraInsumo.valorCompraInsumo = valorCompraInsumo
            context['mensaje'] = 'Compra de Insumo modificada'
            regCompraInsumo.save()
    return render(request, 'asistenteForm/compraInsumoForm.html', context)

#*****************************************************************************************************************

def editarEquiposLabor(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaEquipoLabor = EquiposLabor.objects.prefetch_related('equipoFinca').filter(equipoFinca__finca=regFinca).values('id', 'cantidadUsadaEquipo', 'equipoFinca__id', 'cultivo__id')
    listaCultivos = Cultivo.objects.prefetch_related('lote').filter(lote__finca=regFinca).values('id', 'observacCultivo')
    listaEquipoFinca = EquipoFinca.objects.filter(finca=regFinca).values('id', 'descripEquipoFinca')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Labores de Equipos',
        'ruta': 'equiposlabor',
        'nombreForm': 'Ingresar el labor del Equipo',
        'listaEquipoLabor': listaEquipoLabor,
        'listaCultivos': listaCultivos,
        'listaEquipoFinca': listaEquipoFinca,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regEquiposLabor = EquiposLabor.objects.get(id=id)
            # Respuesta JSON
            data = {
                'equipoFinca': regEquiposLabor.equipoFinca.id,
                'cultivo': regEquiposLabor.cultivo.id,
                'cantidadUsadaEquipo': regEquiposLabor.cantidadUsadaEquipo,
                'costo': regEquiposLabor.costo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaEquipoLabor = int(request.POST['listaEquipoLabor'])
        listaCultivos = int(request.POST['listaCultivos'])
        listaEquipoFinca = int(request.POST['listaEquipoFinca'])
        cantidadUsadaEquipo = request.POST['cantidadUsadaEquipo']
        costo = request.POST['costo']

        regEquipoFinca = EquipoFinca.objects.get(id=listaEquipoFinca)
        regCultivo = Cultivo.objects.get(id=listaCultivos)

        # SI EQUIPO LABOR == 0 ENTONCES CREAR:
        if listaEquipoLabor == 0:
            regEquiposLabor = EquiposLabor(equipoFinca=regEquipoFinca, cultivo=regCultivo, cantidadUsadaEquipo=cantidadUsadaEquipo,costo=costo )
            context['mensaje'] = 'Labor de Equipo registrada'
            regEquiposLabor.save()
        else:
            # SI NO, MODIFICA
            regEquiposLabor = EquiposLabor.objects.get(id=listaEquipoLabor)
            regEquiposLabor.equipoFinca = regEquipoFinca
            regEquiposLabor.cultivo = regCultivo
            regEquiposLabor.cantidadUsadaEquipo = cantidadUsadaEquipo
            regEquiposLabor.costo = costo
            context['mensaje'] = 'Labor de Equipo modificada'
            regEquiposLabor.save()
    return render(request, 'asistenteForm/equiposLaborForm.html', context)

#*****************************************************************************************************************

def editarInsumoLabor(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaHorasTrabajo = HoraTrabajo.objects.prefetch_related('trabajador').filter(trabajador__finca=regFinca).values('id', 'cantidadUsadaInsumo', 'categHora__id', 'cultivo__id', )
    listaCultivos = Cultivo.objects.prefetch_related('lote').filter(lote__finca=regFinca).values('id', 'observacCultivo')
    listaInsumosFinca = InsumoFinca.objects.filter(finca=regFinca).values('id', 'descripInsumoFinca')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Labores de Insumos',
        'ruta': 'insumoLabor',
        'nombreForm': 'Ingresar el labor del Insumo',
        'listaInsumoLabor': listaInsumoLabor,
        'listaCultivos': listaCultivos,
        'listaInsumosFinca': listaInsumosFinca,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regInsumoLabor = InsumosLabor.objects.get(id=id)
            # Respuesta JSON
            data = {
                'insumoFinca': regInsumoLabor.insumoFinca.id,
                'cultivo': regInsumoLabor.cultivo.id,
                'cantidadUsadaInsumo': regInsumoLabor.cantidadUsadaInsumo,
                'costo': regInsumoLabor.costo,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaInsumoLabor = int(request.POST['listaInsumoLabor'])
        listaCultivos = int(request.POST['listaCultivos'])
        listaInsumosFinca = int(request.POST['listaInsumosFinca'])
        cantidadUsadaInsumo = request.POST['cantidadUsadaInsumo']
        costo = request.POST['costo']

        regInsumoFinca = InsumoFinca.objects.get(id=listaInsumosFinca)
        regCultivo = Cultivo.objects.get(id=listaCultivos)

        # SI INSUMO LABOR == 0 ENTONCES CREAR:
        if listaInsumoLabor == 0:
            regInsumoLabor = InsumosLabor(insumoFinca=regInsumoFinca, cultivo=regCultivo, cantidadUsadaInsumo=cantidadUsadaInsumo,costo=costo )
            context['mensaje'] = 'Labor de Insumo registrada'
            regInsumoLabor.save()
        else:
            # SI NO, MODIFICA
            regInsumoLabor = InsumosLabor.objects.get(id=listaInsumoLabor)
            regInsumoLabor.insumoFinca = regInsumoFinca
            regInsumoLabor.cultivo = regCultivo
            regInsumoLabor.cantidadUsadaInsumo = cantidadUsadaInsumo
            regInsumoLabor.costo = costo
            context['mensaje'] = 'Labor de Insumo modificada'
            regInsumoLabor.save()
    return render(request, 'asistenteForm/insumosLaborForm.html', context)

#*****************************************************************************************************************

def editarHorasTrabajo(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaHorasTrabajo = HoraTrabajo.objects.prefetch_related('trabajador').filter(trabajador__finca=regFinca).values('id', 'observacLabor', 'trabajador__id', 'cultivo__id', 'categHora__id')
    listaCultivos = Cultivo.objects.prefetch_related('lote').filter(lote__finca=regFinca).values('id', 'observacCultivo')
    listaCategHora = CategHora.objects.all().values('id', 'descripCategHora')
    listaTrabajador = Trabajador.objects.filter(finca=regFinca).values('id', 'nombreTrabajador')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Horas De Trabajos',
        'ruta': 'horaTrabajo',
        'nombreForm': 'Ingresar El Registro De Hora',
        'listaHorasTrabajo': listaHorasTrabajo,
        'listaCultivos': listaCultivos,
        'listaCategHora': listaCategHora,
        'listaTrabajador': listaTrabajador,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regHorasTrabajos = HoraTrabajo.objects.get(id=id)
            # Respuesta JSON
            data = {
                'categHora': regHorasTrabajos.categHora.id,
                'cultivo': regHorasTrabajos.cultivo.id,
                'trabajador': regHorasTrabajos.trabajador.id,
                'duracionLabor': regHorasTrabajos.duracionLabor,
                'costo': regHorasTrabajos.costo,
                'fechaLabor': regHorasTrabajos.fechaLabor,
                'tipoTrabajo': regHorasTrabajos.tipoTrabajo,
                'observacLabor': regHorasTrabajos.observacLabor,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaHorasTrabajo = int(request.POST['listaHorasTrabajo'])
        listaCultivos = int(request.POST['listaCultivos'])
        listaCategHora = int(request.POST['listaCategHora'])
        listaTrabajador = int(request.POST['listaTrabajador'])
        duracionLabor = request.POST['duracionLabor']
        costo = request.POST['costo']
        fechaLabor = request.POST['fechaLabor']
        tipoTrabajo = request.POST['tipoTrabajo']
        observacLabor = request.POST['observacLabor']

        regCategHora = CategHora.objects.get(id=listaCategHora)
        regCultivo = Cultivo.objects.get(id=listaCultivos)
        regTrabajador = Trabajador.objects.get(id=listaTrabajador)

        # SI INSUMO LABOR == 0 ENTONCES CREAR:
        if listaHorasTrabajo == 0:
            regHorasTrabajos = HoraTrabajo(categHora=regCategHora, trabajador=regTrabajador, cultivo=regCultivo, duracionLabor=duracionLabor,costo=costo, fechaLabor=fechaLabor, tipoTrabajo=tipoTrabajo, observacLabor=observacLabor)
            context['mensaje'] = 'Hora De Trabajo registrada'
            regHorasTrabajos.save()
        else:
            # SI NO, MODIFICA
            regHorasTrabajos = HoraTrabajo.objects.get(id=listaHorasTrabajo)
            regHorasTrabajos.categHora = regCategHora
            regHorasTrabajos.trabajador = regTrabajador
            regHorasTrabajos.cultivo = regCultivo
            regHorasTrabajos.duracionLabor = duracionLabor
            regHorasTrabajos.costo = costo
            regHorasTrabajos.fechaLabor = fechaLabor
            regHorasTrabajos.tipoTrabajo = tipoTrabajo
            regHorasTrabajos.observacLabor = observacLabor
            context['mensaje'] = 'Hora De Trabajo modificada'
            regHorasTrabajos.save()
    return render(request, 'asistenteForm/horasTrabajoForm.html', context)


#*****************************************************************************************************************

def editarVentas(request):

    # CONSULTAR DE QUE FINCA PERTENECE EL USUARIO
    regFinca = request.user.Finca
    listaVentas = Venta.objects.prefetch_related('cliente').filter(cliente__finca=regFinca).values('id', 'observacVenta', 'producto__id', 'cliente__id')
    listaProducto = Producto.objects.filter(finca=regFinca).values('id', 'descripProducto')
    listaCliente = Cliente.objects.filter(finca=regFinca).values('id', 'nombreCliente')

    # ARMAR CONTEXTO
    context = {
        'titulo': 'Ventas',
        'ruta': 'ventas',
        'nombreForm': 'Ingresar La Venta',
        'listaVentas': listaVentas,
        'listaProducto': listaProducto,
        'listaCliente': listaCliente,
    }

    # SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # CONSULTAR REGITRO DE TRABAJADOR
            regVentas = Venta.objects.get(id=id)
            # Respuesta JSON
            data = {
                'producto': regVentas.producto.id,
                'cliente': regVentas.cliente.id,
                'numFactura': regVentas.numFactura,
                'fechaventa': regVentas.fechaventa,
                'cantidadVenta': regVentas.cantidadVenta,
                'observacVenta': regVentas.observacVenta,
                'valorTotalVentas': regVentas.valorTotalVentas,
            }
            return JsonResponse(data)

    if request.method == 'POST':
        listaVentas = int(request.POST['listaVentas'])
        listaProducto = int(request.POST['listaProducto'])
        listaCliente = int(request.POST['listaCliente'])
        numFactura = request.POST['numFactura']
        fechaventa = request.POST['fechaventa']
        cantidadVenta = request.POST['cantidadVenta']
        observacVenta = request.POST['observacVenta']
        valorTotalVentas = request.POST['valorTotalVentas']

        regProducto = Producto.objects.get(id=listaProducto)
        regCliente = Cliente.objects.get(id=listaCliente)

        # SI VENTA == 0 ENTONCES CREAR:
        if listaVentas == 0:
            regVentas = Venta(cliente=regCliente, producto=regProducto, fechaventa=fechaventa,numFactura=numFactura, cantidadVenta=cantidadVenta, observacVenta=observacVenta, valorTotalVentas=valorTotalVentas)
            context['mensaje'] = 'Venta Registrada'
            regVentas.save()
        else:
            # SI NO, MODIFICA
            regVentas = Venta.objects.get(id=listaVentas)
            regVentas.cliente = regCliente
            regVentas.producto = regProducto
            regVentas.fechaventa = fechaventa
            regVentas.numFactura = numFactura
            regVentas.cantidadVenta = cantidadVenta
            regVentas.observacVenta = observacVenta
            regVentas.valorTotalVentas = valorTotalVentas
            context['mensaje'] = 'Venta Modificada'
            regVentas.save()
    return render(request, 'asistenteForm/ventasForm.html', context)