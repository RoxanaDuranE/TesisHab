from django.db import models
from ConfiguracionApp.models import *
from ClienteApp.models import Perfil

# Create your models here.
class Solicitud(models.Model):
    Id= models.AutoField(primary_key=True)
    TipoObra=models.CharField(max_length=10)
    Fecha=models.DateField(null=False)
    Numero=models.CharField(max_length=12)
    Comunidad=models.CharField(max_length=50)
    Area=models.CharField(max_length=8)
    Tipo=models.CharField(max_length=8) # si la solicitud es micro o natural
    TipoIngr=models.CharField(max_length=8,null=True)# solo para natural, tipo empleo o remesa
    Estado=models.CharField(max_length=12)
    Observaciones=models.CharField(max_length=300, null=True)
    EstadoSoli=models.IntegerField(null=True)
    IdPerfil=models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Solicitud'
        verbose_name_plural='Solicitudes'
        db_table= 'Solicitud'

class DatosPers(models.Model): # para cliente
      Id= models.AutoField(primary_key=True)      
      LugarDuiCli=models.CharField(max_length=30)
      FechaDuiCli=models.DateField()
      LugarNaciCli=models.CharField(max_length=30)
      EstadoCiviCli=models.CharField(max_length=30)
      GeneroClie=models.CharField(max_length=10)
      EstadoClie= models.CharField(max_length=2)
      IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
      EstadoSoli=models.IntegerField(null=True)

      class Meta:
            verbose_name='DatosPers'
            verbose_name_plural='DatosPerss'
            db_table= 'DatosPers'

class DatosPersFia(models.Model): # para tipo conyuge o codeudor
       Id= models.AutoField(primary_key=True)
       Tipo=models.CharField(max_length=10,null=True)
       NombreFiad= models.CharField(max_length=50)
       ApellidoFiad= models.CharField(max_length=50)
       DuiFiad= models.CharField(max_length=12)
       LugarDuiFia= models.CharField(max_length=30)
       FechaDuiFia=models.DateField(null=False)
       FechaNaciFia=models.DateField(null=False)
       LugarNaciFia= models.CharField(max_length=30)
       EdadFiad= models.IntegerField()      
       EstadoCiviFiad=models.CharField(max_length=30)
       GeneroFiad=models.CharField(max_length=10)
       IdOcupacionFia= models.ForeignKey('ConfiguracionApp.Ocupacion', on_delete=models.CASCADE)
       IdOcupacionDUIFia= models.ForeignKey('ConfiguracionApp.Ocupacion',null=True, on_delete=models.CASCADE, related_name='ocupacion_DUI_fiador')
       EstadoFiad= models.IntegerField()
       IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
       EstadoSoli=models.IntegerField(null=True)

       class Meta:
            verbose_name='DatosPersFia'
            verbose_name_plural='DatosPersFias'
            db_table= 'DatosPersFia'

class GrupoFami(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Nombre= models.CharField(max_length=100)
    Edad= models.CharField(max_length=5)
    Salario= models.DecimalField(max_digits=10, decimal_places=2)
    Trabajo=models.CharField(max_length=50)
    Parentesco=models.CharField(max_length=30)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='GrupoFami'
        verbose_name_plural='GrupoFami'
        db_table= 'GrupoFami'

class Domicilio(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Direccion=models.CharField(max_length=150)
    Referencia=models.CharField(max_length=75) 
    Telefono=models.CharField(max_length=9)
    ResideDesd=models.CharField(max_length=10)
    CondicionVivi=models.CharField(max_length=20)
    LugarTrab=models.CharField(max_length=100)
    ActividadMicr=models.CharField(max_length=50, null=True)# para micro
    JefeInme=models.CharField(max_length=100, null=True)#para natural
    TiempoEmprTieFun=models.CharField(max_length=10)
    SalarioIngr=models.DecimalField(max_digits=10, decimal_places=2)
    DireccionTrabMic=models.CharField(max_length=150)
    TelefonoTrabMic=models.CharField(max_length=9)
    Tipo= models.CharField(max_length=12)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='Domicilio'
        verbose_name_plural='Domicilios'
        db_table= 'Domicilio'

class DatosObra(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    IdAlternativa=models.ForeignKey('ConfiguracionApp.Alternativa', on_delete=models.CASCADE)
    Dueno=models.CharField(max_length=100)
    Parentesco=models.CharField(max_length=30)
    DireccionExac=models.CharField(max_length=150)
    IdModeloVivi=models.ForeignKey('ConfiguracionApp.ModeloVivi', on_delete=models.CASCADE)
    DetalleAdic=models.CharField(max_length=80, null=True)
    Presupuesto=models.DecimalField(max_digits=15, decimal_places=2)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='DatosObra'
        verbose_name_plural='DatosObras'
        db_table= 'DatosObra'

class Detalle(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Monto=models.DecimalField(max_digits=10, decimal_places=2)
    Plazo=models.CharField(max_length=10)
    Cuota=models.DecimalField(max_digits=10, decimal_places=2)
    FormaPago=models.CharField(max_length=12)
    FechaPago=models.CharField(max_length=15)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='Detalle'
        verbose_name_plural='Detalles'
        db_table= 'Detalle'

class ExperienciaCred(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Lugar=models.CharField(max_length=25,null=True)
    Monto=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    FechaOtor=models.DateField(null=True)
    Estado=models.CharField(max_length=12,null=True)
    Cuota=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    PoseeExpe=models.BooleanField()
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='ExperienciaCred'
        verbose_name_plural='ExperienciaCreds'
        db_table= 'ExperienciaCred'

class Referencias(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Nombre=models.CharField(max_length=100)
    Parentesco=models.CharField(max_length=30)
    Domicilio=models.CharField(max_length=150)
    Telefono=models.CharField(max_length=9)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='Referencias'
        verbose_name_plural='Referencias'
        db_table= 'Referencias'

class Comentarios(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    ComentarioNeceVivMej=models.CharField(max_length=200)
    ComentarioEvalEst=models.CharField(max_length=200)
    ComentarioGaraOfr=models.CharField(max_length=200)
    EstadoSoli=models.IntegerField(null=True)

    class Meta:
        verbose_name='Comentarios'
        verbose_name_plural='Comentarios'
        db_table= 'Comentarios'

class Medio(models.Model):
    Id= models.AutoField(primary_key=True)
    IdSolicitud=models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    RedesSoci=models.CharField(max_length=15)
    Pvv=models.CharField(max_length=5)
    Referenciado=models.CharField(max_length=15)
    Perifoneo=models.CharField(max_length=10)
    Radio=models.CharField(max_length=6)
    FeriaVivi=models.CharField(max_length=18)
    CampanaProm=models.CharField(max_length=25)
    Otros=models.CharField(max_length=6)
    Especifique=models.CharField(max_length=50)
    EstadoSoli=models.IntegerField(null=True)
    
    class Meta:
        verbose_name='Medio'
        verbose_name_plural='Medios'
        db_table= 'Medio'

