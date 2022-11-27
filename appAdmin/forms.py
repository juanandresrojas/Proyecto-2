from django import forms
from appAdmin.models import *

#**************************************************************************************************
class CategHorasForms (forms.Form):

    #lista = CategHoras.objects.all().values_list('id'), 'descripCategHora')
    lista = [(0, 'seleccione una categoria de hora...'),]
    lista1= CategHora.objects.all().values_list('id', 'descripCategHora')
    for elem in lista1:
        lista.append(elem)

    
    categoriasHoras = forms.ChoiceField(choices= lista, label='Lista Categorias de Horas')
    descripCategHora = forms.CharField(label='Descripcion de la categoria')
    recargo = forms.DecimalField(label='Porcentaje de Recargo')


#**************************************************************************************************
class CategMaterialForms (forms.Form):

    lista = [(0, 'seleccione una categoria de Material...'),]
    lista1= CategMaterial.objects.all().values_list('id', 'descripCategMaterial')
    for elem in lista1:
        lista.append(elem)

    
    categoriasMaterial = forms.ChoiceField(choices= lista, label='Lista Categorias de Materiales')
    descripCategMaterial = forms.CharField(label='Descripcion del material')
    
#**************************************************************************************************
class ProveedorForms (forms.Form):

    lista = [(0, 'seleccione un Proveedor...'),]
    lista1= Proveedor.objects.all().values_list('id', 'nombreProveedor')
    for elem in lista1:
        lista.append(elem)

    
    categoriasProveedor = forms.ChoiceField(choices= lista, label='Lista Categorias de Proveedores')
    telefonoProveedor = forms.IntegerField(label='Numero del proveedor')
    nombreProveedor = forms.CharField(label='Nombre del Proveedor')
    nitProvedor = forms.CharField(label='Nit del Proveedor')
    direccionProveedor = forms.CharField(label='Dirección del Proveedor')
    correoProveedor = forms.CharField(label='Correo del proveedor')
     
#**************************************************************************************************

class UnidadMedidaForms (forms.Form):

    lista = [(0, 'seleccione una categoria Medida...'),]
    lista1= UnidadMedida.objects.all().values_list('id', 'descripUnidadMedida')
    for elem in lista1:
        lista.append(elem)

    
    categoriasMedidas = forms.ChoiceField(choices= lista, label='Lista Categorias de Medidas')
    descripUnidadMedida = forms.CharField(label='Descripcion de Medida')

#**************************************************************************************************
