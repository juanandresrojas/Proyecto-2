from ast import Return
from doctest import master
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.

#**************************************************************************************************

class CategMaterial (models.Model):
    descripCategMaterial = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.descripCategMaterial

    class Meta:
        verbose_name_plural = "Categoria Materiales "

class Equipo(models.Model):
     categMaterial = models.ForeignKey(CategMaterial, on_delete=models.CASCADE , null=False)
     descripEquipo = models.CharField(max_length=100, null=False)

     def __str__(self):
        return self.descripEquipo

     class Meta:
        verbose_name_plural = "Equipos"


class Proveedor(models.Model):
    telefonoProveedor = models.IntegerField(null=False)
    nombreProveedor = models.CharField(max_length=100, null=False)
    nitProvedor = models.CharField(max_length=20 , null=False)
    direccionProveedor = models.CharField(max_length=100, null=False)
    correoProveedor = models.CharField(max_length=100 , null=False)

    def __str__(self):
        return self.nombreProveedor

    class Meta:
        verbose_name_plural = "Proveedores"
    

class CategHora(models.Model):
    recargo = models.CharField(max_length=100 , null=False)
    descripCategHora = models.CharField(max_length=300 , null=False)

    def __str__(self):
        return self.descripCategHora
 
    class Meta:
        verbose_name_plural = "Categoria de Horas"

class UnidadMedida(models.Model):
    descripUnidadMedida = models.CharField(max_length=100 , null=False)

    def __str__(self):
        return self.descripUnidadMedida
    class Meta:
        verbose_name_plural = "Unidades Medidas"

class Insumo(models.Model):
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE , null=False)
    descripInsumo = models.CharField(max_length=100 , null=False)
    categMaterial = models.ForeignKey(CategMaterial, on_delete=models.CASCADE , null=False)

    def __str__(self):
        return self.descripInsumo 
    class Meta:
        verbose_name_plural = "Insumos"



    

