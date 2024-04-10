from django.db import models
from django.db import connections
from ClienteApp.models import *
from SolicitudesApp.models import Solicitud

# Create your models here.

class RangoHist(models.Model):
    Id= models.AutoField(primary_key=True)
    Minimo= models.DecimalField(max_digits=10, decimal_places=2)
    Maximo= models.DecimalField(max_digits=10, decimal_places=2)
    Tipo= models.CharField(max_length=15)
    Porcentaje= models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name='RangoHist'
        verbose_name_plural='RangoHists'
        db_table= 'RangoHist'


class RegistroHist(models.Model):
    Id= models.AutoField(primary_key=True)
    Puntaje= models.DecimalField(max_digits=5, decimal_places=2)
    Fecha= models.DateField(null=False)
    IdRango= models.ForeignKey(RangoHist, on_delete=models.CASCADE)
    IdSolicitud= models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name='RegistroHist'
        verbose_name_plural='RegistroHists'
        db_table= 'RegistroHist'
