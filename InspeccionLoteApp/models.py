from django.db import models
from ConfiguracionApp.models import *
from SolicitudesApp.models import *

# Create your models here.
class InspeccionLote(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha= models.DateField(null=False)
    Hora= models.CharField(max_length=15)
    TelefonoPrim= models.CharField(max_length=9)
    TelefonoSegu= models.CharField(max_length=9)
    TerceraEdad= models.CharField(max_length=5)
    Adultos= models.CharField(max_length=5)
    Ninos= models.CharField(max_length=5)
    PersonaDisc= models.CharField(max_length=5)
    PropietarioTerr= models.CharField(max_length=100)
    Latitud= models.CharField(max_length=50)
    Longitud= models.CharField(max_length=50)
    Inmueble= models.CharField(max_length=8)
    ExisteOtraViv= models.CharField(max_length=3)
    TerrenoAgri= models.CharField(max_length=3)
    AnchoConsViv= models.CharField(max_length=8)
    LargoConsViv= models.CharField(max_length=8)
    AreaConsViv= models.CharField(max_length=10)
    AnchoAmplFut= models.CharField(max_length=8)
    LargoAmplFut= models.CharField(max_length=8)
    AreaAmplFut= models.CharField(max_length=10)
    IdSolicitud= models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='InspeccionLote'
        verbose_name_plural='InspeccionLotes'
        db_table= 'InspeccionLote'


class InspeccionLoteConInfSanSerRie(models.Model):
    Id= models.AutoField(primary_key=True)
    IdInfraestructura=models.ForeignKey(Infraestructura, on_delete=models.CASCADE)
    Existe= models.CharField(max_length=3)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='InspeccionLoteConInfSanSerRie'
        verbose_name_plural='InspeccionLoteConInfSanSerRies'
        db_table= 'InspeccionLoteConInfSanSerRie'

class RiesgosInspLot(models.Model):
    Id= models.AutoField(primary_key=True)
    DistanciaTalu= models.CharField(max_length=8)
    DistanciaRiosCer= models.CharField(max_length=8)
    DistanciaLadeCer= models.CharField(max_length=8)
    DistanciaTorrAnt= models.CharField(max_length=8)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='RiesgosInspLot'
        verbose_name_plural='RiesgosInspLots'
        db_table= 'RiesgosInspLot'
    
class ComentariosObseInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    Comentarios= models.CharField(max_length=200)
    Observaciones= models.CharField(max_length=200)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='ComentariosObseInsLot'
        verbose_name_plural='ComentariosObseInsLots'
        db_table= 'ComentariosObseInsLot'

class ViasAcceInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    TipoVias= models.CharField(max_length=30)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='ViasAcceInsLot'
        verbose_name_plural='ViasAcceInsLots'
        db_table= 'ViasAcceInsLot'  
        
class FactibilidadInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    Detalle= models.CharField(max_length=35)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='FactibilidadInsLot'
        verbose_name_plural='FactibilidadInsLots'
        db_table= 'FactibilidadInsLot'

class DescripcionProyInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    ModeloViviCon= models.CharField(max_length=20)
    SolucionSaniPro= models.CharField(max_length=100)
    ObrasAdicCon= models.CharField(max_length=100)
    ObservacionesTecn= models.CharField(max_length=200)
    ActividadRespFia= models.CharField(max_length=300)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='DescripcionProyInsLot'
        verbose_name_plural='DescripcionProyInsLots'
        db_table= 'DescripcionProyInsLot'

class ResponsabilidadSoliInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    MojonesLote= models.CharField(max_length=3)
    LinderosLote= models.CharField(max_length=3)
    ResguardoMate= models.CharField(max_length=3)
    AuxiliaresCons= models.CharField(max_length=3)
    AguaPota= models.CharField(max_length=3)
    EnergiaElec= models.CharField(max_length=3)
    IdInspeccionLote=models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='ResponsabilidadSoliInsLot'
        verbose_name_plural='ResponsabilidadSoliInsLots'
        db_table= 'ResponsabilidadSoliInsLot'

# para primera inspección
class PrimeraInspLot(models.Model):
    Id= models.AutoField(primary_key=True)
    NumeroInsp= models.CharField(max_length=8)
    Fecha= models.DateField(null=False)
    Esquema= models.FileField(upload_to = "documentos/", blank=True)
    Ubicacion = models.FileField(upload_to="documentos/", blank=True)
    IdInspeccionLote= models.ForeignKey(InspeccionLote, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='PrimeraInspLot'
        verbose_name_plural='PrimeraInspLots'
        db_table= 'PrimeraInspLot'

class ImagenPrimInsLot(models.Model):
    Id= models.AutoField(primary_key=True)
    ReporteFoto= models.FileField(upload_to="documentos/", blank=True) 
    IdPrimeraInspLot= models.ForeignKey(PrimeraInspLot, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='ImagenPrimInsLot'
        verbose_name_plural='ImagenPrimInsLots'
        db_table= 'ImagenPrimInsLot'

