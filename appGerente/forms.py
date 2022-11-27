from django import forms
from appGerente.models import *

#**************************************************************************************************
class FincaForms (forms.Form):

    lista = [(0, 'seleccione su finca...'),]
    lista1= Finca.objects.all().values_list('id', 'nombreFinca','nombreGerente','apellidoGerente','nitFinca','correoGerente','cedulaGerente','ubicacionFinca')
    for elem in lista1:
        lista.append(elem)

    
    categoriaFinca = forms.ChoiceField(choices= lista, label='Lista de finca')
    nombreFinca = forms.CharField(label='Nombre de la finca')
    nombreGerente = forms.CharField(label='Nombre del gerenete')
    apellidoGerente = forms.CharField(label='apellido gerente')
    nitFinca = forms.CharField(label='Nit de la finca')
    correoGerente = forms.CharField(label='Correo del gerente')
    cedulaGerente = forms.CharField(label='Cedula del gerente')
    ubicacionFinca = forms.CharField(label='Ubicacion de la finca')
    
#**************************************************************************************************

