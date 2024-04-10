from django.db import models
from SolicitudesApp.models import *
from ConfiguracionApp.models import *

# Create your models here.
class SolicitudInscSeg(models.Model):
    Id= models.AutoField(primary_key=True)
    MontosAsegAnt= models.DecimalField(decimal_places=2, max_digits=10)
    NuevoMontAse= models.DecimalField(decimal_places=2, max_digits=10)
    MontoTotaAse= models.DecimalField(decimal_places=2, max_digits=10)
    Plazo= models.CharField(max_length=10)
    Garantia=models.CharField(max_length=50)
    Estatura= models.CharField(max_length=5)
    Peso= models.CharField(max_length=10)
    DesignoBene= models.CharField(max_length=28)
    IdSolicitud= models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='SolicitudInscSeg'
        verbose_name_plural='SolicitudInscSegs'
        db_table= 'SolicitudInscSeg'

class SolicitudInscSegPad(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitudInscSegEnf= models.ForeignKey(SolicitudInscSegEnf, on_delete=models.CASCADE)
    IdPerfil= models.ForeignKey(Perfil, on_delete=models.CASCADE)
    FechaPade=models.DateField(null=True, blank=True)
    TratamientoReci=models.CharField(max_length=100)
    SituacionActu=models.CharField(max_length=15)
    Estado= models.CharField(max_length=10)
      
    class Meta:
        verbose_name='SolicitudInscSegPad'
        verbose_name_plural='SolicitudInscSegPads'
        db_table= 'SolicitudInscSegPad'

class SolicitudInscSegDefAmpDefFis(models.Model):
    Id= models.AutoField(primary_key=True)
    TieneDefoAmpDefFis=models.CharField(max_length=3)
    DetallesDefoAmpDefFis=models.CharField(max_length=50)
    FumaCigaPip=models.CharField(max_length=3)
    CuantosDia=models.CharField(max_length=5)
    BebidasAlco=models.CharField(max_length=3)
    FrecuenciaBebiAlc=models.CharField(max_length=15)
    TratamientoMedi=models.CharField(max_length=3)
    DetalleTratMed=models.CharField(max_length=50)
    PracticaActiDep=models.CharField(max_length=3)
    ClaseActiDep=models.CharField(max_length=25)
    FrecuenciaActiDep=models.CharField(max_length=25)
    SeguroDese=models.CharField(max_length=3)
    IdSolicitudInscSeg= models.ForeignKey(SolicitudInscSeg, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='SolicitudInscSegDefAmpDefFis'
        verbose_name_plural='SolicitudInscSegDefAmpDefFiss'
        db_table= 'SolicitudInscSegDefAmpDefFis'

