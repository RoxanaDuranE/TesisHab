from django.db import models
from ConfiguracionApp.models import *
from SolicitudesApp.models import *

# Create your models here.

class PresupuestoViviDatGen(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha= models.DateField(null=False)
    TiempoCons= models.CharField(max_length=8)
    Modelo= models.CharField(max_length=20)
    DimensionVivi= models.CharField(max_length=35)
    CantidadVivi= models.IntegerField()
    CostoTotaViv= models.DecimalField(decimal_places=2, max_digits=15)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='PresupuestoViviDatGen'
        verbose_name_plural='PresupuestoViviDatGens'
        db_table= 'PresupuestoViviDatGen'
        
class PresupuestoViviMat(models.Model):
    Id= models.AutoField(primary_key=True)
    Cantidad= models.DecimalField(decimal_places=2, max_digits=10)
    PrecioUnit= models.DecimalField(decimal_places=2, max_digits=10)
    SubTota= models.DecimalField(decimal_places=2, max_digits=15)
    IdMateriales=models.ForeignKey(Materiales, on_delete=models.CASCADE)
    IdPresupuestoViviDatGen=models.ForeignKey(PresupuestoViviDatGen, on_delete=models.CASCADE)

    class Meta:
        verbose_name='PresupuestoViviMat'
        verbose_name_plural='PresupuestoViviMats'
        db_table= 'PresupuestoViviMat'

class PresupuestoViviManObr(models.Model):
    Id= models.AutoField(primary_key=True)
    Descripcion= models.CharField(max_length=150)
    Unidad= models.CharField(max_length=8)
    PrecioUnit= models.DecimalField(decimal_places=2, max_digits=10)
    Cantidad= models.DecimalField(decimal_places=2, max_digits=10)
    SubTota= models.DecimalField(decimal_places=2, max_digits=15)
    IdPresupuestoViviDatGen=models.ForeignKey(PresupuestoViviDatGen, on_delete=models.CASCADE)

    class Meta:
        verbose_name='PresupuestoViviManObr'
        verbose_name_plural='PresupuestoViviManObrs'
        db_table= 'PresupuestoViviManObr'

class PresupuestoViviTot(models.Model):
    Id= models.AutoField(primary_key=True)
    Materiales= models.DecimalField(decimal_places=2, max_digits=15)
    ManoObra= models.DecimalField(decimal_places=2, max_digits=15)
    Transporte= models.DecimalField(decimal_places=2, max_digits=10)
    SolucionSani= models.DecimalField(decimal_places=2, max_digits=10)
    KitEmer= models.DecimalField(decimal_places=2, max_digits=10)
    Herramientas= models.DecimalField(decimal_places=2, max_digits=10)
    TotalCostDir= models.DecimalField(decimal_places=2, max_digits=15)
    IdPresupuestoViviDatGen=models.ForeignKey(PresupuestoViviDatGen, on_delete=models.CASCADE)

    class Meta:
        verbose_name='PresupuestoViviTot'
        verbose_name_plural='PresupuestoViviTots'
        db_table= 'PresupuestoViviTot'


# para obras adicionales 
class PresupuestoViviDatGenObr(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha= models.DateField(null=False)
    TipoObra= models.CharField(max_length=100)
    CostoObra= models.DecimalField(decimal_places=2, max_digits=10)
    SolucionSan= models.DecimalField(decimal_places=2, max_digits=10)
    TotalObraAdi= models.DecimalField(decimal_places=2, max_digits=15)
    IdPresupuestoViviDatGen=models.ForeignKey(PresupuestoViviDatGen, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='PresupuestoViviDatGenObr'
        verbose_name_plural='PresupuestoViviDatGenObrs'
        db_table= 'PresupuestoViviDatGenObr'
        

class PresupuestoViviMatObr(models.Model):
    Id= models.AutoField(primary_key=True)
    Cantidad= models.DecimalField(decimal_places=2, max_digits=10)
    PrecioUnit= models.DecimalField(decimal_places=2, max_digits=10)
    SubTota= models.DecimalField(decimal_places=2, max_digits=15)
    IdMateriales=models.ForeignKey(Materiales, on_delete=models.CASCADE)
    IdPresupuestoViviDatGenObr=models.ForeignKey(PresupuestoViviDatGenObr, on_delete=models.CASCADE)

    class Meta:
        verbose_name='PresupuestoViviMatObr'
        verbose_name_plural='PresupuestoViviMatObrs'
        db_table= 'PresupuestoViviMatObr'

class PresupuestoViviManObrObr(models.Model):
    Id= models.AutoField(primary_key=True)
    Descripcion= models.CharField(max_length=150)
    Unidad= models.CharField(max_length=10)
    PrecioUnit= models.DecimalField(decimal_places=2, max_digits=10)
    Cantidad= models.DecimalField(decimal_places=2, max_digits=10)
    SubTota= models.DecimalField(decimal_places=2, max_digits=15)
    IdPresupuestoViviDatGenObr=models.ForeignKey(PresupuestoViviDatGenObr, on_delete=models.CASCADE)

    class Meta:
        verbose_name='PresupuestoViviManObrObr'
        verbose_name_plural='PresupuestoViviManObrObrs'
        db_table= 'PresupuestoViviManObrObr'

