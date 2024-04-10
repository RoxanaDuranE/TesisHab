from django.db import models
from ClienteApp.models import *
from SolicitudesApp.models import *

# Create your models here.

class ClienteDatoGen(models.Model):
    Id= models.AutoField(primary_key=True)
    Fecha= models.DateField(null=False)        
    Codigo= models.CharField(max_length=10)  
    CalidadActu= models.CharField(max_length=10)
    NombreConzCli= models.CharField(max_length=100)
    ConocidoComo= models.CharField(max_length=100)
    Nacionalidad=models.CharField(max_length=15)
    DocumentoIden= models.CharField(max_length=5)
    NumeroDocu= models.CharField(max_length=20)
    FechaVencdoc= models.DateField(null=True, blank=True)     
    DireccionDomi= models.CharField(max_length=150)
    CorreoElec= models.CharField(max_length=100)     
    TelefonoCelu=models.CharField(max_length=9)
    TelefonoFijo=models.CharField(max_length=9)
    EstatusProp= models.CharField(max_length=20)
    NombreCony= models.CharField(max_length=100) 
    Estado= models.CharField(max_length=10) 
    IdSolicitud= models.ForeignKey(Solicitud, on_delete=models.CASCADE)

    class Meta:
        verbose_name='ClienteDatoGen'
        verbose_name_plural='ClienteDatoGens'
        db_table= 'ClienteDatoGen'

class ClienteActiEco(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    TipoActi= models.CharField(max_length=15)
    LugarTrab= models.CharField(max_length=150)
    CargoDese= models.CharField(max_length=30)    
    TiempoLabo= models.CharField(max_length=10)
    ProcedenciaFond= models.CharField(max_length=30)
    RangoIngrMen=models.CharField(max_length=20)
    OtrosIngr= models.CharField(max_length=15)
    ProcedenciaOtroIng= models.CharField(max_length=30,null=True)
    Estado= models.CharField(max_length=10) 

    class Meta:
        verbose_name='ClienteActiEco'
        verbose_name_plural='ClienteActiEcos'
        db_table= 'ClienteActiEco'

class ClienteDatoNeg(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    NombreNego= models.CharField(max_length=75)
    ProductoServ= models.CharField(max_length=200)
    DireccionNego= models.CharField(max_length=150)
    FechaInicAct= models.DateField(null=True, blank=True) #  permitirá que el campo sea nulo en la base de datos y también permitirá que se deje en blanco en los formularios.
    RangoIngrMen=models.CharField(max_length=20)
    OtrosIngrMen= models.CharField(max_length=15)
    ProcedenciaOtroIng= models.CharField(max_length=30,null=True)
    Estado= models.CharField(max_length=10) 

    class Meta:
        verbose_name='ClienteDatoNeg'
        verbose_name_plural='ClienteDatoNegs'
        db_table= 'ClienteDatoNeg'

        
class ClienteReciRemFam(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    RecibeReme= models.CharField(max_length=3) 
    NombreRemi= models.CharField(max_length=100,null=True)
    Parentesco= models.CharField(max_length=30,null=True)
    PaisOrig= models.CharField(max_length=15,null=True)
    Monto= models.CharField(max_length=10,null=True) 
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClienteReciRemFam'
        verbose_name_plural='ClienteReciRemFams'
        db_table= 'ClienteReciRemFam'

class ClienteDeclCli(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    ClasificacionCred= models.CharField(max_length=10)
    MontoDeclCli= models.CharField(max_length=10)
    CuotaDeclCli= models.CharField(max_length=10)
    RealizarPagoAdi= models.CharField(max_length=3)
    ProcedenciaPagoAdi=models.CharField(max_length=30,null=True)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClienteDeclCli'
        verbose_name_plural='ClienteDeclClis'
        db_table= 'ClienteDeclCli'

class ClientePersBen(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    NoApli= models.CharField(max_length=3,null=True)
    NombreComp= models.CharField(max_length=100,null=True)
    DireccionPerm= models.CharField(max_length=150,null=True)
    TipoDocuPers= models.CharField(max_length=5,null=True)
    NumeroDocuPers= models.CharField(max_length=20,null=True)
    BeneficiarioPeps= models.CharField(max_length=3,null=True)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClientePersBen'
        verbose_name_plural='ClientePersBens'
        db_table= 'ClientePersBen'

class ClientePerfTra(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    Prestamos= models.CharField(max_length=75,null=True)
    EspecificarOtroPer= models.CharField(max_length=75,null=True)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClientePerfTra'
        verbose_name_plural='ClientePerfTras'
        db_table= 'ClientePerfTra'

class ClientePeps(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    UstedPeps= models.CharField(max_length=3)
    RelacionPeps= models.CharField(max_length=3)
    NombrePeps= models.CharField(max_length=100,null=True)
    PuestoDese= models.CharField(max_length=25,null=True)
    PeriodoGestDes= models.CharField(max_length=20,null=True)
    PeriodoGestHas= models.CharField(max_length=20,null=True)
    Grado=models.CharField(max_length=8,null=True)
    Parentesco=models.CharField(max_length=30,null=True)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClientePeps'
        verbose_name_plural='ClientePepss'
        db_table= 'ClientePepss'

class ClienteParaUsoExc(models.Model):
    Id= models.AutoField(primary_key=True)
    IdClienteDatoGen= models.ForeignKey (ClienteDatoGen, on_delete=models.CASCADE) 
    ValideFirmNomFot= models.CharField(max_length=3)
    VerifiqueDire= models.CharField(max_length=3)
    VerificadoPor= models.CharField(max_length=100)
    CodigoEmpl= models.CharField(max_length=15)
    Estado= models.CharField(max_length=10)

    class Meta:
        verbose_name='ClienteParaUsoExc'
        verbose_name_plural='ClienteParaUsoExcs'
        db_table= 'ClienteParaUsoExc'  