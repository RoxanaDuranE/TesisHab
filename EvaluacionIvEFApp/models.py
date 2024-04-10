from django.db import models
from ClienteApp.models import *

# Create your models here.

class EgresosFami(models.Model):
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
    Estado=models.IntegerField()
    IdPerfil= models.ForeignKey(Perfil, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name='EgresosFami'
        verbose_name_plural='EgresosFamis'
        db_table= 'EgresosFami'

class IngresosFami(models.Model):
    Id= models.AutoField(primary_key=True)
    Familiar= models.DecimalField(decimal_places=2, max_digits=10)
    OtrosIngr= models.DecimalField(decimal_places=2, max_digits=10)
    TotalIngr=models.DecimalField(decimal_places=2, max_digits=15)
    IdEgresosFami= models.ForeignKey(EgresosFami, on_delete=models.CASCADE)
      
    class Meta:
        verbose_name='IngresosFami'
        verbose_name_plural='IngresosFamis'
        db_table= 'IngresosFami'

class CapacidadPagoFam(models.Model):
    Id= models.AutoField(primary_key=True)
    PorcentajeEnde= models.CharField(max_length=8)
    Disponible= models.DecimalField(decimal_places=2, max_digits=15)
    PorcentajeDisp= models.CharField(max_length=8)
    Cuota=models.DecimalField(decimal_places=2, max_digits=15)
    PorcentajeCuot= models.CharField(max_length=8)
    Superavit= models.DecimalField(decimal_places=2, max_digits=15)
    Deficit=models.DecimalField(decimal_places=2, max_digits=15)
    Estado= models.CharField(max_length=10)
    IdEgresosFami= models.ForeignKey(EgresosFami, on_delete=models.CASCADE)   
    
    class Meta:
        verbose_name='CapacidadPagoFam'
        verbose_name_plural='CapacidadPagoFams'
        db_table= 'CapacidadPagoFam'

class BienesHoga(models.Model):
    Id= models.AutoField(primary_key=True)
    Numero= models.CharField(max_length=10,null=True)
    DescripcionBien= models.CharField(max_length=100,null=True)
    PrecioComp= models.DecimalField(decimal_places=2, max_digits=10,null=True)
    CuotaMens=models.DecimalField(decimal_places=2, max_digits=10,null=True)
    IdEgresosFami= models.ForeignKey(EgresosFami, on_delete=models.CASCADE)   
    
    class Meta:
        verbose_name='BienesHoga'
        verbose_name_plural='BienesHogas'
        db_table= 'BienesHoga'

