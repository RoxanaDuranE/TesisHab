from django.db import models
from ClienteApp.models import *

# Create your models here.
class BalanceSituMic(models.Model):
    Id= models.AutoField(primary_key=True)
    TipoNego= models.CharField(max_length=50)
    Estado = models.IntegerField()## Estado para saber que proceso lleva y si se desabilita por dicom
    IdPerfil= models.ForeignKey(Perfil, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name='BalanceSituMic'
        verbose_name_plural='BalanceSituMics'
        db_table= 'BalanceSituMic'

class ActivoBalaSit(models.Model):
    Id= models.AutoField(primary_key=True)
    TotalCircAct= models.DecimalField(decimal_places=2, max_digits=15)
    Caja= models.DecimalField(decimal_places=2, max_digits=15)
    Bancos= models.DecimalField(decimal_places=2, max_digits=15)
    CuentasPorCob= models.DecimalField(decimal_places=2, max_digits=15)
    Inventarios=models.DecimalField(decimal_places=2, max_digits=15)
    TotalFijoAct= models.DecimalField(decimal_places=2, max_digits=15)
    Mobiliario= models.DecimalField(decimal_places=2, max_digits=15)
    Terrenos=models.DecimalField(decimal_places=2, max_digits=15)
    Vehiculos=models.DecimalField(decimal_places=2, max_digits=15)
    TotalActi=models.DecimalField(decimal_places=2, max_digits=15)
    IdBalanceSituMic= models.ForeignKey(BalanceSituMic, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name='ActivoBalaSit'
        verbose_name_plural='ActivoBalaSits'
        db_table= 'ActivoBalaSit'

class PasivoBalaSit(models.Model):
    Id= models.AutoField(primary_key=True)
    TotalCircPas=models.DecimalField(decimal_places=2, max_digits=15)
    Proveedores=models.DecimalField(decimal_places=2, max_digits=15)
    CuentasPorPag=models.DecimalField(decimal_places=2, max_digits=15)
    PrestamosCortPla=models.DecimalField(decimal_places=2, max_digits=15)
    FijoPasi=models.DecimalField(decimal_places=2, max_digits=15)
    PrestamosLargPla=models.DecimalField(decimal_places=2, max_digits=15)
    TotalPasi=models.DecimalField(decimal_places=2, max_digits=15)
    Patrimonio=models.DecimalField(decimal_places=2, max_digits=15)
    Capital=models.DecimalField(decimal_places=2, max_digits=15) #  decimal_places=2, lo cual indica que queremos que se guarden dos decimales después del punto. También hemos establecido max_digits=8, lo cual indica que el campo puede tener hasta 8 dígitos en total
    PasivoMasPat=models.DecimalField(decimal_places=2, max_digits=15)
    IdBalanceSituMic= models.ForeignKey(BalanceSituMic, on_delete=models.CASCADE)     
    
    class Meta:
        verbose_name='PasivoBalaSit'
        verbose_name_plural='PasivoBalaSits'
        db_table= 'PasivoBalaSit'

class EstadoResuMic(models.Model):
    Id= models.AutoField(primary_key=True)
    VentasTota= models.DecimalField(decimal_places=2, max_digits=15)
    CostoVent= models.DecimalField(decimal_places=2, max_digits=15)
    UtilidadBrut= models.DecimalField(decimal_places=2, max_digits=15)
    GastosGral=models.DecimalField(decimal_places=2, max_digits=15)
    Transporte= models.DecimalField(decimal_places=2, max_digits=15)
    Servicios= models.DecimalField(decimal_places=2, max_digits=15)
    Impuestos=models.DecimalField(decimal_places=2, max_digits=15)
    Alquiler=models.DecimalField(decimal_places=2, max_digits=15)
    CuotaPres=models.DecimalField(decimal_places=2, max_digits=15)
    ImprevistosEstaRes=models.DecimalField(decimal_places=2, max_digits=15)
    UtilidadNeta=models.DecimalField(decimal_places=2, max_digits=15)
    Mensual=models.DecimalField(decimal_places=2, max_digits=15)
    IdBalanceSituMic= models.ForeignKey(BalanceSituMic, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name='EstadoResuMic'
        verbose_name_plural='EstadoResuMics'
        db_table= 'EstadoResuMic'

class EgresoFlujMic(models.Model):
    Id= models.AutoField(primary_key=True)
    Alimentacion= models.DecimalField(decimal_places=2, max_digits=10)
    Educacion= models.DecimalField(decimal_places=2, max_digits=10)
    Transporte= models.DecimalField(decimal_places=2, max_digits=10)
    Salud= models.DecimalField(decimal_places=2, max_digits=10)
    Afp=models.DecimalField(decimal_places=2, max_digits=10)
    Servicios= models.DecimalField(decimal_places=2, max_digits=10)
    Alquiler= models.DecimalField(decimal_places=2, max_digits=10)
    PorcentajePlan=models.DecimalField(decimal_places=2, max_digits=10)
    PorcentajeVent=models.DecimalField(decimal_places=2, max_digits=10)
    PorcentajeHplhes=models.DecimalField(decimal_places=2, max_digits=10)
    OtrosDesc=models.DecimalField(decimal_places=2, max_digits=10)
    Recreacion=models.DecimalField(decimal_places=2, max_digits=10)
    Imprevistos=models.DecimalField(decimal_places=2, max_digits=10)
    Total=models.DecimalField(decimal_places=2, max_digits=15)
    IdBalanceSituMic= models.ForeignKey(BalanceSituMic, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name='EgresoFlujMic'
        verbose_name_plural='EgresoFlujMics'
        db_table= 'EgresoFlujMic'

class IngresoFlujMic(models.Model):
    Id= models.AutoField(primary_key=True)
    Negocio= models.DecimalField(decimal_places=2, max_digits=15)
    Remesas= models.DecimalField(decimal_places=2, max_digits=10)
    TotalIngrMic=models.DecimalField(decimal_places=2, max_digits=15)
    IdEgresoFlujMic= models.ForeignKey(EgresoFlujMic, on_delete=models.CASCADE)
      
    class Meta:
        verbose_name='IngresoFlujMic'
        verbose_name_plural='IngresoFlujMics'
        db_table= 'IngresoFlujMic'

class CapacidadPagoMic(models.Model):
    Id= models.AutoField(primary_key=True)
    PorcentajeEnde= models.CharField(max_length=8)
    Disponible= models.DecimalField(decimal_places=2, max_digits=15)
    PorcentajeDisp= models.CharField(max_length=8)
    Cuota=models.DecimalField(decimal_places=2, max_digits=15)
    PorcentajeCuot= models.CharField(max_length=8)
    Superavit= models.DecimalField(decimal_places=2, max_digits=15)
    Deficit=models.DecimalField(decimal_places=2, max_digits=15)
    Estado= models.CharField(max_length=10)
    IdEgresoFlujMic= models.ForeignKey(EgresoFlujMic, on_delete=models.CASCADE)   
    
    class Meta:
        verbose_name='CapacidadPagoMic'
        verbose_name_plural='CapacidadPagoMics'
        db_table= 'CapacidadPagoMic'



