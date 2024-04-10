from django.db import connections
from django.db import models
from DireccionApp.models import *
from SolicitudesApp.models import Solicitud

# Create your models here.
class Agencia(models.Model):
    Id= models.AutoField(primary_key=True)
    Nombre= models.CharField(max_length=25)
    Direccion= models.CharField(max_length=150)
    Telefono= models.CharField(max_length=9)
    TelefonoDos= models.CharField(max_length=9)
    Departamento= models.CharField(max_length=15)
    Municipio= models.CharField(max_length=22)
    Distrito=models.CharField(max_length=28)
    Estado=models.IntegerField()

    class Meta:
        verbose_name='Agencia'
        verbose_name_plural='Agencias'
        db_table= 'Agencia'

class Salario(models.Model):
    Id= models.AutoField(primary_key=True)
    TipoSala=models.CharField(max_length=65)
    SalarioMaxi= models.DecimalField(decimal_places=2, max_digits=10)
    SalarioMini= models.DecimalField(decimal_places=2, max_digits=10)
    FechaInic=models.DateField(null=False)
    FechaFina= models.DateField(null=True, blank=True) #permite q la fecha quede vacia
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='Salario'
        verbose_name_plural='Salarios'
        db_table= 'Salario'

class Ocupacion(models.Model):
    Id= models.AutoField(primary_key=True)
    Nombre= models.CharField(max_length=50)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='Ocupacion'
        verbose_name_plural='Ocupacions'
        db_table= 'Ocupacion'

class ZonaAgen(models.Model):
    Id=models.AutoField(primary_key=True)
    NombreZona=models.CharField(max_length=25)
    IdAgencia=models.ForeignKey(Agencia, on_delete=models.CASCADE)

    class Meta:
        verbose_name='ZonaAgen'
        verbose_name_plural='ZonaAgens'
        db_table= 'ZonaAgen'

    def __str__(self) :
        return self.NombreZona

#es tabla pueba  
class Zona(models.Model):
    Id=models.AutoField(primary_key=True)
    IdZonaAgen=models.ForeignKey(ZonaAgen, on_delete=models.CASCADE)
    IdDistrito=models.ForeignKey(Distrito, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Zona'
        verbose_name_plural='Zonas'
        db_table= 'Zona'

class DocumentosClie(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha = models.DateTimeField(auto_now = True)
    Archivo= models.FileField(upload_to = "documentos/")
    NombreDocu = models.CharField(max_length=30)  
    IdSolicitud=models.ForeignKey('SolicitudesApp.Solicitud', on_delete=models.CASCADE)

    class Meta:
        verbose_name='DocumentosClie'
        verbose_name_plural='DocumentosClies'
        db_table= 'DocumentosClie'

class SolicitudInscSegEnf(models.Model):
    Id= models.AutoField(primary_key=True)
    NombreEnfe= models.CharField(max_length=50)
    Estado= models.CharField(max_length=10)
    Personal= models.CharField(max_length=3) # para difernciar la enfermedad adicional que agrego el cliente
    
    class Meta:
        verbose_name='SolicitudInscSegEnf'
        verbose_name_plural='SolicitudInscSegEnfs'
        db_table= 'SolicitudInscSegEnf'

class Materiales(models.Model):
    Id= models.AutoField(primary_key=True)
    Nombre= models.CharField(max_length=100)
    Descripcion= models.CharField(max_length=100)
    Unidad= models.CharField(max_length=10)
    Estado= models.CharField(max_length=10)
    
    class Meta:
        verbose_name='Materiales'
        verbose_name_plural='Materialess'
        db_table= 'Materiales'

class Infraestructura(models.Model):
    Id= models.AutoField(primary_key=True)
    Nombre= models.CharField(max_length=40)
    Tipo= models.CharField(max_length=30)
    TipoLoteMej= models.CharField(max_length=8)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='Infraestructura'
        verbose_name_plural='Infraestructuras'
        db_table= 'Infraestructura'

class TipoOper(models.Model):
    Id= models.AutoField(primary_key=True)
    Nombre= models.CharField(max_length=25)
    Estado= models.CharField(max_length=10)
  
    class Meta:
        verbose_name='TipoOper'
        verbose_name_plural='TipoOpers'
        db_table= 'TipoOper'

class TasaInte(models.Model):
    Id=models.AutoField(primary_key=True)
    NumeroCred=models.CharField(max_length=50)
    Interes=models.IntegerField()
    Estado=models.IntegerField()

    class Meta:
        verbose_name='TasaInte'
        verbose_name_plural='TasaInte'
        db_table= 'TasaInte'

class Alternativa(models.Model):
      Id=models.AutoField(primary_key=True)
      Alternativa=models.CharField(max_length=50)
      MontoMini=models.DecimalField(decimal_places=2, max_digits=10)
      MontoMaxi=models.DecimalField(decimal_places=2, max_digits=10)
      Plazo=models.IntegerField()
      PlazoMese=models.IntegerField()
      IdTasaInte=models.ForeignKey(TasaInte, on_delete=models.CASCADE)
      Estado=models.IntegerField()

      class Meta:
         verbose_name='Alternativa'
         verbose_name_plural='Alternativas'
         db_table= 'Alternativa'

class RangoFina(models.Model):#Rango de financiamiento
    Id=models.AutoField(primary_key=True)
    VecesFina=models.DecimalField(max_digits=5, decimal_places=2)
    MontoMini=models.DecimalField(max_digits=8, decimal_places=2)
    MontoMaxi=models.DecimalField(max_digits=8, decimal_places=2)
    IdAlternativa=models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    IdSalario=models.ForeignKey(Salario, on_delete=models.CASCADE)
    
    class Meta:
         verbose_name='RangoFina'
         verbose_name_plural='RangoFina'
         db_table= 'RangoFina'

class ModeloVivi(models.Model): 
    Id= models.AutoField(primary_key=True)
    TipoVivi = models.CharField(max_length=15)  
    Modelo= models.FileField(upload_to = "documentos/")
    MontoCons= models.DecimalField(decimal_places=2, max_digits=15)
    Descripcion=models.CharField(max_length=300)

    class Meta:
        verbose_name='ModeloVivi'
        verbose_name_plural='ModeloVivis'
        db_table= 'ModeloVivi'