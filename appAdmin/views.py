from asyncio.windows_events import NULL
from multiprocessing import context
from re import X
from django.shortcuts import render,redirect
from .forms import *
from django.http import JsonResponse
import json
from .models import *

# *********************************************************************************************************************
# Create your views here.
# **************************** CONSULTAR Y EDITAR HORAS ************************************


def editarHoras(request):
    context = {
        'titulo': 'Horas',
        'nombreForm': 'Consultar y Editar Horas',
        'ruta': 'categHoras',
    }
    if request.method == 'POST':
        id = int(request.POST['categoriasHoras'])
        descrip = request.POST['descripCategHora']
        recargo = request.POST['recargo']
        if len(descrip) > 0 and len(recargo) > 0:
            if id > 0:
                existe = CategHora.objects.filter(id=id).exists()
                if existe:
                    regHora = CategHora.objects.get(id=id)
                    regHora.descripCategHora = descrip
                    regHora.recargo = recargo
                    regHora.save()
                    context['mensaje'] = 'Registro modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regHora = CategHora(descripCategHora=descrip, recargo=recargo)
                regHora.save()
                context['mensaje'] = 'Registro creado'
        else:
            context['alarma'] = 'Debe diligenciar la descripcion y el recargo'
        # EN CUALQUIER CASO.....
    context['form'] = CategHorasForms()
    return render(request, 'plantillaForm.html', context)


"""
    Usa AJAX para enviar datos desde un tipo hora en formato JSON
"""


def consultarHora(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # Lee el registro
            regHora = CategHora.objects.get(id=id)
            data = {
                'descripCategHora': regHora.descripCategHora,
                'recargo': regHora.recargo,
            }
            return JsonResponse(data)

    else:
        data = {
            'error': 'No es AJAX', }

        return JsonResponse(data)

# ***************************************** EDITAR Y CONSULTAR MATERIALES ****************************************************************************


def editarMateriales(request):
    context = {
        'titulo': 'Materiales',
        'nombreForm': 'Consultar y Editar Materiales',
        'ruta': 'categMaterial',
    }
    if request.method == 'POST':
        id = int(request.POST['categoriasMaterial'])
        descrip = request.POST['descripCategMaterial']
        if len(descrip) > 0:
            if id > 0:
                existe = CategMaterial.objects.filter(id=id).exists()
                if existe:
                    regMaterial = CategMaterial.objects.get(id=id)
                    regMaterial.descripCategMaterial = descrip
                    regMaterial.save()
                    context['mensaje'] = 'Registro modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regMaterial = CategMaterial(descripCategMaterial=descrip)
                regMaterial.save()
                context['mensaje'] = 'Registro creado'
        else:
            context['alarma'] = 'Debe diligenciar la descripcion.'
        # EN CUALQUIER CASO.....
    context['form'] = CategMaterialForms()
    return render(request, 'plantillaForm.html', context)


def consultarMaterial(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # Lee el registro
            regMaterial = CategMaterial.objects.get(id=id)
            data = {
                'descripCategMaterial': regMaterial.descripCategMaterial,
            }
            return JsonResponse(data)

    else:
        data = {
            'error': 'No es AJAX', }

        return JsonResponse(data)


# ***************************************** EDITAR Y CONSULTAR PROVEEDORES ******************************************

def editarProvedores(request):
    context = {
        'titulo': 'Proveedores',
        'nombreForm': 'Consultar y Editar Proveedores',
        'ruta': 'proveedor',
    }
    if request.method == 'POST':
        id = int(request.POST['categoriasProveedor'])
        nombreProveedor = request.POST['nombreProveedor']
        telefonoProveedor = request.POST['telefonoProveedor']
        nitProvedor = request.POST['nitProvedor']
        direccionProveedor = request.POST['direccionProveedor']
        correoProveedor = request.POST['correoProveedor']
        if len(nombreProveedor) > 0:
            if id > 0 and len(telefonoProveedor) > 0 and len(nitProvedor) > 0 and len(direccionProveedor) > 0 and len(correoProveedor) > 0:
                existe = Proveedor.objects.filter(id=id).exists()
                if existe:
                    regProveedor = Proveedor.objects.get(id=id)
                    regProveedor.nombreProveedor = nombreProveedor
                    regProveedor.telefonoProveedor = telefonoProveedor
                    regProveedor.nitProvedor = nitProvedor
                    regProveedor.direccionProveedor = direccionProveedor
                    regProveedor.correoProveedor = correoProveedor
                    regProveedor.save()
                    context['mensaje'] = 'Registro modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' + \
                        str(id) + 'no existe'
            else:
                regProveedor = Proveedor(nombreProveedor=nombreProveedor, telefonoProveedor=telefonoProveedor,nitProvedor=nitProvedor, direccionProveedor=direccionProveedor, correoProveedor=correoProveedor)
                regProveedor.save()
                context['mensaje'] = 'Registro creado'
        else:
            context['alarma'] = 'Debe diligenciar la descripcion.'
        # EN CUALQUIER CASO.....
    context['form'] = ProveedorForms()
    return render(request, 'plantillaForm.html', context)


def consultarProveedor(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # Lee el registro
            regProveedor = Proveedor.objects.get(id=id)
            data = {
                'telefonoProveedor': regProveedor.telefonoProveedor,
                'nombreProveedor': regProveedor.nombreProveedor,
                'nitProvedor': regProveedor.nitProvedor,
                'direccionProveedor': regProveedor.direccionProveedor,
                'correoProveedor': regProveedor.correoProveedor,
            }
            return JsonResponse(data)

    else:
        data = {
            'error': 'No es AJAX', }

        return JsonResponse(data)


# ****************************************** EDITAR Y CONSULTAR EQUIPOS ******************************************************************

def editarEquipos(request):
    # consulta las categorias
    listaCategoriasMat = CategMaterial.objects.all().values('id', 'descripCategMaterial')
    # consulta los equipos
    listaEquipos = Equipo.objects.all().values('id', 'descripEquipo', 'categMaterial__id')
    # armar el context
    context = {
        'titulo': 'Equipos',
        'nombreForm': 'Consultar y Editar Equipos',
        'ruta': 'equipos',
        'listaCategoriasMat': listaCategoriasMat,
        'listaEquipos': listaEquipos,
    }

    #SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
      if request.method == 'POST':
          # Consultar registro equipo 
          data = json.load(request)
          id1 = data.get('id')
          regEquipo = Equipo.objects.get(id=id1)
          # Respuesta JSON 
          data = {
            'categMaterial': regEquipo.categMaterial.id,              
            'descripEquipo': regEquipo.descripEquipo,           
          }
          return JsonResponse(data)

    #si es POST 
    if request.method == 'POST':
        #Validar datos del formulario 
        id = int(request.POST['listaEquipos'])
        descripEquipo = request.POST['descripEquipo']
        categ_id = int(request.POST['listaCategoriasMat']) 

        ok = True
        if len(descripEquipo) == 0:
            ok = False
        if categ_id != 0:
            regCateg = CategMaterial.objects.get(id= categ_id)
        else:
            ok = False
        if ok:
            #Si equipo.id = 0
            if id == 0:
                #Crear Regitro
                regEquipo = Equipo(categMaterial=regCateg, descripEquipo=descripEquipo)
                regEquipo.save()
                context['mensaje'] = 'Registro creado'
                # Si no
            else:
                #modificar registro 
                regEquipo = Equipo.objects.get(id=id)
                regEquipo.categMaterial = regCateg
                regEquipo.descripEquipo = descripEquipo
                regEquipo.save()
                context['mensaje'] = 'Registro modificado'
        else:
            context['alarma'] = 'Por favor seleccione todos los datos'


    # Renderizar
    return render(request, 'equipoForm.html', context)

# *********************************************************************************************************************

def editarMedida(request):
    context = {
        'titulo': 'Medidas',
        'nombreForm': 'Consultar y Editar Medidas',
        'ruta': 'unidadMedida',
    }
    if request.method == 'POST':
        id = int(request.POST['categoriasMedidas'])
        descrip = request.POST['descripUnidadMedida']
        if len(descrip) > 0:
            if id > 0:
                existe = UnidadMedida.objects.filter(id=id).exists()
                if existe:
                    regMedida = UnidadMedida.objects.get(id=id)
                    regMedida.descripUnidadMedida = descrip
                    regMedida.save()
                    context['mensaje'] = 'Registro modificado'
                else:
                    context['alarma'] = 'El registro con PK = ' +str(id) + 'no existe'
            else:
                regMedida = UnidadMedida(descripUnidadMedida=descrip)
                regMedida.save()
                context['mensaje'] = 'Registro creado'
        else:
            context['alarma'] = 'Debe diligenciar la descripcion.'
        # EN CUALQUIER CASO.....
    context['form'] = UnidadMedidaForms()
    return render(request, 'plantillaForm.html', context)



def consultarMedida(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # Toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            # Lee el registro
            regMedida = UnidadMedida.objects.get(id=id)
            data = {
                'descripUnidadMedida': regMedida.descripUnidadMedida,
            }
            return JsonResponse(data)

    else:
        data = {
            'error': 'No es AJAX', }

        return JsonResponse(data)


# *********************************************************************************************************************

def editarInsumos(request):
    # consulta las medidas
    listaMedidas = UnidadMedida.objects.all().values('id', 'descripUnidadMedida')
    # consulta las medidas
    listaMateriales = CategMaterial.objects.all().values('id', 'descripCategMaterial')
    # consulta los insumos
    listainsumos = Insumo.objects.all().values('id', 'descripInsumo', 'unidadMedida__id', 'categMaterial__id')
    # armar el context
    context = {
        'titulo': 'Insumos',
        'nombreForm': 'Consultar y Editar Insumos',
        'ruta': 'insumos',
        'listaMedidas': listaMedidas,
        'listaMateriales': listaMateriales,
        'listainsumos': listainsumos,
    }
    
    #SI ES AJAX Y POST
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
      if request.method == 'POST':
          # Consultar registro insumo 
          data = json.load(request)
          id1 = data.get('id')
          regInsumo = Insumo.objects.get(id=id1)
          # Respuesta JSON 
          data = {
            'categMaterial': regInsumo.categMaterial.id,           
            'unidadMedida': regInsumo.unidadMedida.id,           
            'descripInsumo': regInsumo.descripInsumo,           
          }
          return JsonResponse(data)

    #si es POST 
    if request.method == 'POST':
        #Validar datos del formulario 
        id = int(request.POST['listainsumos'])
        descripInsumo = request.POST['descripInsumo']
        listaMateriales = int(request.POST['listaMateriales']) 
        listaMedidas = int(request.POST['listaMedidas'])

        ok = True
        if len(descripInsumo) == 0:
            ok = False
        if listaMateriales != 0:
            regCateg = CategMaterial.objects.get(id= listaMateriales)
        else:
            ok = False
        if listaMedidas != 0:
            regUnidad = UnidadMedida.objects.get(id= listaMedidas)
        else: 
            ok = False

        if ok:
            #Si insumo.id = 0
            if id == 0:
                #Crear Regitro
                regInsumo = Insumo(categMaterial=regCateg, unidadMedida= regUnidad, descripInsumo=descripInsumo)
                regInsumo.save()
                context['mensaje'] = 'Registro creado'
              
                # Si no
            else:
                #modificar registro 
                regInsumo = Insumo.objects.get(id=id)
                regInsumo.categMaterial = regCateg
                regInsumo.unidadMedida = regUnidad
                regInsumo.descripInsumo = descripInsumo
                regInsumo.save()
                context['mensaje'] = 'Registro modificado'
        else:
            context['alarma': 'Por favor seleccione todos los datos']


    # Renderizar
    return render(request, 'insumoForm.html', context)

# *********************************************************************************************************************
