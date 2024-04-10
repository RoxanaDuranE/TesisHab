from django.db import models
from SolicitudesApp.models import*

# Create your models here.

class ListaCheq(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha=models.DateField(null=False) # la fecha no debe ir vacia
    SolicitudCred= models.CharField(max_length=3, null=True)
    FotocopiaDui= models.CharField(max_length=3, null=True)
    RecibosAgua= models.CharField(max_length=3, null=True)
    RecibosLuz= models.CharField(max_length=3, null=True)
    RecibosTele= models.CharField(max_length=3, null=True)
    ReferenciaCred= models.CharField(max_length=3, null=True)
    ConstanciaEmpl= models.CharField(max_length=3, null=True)
    TacoIsss= models.CharField(max_length=3, null=True)
    AnalisisEcon= models.CharField(max_length=3, null=True)
    Balance= models.CharField(max_length=3, null=True)
    BalanceResu= models.CharField(max_length=3, null=True)
    CopiaDuiFia= models.CharField(max_length=3, null=True)
    RecibosAguaFia= models.CharField(max_length=3, null=True)
    RecibosLuzFia= models.CharField(max_length=3, null=True)
    ConstanciaEmplFia= models.CharField(max_length=3, null=True)
    ReferenciaCredFia= models.CharField(max_length=3, null=True)
    InspeccionTecn= models.CharField(max_length=3, null=True)
    PresupuestoCons= models.CharField(max_length=3, null=True)
    CertificadoExtr= models.CharField(max_length=3, null=True)
    CarenciaBien= models.CharField(max_length=3, null=True)
    FotocopiaEscr= models.CharField(max_length=3, null=True)
    DeclaracionSalu= models.CharField(max_length=3, null=True)
    InformeDico= models.CharField(max_length=3, null=True)
    DocumentoSopoIng= models.CharField(max_length=3, null=True)
    DocumentoReme= models.CharField(max_length=3, null=True)
    CancelacionesPresEst= models.CharField(max_length=3, null=True)
    Finiquitos= models.CharField(max_length=3, null=True)
    HojaAproCre= models.CharField(max_length=3, null=True)
    CartaElabMut= models.CharField(max_length=3, null=True)
    ReciboPagoPri= models.CharField(max_length=3, null=True)
    OrdenDeseIrr= models.CharField(max_length=3, null=True)
    PermisoCons= models.CharField(max_length=3, null=True)
    CartaEntrCosdes= models.CharField(max_length=3, null=True)
    FotocopiaMutu= models.CharField(max_length=3, null=True)
    GestionCobr= models.CharField(max_length=3, null=True)
    Estado= models.CharField(max_length=10)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)

    class Meta:
        verbose_name='ListaCheq'
        verbose_name_plural='ListaCheqs'
        db_table= 'ListaCheq'


