from django.db import models
from SolicitudesApp.models import *
from ConfiguracionApp.models import *


# Create your models here.
class DeclaracionJuraCli(models.Model):
    Id= models.AutoField(primary_key=True)  
    NombrePersNat=models.CharField(max_length=100)
    DuiPersNat=models.CharField(max_length=12)  
    IdTipoOper= models.ForeignKey(TipoOper, on_delete=models.CASCADE)  
    NumeroCred= models.CharField(max_length=20)
    Monto= models.CharField(max_length=10)
    Plazo= models.CharField(max_length=10)
    Cuota= models.CharField(max_length=10)
    FormaPago= models.CharField(max_length=15)
    CanceladoAcueCuo= models.CharField(max_length=3)
    RealizarPagoAdi= models.CharField(max_length=3)
    ProcedenciaFond= models.CharField(max_length=30, null=True)
    IdSolicitud= models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='DeclaracionJuraCli'
        verbose_name_plural='DeclaracionJuraClis'
        db_table= 'DeclaracionJuraCli'

class DeclaracionActiEco(models.Model):
    Id= models.AutoField(primary_key=True)
    EmpleadoEn= models.CharField(max_length=50)
    ProfecionalInde=models.CharField(max_length=50, null=True)
    ConocimientosEn= models.CharField(max_length=50, null=True)
    EmpresarioEn= models.CharField(max_length=50, null=True)
    EspecificarOtraAct= models.CharField(max_length=40, null=True)
    IdDeclaracionJuraCli= models.ForeignKey(DeclaracionJuraCli, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='DeclaracionActiEco'
        verbose_name_plural='DeclaracionActiEcos'
        db_table= 'DeclaracionActiEco'

class DeclaracionJiroNeg(models.Model):
    Id= models.AutoField(primary_key=True)
    Empresa= models.CharField(max_length=50, null=True)
    IndustriaDe=models.CharField(max_length=50, null=True)
    ComercioDe= models.CharField(max_length=50, null=True)
    EspecificarOtro= models.CharField(max_length=40, null=True)
    IdDeclaracionJuraCli= models.ForeignKey(DeclaracionJuraCli, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='DeclaracionJiroNeg'
        verbose_name_plural='DeclaracionJiroNegs'
        db_table= 'DeclaracionJiroNeg'



