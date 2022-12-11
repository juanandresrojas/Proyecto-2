from django.db import models
from datetime import date

from appAdmin.models import *

# Create your models here.
#***************************************************************************************

class Finca (models.Model):
    nombreFinca = models.CharField(max_length=100, null=False)
    nombreGerente = models.CharField(max_length=100, null=False)
    apellidoGerente = models.CharField(max_length=100, null=True)
    nitFinca = models.IntegerField(null=False)
    correoGerente = models.CharField(max_length=100, null=False)
    cedulaGerente = models.CharField(max_length=100, null=False)
    ubicacionFinca = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.nombreFinca

#***************************************************************************************

class Lote (models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    observacLote = models.CharField(max_length=300, null=False)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE , null=False)
    descripLote = models.CharField(max_length=100, null=False)
    areaLote = models.IntegerField(null=False)
    

    def __str__(self):
        return "{} - {}".format(self.finca, self.descripLote )

#***************************************************************************************

class Indirecto (models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    fechaPago = models.DateField(null=False)
    numFactura = models.CharField(max_length=15, null=False)
    observacPago = models.CharField(max_length=200, null=False)
    valorPagado = models.DecimalField(max_digits=10, decimal_places=2,  null=False)

    def __str__(self):
        return "{} - {}".format(self.finca, self.observacPago )

    class Meta:
        verbose_name_plural = "Costos indirectos"


#***************************************************************************************

class Trabajador (models.Model):
    finca  = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    telefonoTrabajador = models.CharField(max_length=20, null=False)
    nombreTrabajador = models.CharField(max_length=100, null=False)
    nitTrabajador = models.IntegerField(null=False)
    emailTrabajador = models.CharField(max_length=100, null=False)
    costoHoraTrabajador = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    rol = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.nombreTrabajador

    class Meta:
        verbose_name_plural = "Trabajadores"

#***************************************************************************************
class Producto (models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    existenciaProducto = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    descripProducto = models.CharField(max_length=100, null=False)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE , null=False)

    def __str__(self):
        return "{} - {}".format(self.descripProducto, self.existenciaProducto )

#***************************************************************************************

class Cultivo (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE , null=False)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE , null=False)
    fechaSiembra = models.DateField(null=False)
    fechaCosecha = models.DateField(null=False)
    cantidadCosecha = models.IntegerField(null=False)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE , null=False)
    observacCultivo = models.CharField(max_length=300, null=False)
    activo = models.BooleanField(default=True, null=False)

    def __str__(self):
        return "{} - {}".format(self.producto, self.observacCultivo )

#***************************************************************************************

class HoraTrabajo (models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE , null=False)
    observacLabor = models.CharField(max_length=300, null=False)
    tipoTrabajo = models.CharField(max_length=300, null=False)
    categHora = models.ForeignKey(CategHora, on_delete=models.CASCADE , null=False)
    fechaLabor = models.DateField(null=False)
    duracionLabor = models.IntegerField(null=False)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE , null=False)
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    def __str__(self):
        return "{} - {}".format(self.trabajador, self.categHora )
    class Meta:
        verbose_name_plural = "Horas de trabajo"

#***************************************************************************************
class EquipoFinca (models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE , null=False)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    existenciaEquipo = models.DecimalField(max_digits=10,decimal_places=2, null=False)
    valorUnitarioEquipo = models.DecimalField(max_digits=10,decimal_places=2, null=False)
    deprecEquipo = models.DecimalField(max_digits=10,decimal_places=2, null=False)
    descripEquipoFinca = models.CharField(max_length=100, null=True)


    def __str__(self):
        return "{} - {}".format(self.finca, self.descripEquipoFinca )
    class Meta:
        verbose_name_plural = "Equipo de fincas"

#***************************************************************************************

class CompraEquipo (models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE , null=False)
    equipoFinca = models.ForeignKey(EquipoFinca, on_delete=models.CASCADE , null=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE , null=False)
    fechaCompraEquipo = models.DateField(null=False)
    numFactura = models.CharField(max_length=15, null=False)
    cantidadCompraEquipo = models.DecimalField(max_digits=12,decimal_places=2, null=False)
    valorCompraEquipo = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    def __str__(self):
        return "{} - {}".format(self.equcultivopoFinca, self.proveedor )
    class Meta:
        verbose_name_plural = "Compra de equipos"


#***************************************************************************************

class InsumoFinca (models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE , null=False)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)
    existenciaInsumo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE , null=False)
    valorUnitarioInsumo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    descripInsumoFinca = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "{} - {}".format(self.finca, self.descripInsumoFinca)
    class Meta:
        verbose_name_plural = "Insumos de finca"

#***************************************************************************************

class CompraInsumo (models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE , null=False)
    insumoFinca = models.ForeignKey(InsumoFinca, on_delete=models.CASCADE , null=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE , null=False)
    cantidadCompraInsumo = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fechaCompraInsumo = models.DateField(null=False)
    numFactura = models.CharField(max_length=15, null=False)
    valorCompraInsumo = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return "{} - {}".format(self.insumo, self.proveedor )

    class Meta:
        verbose_name_plural = "Compra de insumos"

#***************************************************************************************

class Cliente (models.Model):
    telefonoCliente = models.IntegerField(null=False)
    nombreCliente = models.CharField(max_length=100, null=False)
    nitCliente = models.CharField(max_length=20, null=False)
    direccionCliente = models.CharField(max_length=100, null=False)
    correoCliente = models.CharField(max_length=100, null=False)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE , null=False)

    def __str__(self):
        return "{} - {}".format(self.nombreCliente, self.finca )

#***************************************************************************************
class Venta (models.Model):
    numFactura = models.CharField(max_length=15, null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE , null=False)
    fechaventa = models.DateField(default= date.today)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE , null=False)
    cantidadVenta = models.IntegerField(null=False)
    observacVenta = models.CharField(max_length=300, null=False)
    valorTotalVentas = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return "{} - {}".format(self.cantidadVenta, self.cliente )

#***************************************************************************************

class InsumosLabor (models.Model):
    insumoFinca = models.ForeignKey(InsumoFinca, on_delete=models.CASCADE , null=False)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE , null=False)
    cantidadUsadaInsumo = models.IntegerField(null=False)
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    def __str__(self):
        return self.cantidadUsadaInsumo

    class Meta:
        verbose_name_plural = "Insumos de labores"
#***************************************************************************************








        




