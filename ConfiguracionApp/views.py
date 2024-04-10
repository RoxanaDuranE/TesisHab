import json
from django.shortcuts import render, HttpResponse

# Create your views here.
from email import message
from pyexpat import model
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q


from ConfiguracionApp.models import *
from DireccionApp.models import *
from DeclaracionJurClienteApp.models import *
from DireccionApp.models import *
from InspeccionLoteApp.models import *
from InspeccionMejViviendaApp.models import *
from SolicitudInscripcionSApp.models import *
from PresupuestoApp.models import *
from PresupuestoVApp.models import *
from TesisApp.views import registroBit
from TesisApp.models import *

from django.utils import timezone # para fecha


########################
#  salario
def salario(request):
    return render(request,"ConfiguracionApp/salario.html")

def registrarSalario(request):
    tiposalario = request.POST['tiposalario']
    salariomaximo = request.POST['salariomaximo']
    salariominimo = request.POST['salariominimo']
    fechai = request.POST['fechaI']

    esta = "activo"

    # Verificar si ya existe un salario con el mismo tipo de salario
    vsalario = Salario.objects.filter(TipoSala=tiposalario, Estado=esta).exists()

    if vsalario:
        mensaje = "El tipo de salario ya está registrado"
        messages.warning(request, mensaje)
    else:
        # Verificar si el rango de salario se superpone con otro rango existente
        superpuesto = Salario.objects.filter(
            Q(Estado=esta),
            Q(SalarioMini__lte=salariomaximo, SalarioMaxi__gte=salariominimo) |
            Q(SalarioMini__gte=salariominimo, SalarioMaxi__lte=salariomaximo) |
            Q(SalarioMini__lte=salariomaximo, SalarioMaxi__gte=salariominimo)
        ).exists()

        if superpuesto:
            mensaje = "El rango de salario pertenece a otro rango existente"
            messages.warning(request, mensaje)
        else:
            salario=Salario.objects.create(TipoSala=tiposalario,SalarioMaxi=salariomaximo, SalarioMini=salariominimo,FechaInic=fechai, Estado=esta) 
            
    mensaje="Salario registrado"
    registroBit(request, Actividad=mensaje+" "+ tiposalario, Nivel="Registro")
    messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/salario')


def listaSalario(request):
    listas=Salario.objects.all()
    return render(request, "ConfiguracionApp/listasalario.html", {"salarios":listas})

def salarioB(request, id):

    fecha_actual = timezone.now().date()
    print(fecha_actual)
   
    estad="inactivo"
    # cambia el estado del salario a inactivo
    idsal= Salario.objects.get(Id=id,Estado="activo")
    salv= Salario.objects.get(Id= idsal.Id)
    salv.FechaFina = fecha_actual
    salv.Estado =estad
    salv.save()

    mensaje="El Salario a sido dado de baja"
    registroBit(request, Actividad=mensaje + " "+ salv.TipoSala, Nivel="Desactivacion")
    messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaSalario')

def editarSalario(request, id):
    salario = Salario.objects.get(Id=id)    
    
    return render(request, "ConfiguracionApp/editarSalario.html", {"s":salario})

def modificarSalario(request):
    id = request.POST['ids']
    tiposalario = request.POST['tiposalario']
    salariomaximo = request.POST['salariomaximo']
    salariominimo = request.POST['salariominimo']

    esta = "activo"

    # Obtener el salario actual
    salario_actual = Salario.objects.get(Id=id)

    # Verificar si el tipo de salario se repite, excluyendo el salario actual
    vsalario = Salario.objects.filter(TipoSala=tiposalario, Estado=esta).exclude(Id=id).exists()

    # Verificar si el rango a modificar se superpone con otro rango existente
    superpuesto = Salario.objects.filter(
        Q(Estado=esta),
        ~Q(Id=id),  # Excluye el salario actual
        Q(SalarioMini__lte=salariominimo, SalarioMaxi__gte=salariomaximo) |
        Q(SalarioMini__gte=salariominimo, SalarioMaxi__lte=salariomaximo) |
        Q(SalarioMini__lte=salariomaximo, SalarioMaxi__gte=salariominimo)
    ).exists()

    if vsalario or superpuesto:
        mensaje = "Ese rango de Salario ya existe o pertenece a otro rango"
        messages.warning(request, mensaje)
    else:
        # Actualizar el salario si no hay superposición ni duplicados
        salario_actual.TipoSala = tiposalario
        salario_actual.SalarioMaxi = salariomaximo
        salario_actual.SalarioMini = salariominimo
        salario_actual.save()
        mensaje = "Salario actualizado"
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaSalario')

################################
 # Ocupacion

def ocupacion(request):
    return render(request,"ConfiguracionApp/ocupacion.html")

def registrarOcupacion(request):
    esta="activo"  
    ocupacion=request.POST['ocupacion'].upper() 
   
    oc=Ocupacion.objects.filter(Nombre=ocupacion,Estado=esta).exists()
    
    if oc == True:
            mensaje="la ocupación ya existe"
            messages.warning(request, mensaje)
    else:
        ocup=Ocupacion.objects.create(Nombre=ocupacion,Estado=esta)
        mensaje="Ocupacion registrada"
        registroBit(request, Actividad=mensaje + " "+ ocupacion, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/ocupacion/')

def listaOcupacion(request):
    listao=Ocupacion.objects.all()
    return render(request, "ConfiguracionApp/listaocupacion.html", {"ocupaciones":listao})

def eliminarO(request, id):
    estad="inactivo" 
    p=Perfil.objects.filter(Id=id).exists()
    ocupacion= Ocupacion.objects.get(Id=id)
    if p == True and ocupacion.Estado=="activo":
        ocupacion.Estado =estad
        ocupacion.save()
        mensaje="La ocupación fue dada de baja"
        registroBit(request, Actividad=mensaje + " " + ocupacion.Nombre, Nivel="Desactivar")
        messages.success(request, mensaje)
    else:             
        ocupacion.delete()
        mensaje="Ocupacion eliminada"
        registroBit(request, Actividad=mensaje, Nivel="Eliminacion")
        messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaOcupacion')

def editarOcupacion(request, id):
    linfo=Ocupacion.objects.get(Id=id)  
    return render(request,"ConfiguracionApp/editarOcupacion.html", {"o":linfo})

def ModificarOcupacion(request):
    ido=request.POST['ido']
    ocupacion=request.POST['ocupacion'].upper() 
   
    oc=Ocupacion.objects.filter(Nombre=ocupacion).exists()
    
    if oc == True:
            mensaje="La ocupación ya existe"
            messages.warning(request, mensaje)
    else:
        moc=Ocupacion.objects.get(Id=ido)
        moc.Nombre=ocupacion
        moc.save()
        mensaje="Datos actualizados "
        registroBit(request, Actividad=mensaje +" "+ ocupacion, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaOcupacion/')

######################################################
# asignar agencia # 

def zonaAgencia(request):
    listaragencia=Agencia.objects.filter(Estado=1)
    return render(request,"ConfiguracionApp/zonaAgencia.html",{ "Agencia":listaragencia})

def registrarZona(request):
    nombrezona=request.POST['nombrezona']
    agencia=request.POST['agencia']
    estado=2
    age=Agencia.objects.get(Id=agencia)
    age.Id=agencia
    age.Estado=estado
    age.save()
    consulta=ZonaAgen.objects.filter(NombreZona=nombrezona).exists()
    
    if consulta==True:
        mensaje="El nombre de la zona ya existe"
        messages.warning(request, mensaje)
        return redirect('zonaAgencia')
    else:
        zonaagen= ZonaAgen.objects.create(NombreZona=nombrezona,IdAgencia=age)
        mensaje="Se ha guardado la zona"
        registroBit(request, Actividad=mensaje +" " + nombrezona, Nivel="Registro")
        messages.success(request, mensaje)
        return redirect('zonaAgencia')
    
def mu(request):
    id=request.GET['departamento']
    depto=Departamento.objects.get(Id=id)
    
    muni=Municipio.objects.filter(IdDepartamento=depto, Estado=1)
    return render(request,"ConfiguracionApp/mu.html", {"muni":muni})

def dist(request):    
    idmuni=request.GET['municipio']
    
    idmuni=Municipio.objects.get(Id=idmuni)
    destri=Distrito.objects.filter(IdMunicipio=idmuni, Estado=1)
    
    return render(request,"ConfiguracionApp/dis.html", {"Distrito":destri})
  
## espacio para agragar municipios para cada zona y agencia
def asignarZona(request):
     listarzona=ZonaAgen.objects.all()
     muni=Zona.objects.all()
     listarmuni=Departamento.objects.all()
     #listarmuni=Muni.objects.filter(estado=1)
     listamuni=Municipio.objects.all()
     ran_json = json.dumps(list(listamuni.values()))  # Convertir la lista a JSON

     return render(request,"ConfiguracionApp/asignarZona.html", {"ZonaAgencia":listarzona, "Departamento":listarmuni, "ran_json": ran_json,})
    
 
def registrarZona1(request): 
    idzona=request.POST['zona']
    iddistrito=request.POST['distrito']
    estado=2
    zona=ZonaAgen.objects.get(Id=idzona)
    zona.Id=idzona
    distrito=Distrito.objects.get(Id=iddistrito)
    distrito.Id=iddistrito  
    distrito.Estado=estado
    distrito.save()
    zon= Zona.objects.create(IdZonaAgen=zona,IdDistrito=distrito)
    mensaje="Se ha asignado la zona"
    registroBit(request, Actividad=mensaje, Nivel="Registro")
    messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/asignarZona')

#######################################################
# agencia#

# vista del formulario para registrar agencia
def registroAgencias(request):
    dire = Agencia.objects.only('Municipio','Direccion','Telefono','TelefonoDos')
    try:
        listarDepto=Departamento.objects.all()
    except Departamento.DoesNotExist:
        listarDepto=""  
    return render(request,"ConfiguracionApp/registroAgencia.html",{"dire":dire,"Departamento":listarDepto})

def municipio(request):
    id=request.GET['departamento']
    depto=Departamento.objects.get(NombreDepa=id)
    muni=Municipio.objects.filter(IdDepartamento=depto.Id, Estado=1)
    return render(request,"ConfiguracionApp/municipio.html", {"Muni":muni})

def distri(request):   
    idmuni=request.GET['municipio']
    idmuni=Municipio.objects.get(Id=idmuni)
    destri=Distrito.objects.filter(IdMunicipio=idmuni)
    
    return render(request,"ConfiguracionApp/distrito.html", {"MuniDistrito":destri})


def listarAgencias(request):  
    return render(request,"ConfiguracionApp/listaAgencias.html")

def registrarAgencia(request):
    
    nombre=request.POST['nombre'].upper() 
    direccion=request.POST['direccion']
    telefono=request.POST['telefono']
    telefonodos=request.POST['telefonodos']
    departamento=request.POST['departamento']
    municipio=request.POST['municipio']
    distrito=request.POST['distrito']
    estado=1
    mun=Municipio.objects.get(Id=municipio)
    
    agencia = Agencia.objects.create(Nombre=nombre, Direccion=direccion, Telefono=telefono, 
    TelefonoDos=telefonodos, Departamento=departamento, Municipio=mun.NombreMuni, Distrito=distrito, Estado=estado)
    mensaje="Agencia registrada"
    registroBit(request, Actividad=mensaje, Nivel="Registro")
    messages.success(request, mensaje)
    
    return redirect('listarAgencias')

def listaAgencias(request):
    listAgencias=Agencia.objects.exclude(Direccion='Central')
    return render(request, "ConfiguracionApp/listaAgencias.html", {"agencias":listAgencias})

def editarAgencia(request, idAgencia):
    #print(idAgencia)
    agencia = Agencia.objects.get(Id=idAgencia)
    dire = Agencia.objects.only('Municipio','Direccion','Telefono','TelefonoDos')
    #print(agencia.Distrito)
    idDepto=Departamento.objects.get(NombreDepa=agencia.Departamento)
    idMun=Municipio.objects.get(NombreMuni=agencia.Municipio)
    #print(idDepto)
    try:
        listarDepto=Departamento.objects.all()
    except Departamento.DoesNotExist:
        listarDepto="" 
    try:
        listarMuni=Municipio.objects.filter(IdDepartamento=idDepto.Id)
    except Municipio.DoesNotExist:
        listarMuni=""  
    try:
        listarDist=Distrito.objects.filter(IdMunicipio=idMun.Id)
    except Distrito.DoesNotExist:
        listarDist=""  

    return render(request, "ConfiguracionApp/editarAgencia.html", {"agencia":agencia,"dire":dire,"Departamento":listarDepto,"Municipio":listarMuni,"Distrito":listarDist})

def modificarAgencia(request):
    depas=("Ahuachapán","Cabañas","Chalatenango","Cuscatlán","La Libertad","La Paz","La Unión","Morazán","San Miguel","San Salvador","San Vicente","Santa Ana","Sonsonate","Usulután")
    idAg=request.POST['idAg']
    nombre=request.POST['nombre']
    direccion=request.POST['direccion']
    telefono=request.POST['telefono']
    telefonodos=request.POST['telefonodos']
    departamento=request.POST['departamento']
    municipio=request.POST['municipioe']   
    distrito=request.POST['distritoe']    
    mun=Municipio.objects.get(Id=municipio)
    dis=Distrito.objects.get(Id=distrito)
    

    agencia = Agencia.objects.get(Id=idAg)
    agencia.Nombre=nombre
    agencia.Direccion=direccion
    agencia.Telefono=telefono
    agencia.TelefonoDos=telefonodos
    agencia.Departamento=departamento
    agencia.Municipio=mun.NombreMuni
    agencia.Distrito=dis.Distrito
    agencia.save()
    mensaje="Datos de agencia actualizados"
    registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
    messages.success(request, mensaje)
    return redirect('listarAgencias')


def con(request):
    dire = Agencia.objects.only('Municipio','Direccion')
    return render(request,"ConfiguracionApp/consulta.html",{"dire":dire})

##################################################################

##################################################################
# para registrar enfermedades
def enfermedad(request):
    return render(request,"ConfiguracionApp/registrarEnfermedadesSIS.html")

def registrarEnfermedad(request):
    
    enfermedad=request.POST['enfermedadop'].upper() 
    estadoenf="activo"
    estadop="No"
   
    enf=SolicitudInscSegEnf.objects.filter(NombreEnfe=enfermedad).exists()
    
    if enf == True:
            mensaje="la enfermedad o padecimiento ya existe"
            messages.warning(request, mensaje)
    else:
        enfermedades=SolicitudInscSegEnf.objects.create(NombreEnfe=enfermedad,Estado=estadoenf,Personal=estadop)
        mensaje="Enfermedad registrada"
        registroBit(request, Actividad=mensaje, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/enfermedad/')

def listaEnfermedades(request):
    listae=SolicitudInscSegEnf.objects.all()
    return render(request, "ConfiguracionApp/listaEnfermedades.html", {"enfermedades":listae})

def eliminarE(request, id):
    estad="inactivo" 
    sp=SolicitudInscSegPad.objects.filter(IdSolicitudInscSegEnf=id).exists()
    solEnf= SolicitudInscSegEnf.objects.get(Id=id)
    if sp == True and solEnf.Estado=="activo":
        solEnf.Estado =estad
        solEnf.save()
        mensaje="La Enfermedad fue dada de baja"
        registroBit(request, Actividad=mensaje, Nivel="Desactivacion")
        messages.success(request, mensaje)
    else:             
        solEnf.delete()
        mensaje="Enfermedad eliminada"
        messages.success(request, mensaje)
        registroBit(request, Actividad=mensaje, Nivel="Eliminacion")
    return redirect('/ConfiguracionApp/listaEnfermedades')

def editarEnf(request, id):
    enf=SolicitudInscSegEnf.objects.get(Id=id)  
    return render(request,"ConfiguracionApp/editarEnfermedadesSIS.html", {"enfermedad":enf})

def ModificarE(request):   
    ide=request.POST['ide']
    enfermedad=request.POST['enfermedadop'].upper() 
 
    menf=SolicitudInscSegEnf.objects.get(Id=ide)
    menf.NombreEnfe=enfermedad
    menf.save()
    mensaje="Registro de enfermedad actualizados"
    registroBit(request, Actividad=mensaje + enfermedad, Nivel="Actualizacion")
    messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaEnfermedades/')
###################################################################
###################################################################
# Materiales

def materiales(request):
    return render(request,"ConfiguracionApp/materiales.html")

def registrarMaterial(request):
    nombre=request.POST['nombremt'].upper()
    descripcion=request.POST['descripcionmt'].upper()
    unidad=request.POST['unidadmt'].upper()

    estadomt="activo"
    mat=Materiales.objects.filter(Nombre=nombre,Descripcion=descripcion).exists()
    
    if mat == True:
            mensaje="El material ya existe"
            messages.warning(request, mensaje)
    else:
        material=Materiales.objects.create(Nombre=nombre,Descripcion=descripcion,Unidad=unidad,Estado=estadomt)
        mensaje="Material registrado"
        registroBit(request, Actividad=mensaje + material.Nombre, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/materiales/')

def listaMateriales(request):
    listam=Materiales.objects.all()
    return render(request, "ConfiguracionApp/listaMateriales.html", {"materiales":listam})

def eliminarM(request, id):
    estad="inactivo" 
    pre =PresupuestoMate.objects.filter(IdMateriales=id).exists()
    prev =PresupuestoViviMat.objects.filter(IdMateriales=id).exists()
    mater= Materiales.objects.get(Id=id)
    nomb=mater.Nombre
    if pre == True or prev == True and mater.Estado=="activo":
        mater.Estado =estad
        mater.save()
        mensaje="El material fue dado de baja"
        registroBit(request, Actividad=mensaje + nomb, Nivel="Desactivacion")
        messages.success(request, mensaje)
    else:             
        mater.delete()
        mensaje="Material eliminado"
        registroBit(request, Actividad=mensaje + nomb, Nivel="Eliminacion")
        messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaMateriales')

def editarMat(request, id):
    lmat=Materiales.objects.get(Id=id)  
    return render(request,"ConfiguracionApp/editarMateriales.html", {"material":lmat})

def ModificarMat(request):   
    idm=request.POST['idm']
    nombre=request.POST['nombremt']
    descripcion=request.POST['descripcionmt']
    unidad=request.POST['unidadmt']
    estadomt="activo"

    mat=Materiales.objects.filter(Nombre=nombre,Descripcion=descripcion).exists()
    
    if mat == True:
            mensaje="El material ya existe"
            messages.warning(request, mensaje)
    else:
        mmat=Materiales.objects.get(Id=idm)
        mmat.Nombre=nombre
        mmat.Descripcion=descripcion
        mmat.Unidad=unidad
        mmat.Estado=estadomt
        mmat.save()
        mensaje="Datos Actualizados"
        registroBit(request, Actividad=mensaje + mmat.Nombre, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaMateriales/')


###################################################################
# Infraestructura Lote

def infraestructura(request):
    return render(request,"ConfiguracionApp/infraestructura.html")

def registrarInfraestructura(request):  
    nombre=request.POST['nombreif'].upper()
    tipo=request.POST['tipoif']
    estadoif="activo"
   
    inf=Infraestructura.objects.filter(Nombre=nombre,Tipo=tipo,TipoLoteMej="Lote").exists()
    
    if inf == True:
            mensaje="La infraestructura ya existe"
            messages.success(request, mensaje)
    else:
        infraestructura=Infraestructura.objects.create(Nombre=nombre,Tipo=tipo,TipoLoteMej="Lote",Estado=estadoif)
        mensaje="Infraestructura registrada"
        registroBit(request, Actividad=mensaje, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/infraestructura/')

def listaInfraestructura(request):
    listaif=Infraestructura.objects.filter(TipoLoteMej="Lote",Estado="activo")
    return render(request, "ConfiguracionApp/listaInfraestructura.html", {"infraestructura":listaif})

def eliminarInf(request, id):
    estad="inactivo" 
    inp =InspeccionLoteConInfSanSerRie.objects.filter(IdInfraestructura=id).exists()
    inf= Infraestructura.objects.get(Id=id)
    if inp == True and inf.Estado=="activo":
        inf.Estado =estad
        inf.save()
        mensaje="La Infraestructura fue dada de baja"
        messages.success(request, mensaje)
    else:             
        inf.delete()
        mensaje="Infraestructura eliminada"
        messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaInfraestructura')

def editarInf(request, id):
    linf=Infraestructura.objects.get(Id=id)  
    return render(request,"ConfiguracionApp/editarInfraestructura.html", {"inf":linf})


def ModificarInf(request):  
    idif=request.POST['idif']
    nombre=request.POST['nombreif']
    tipo=request.POST['tipoif']

    inf=Infraestructura.objects.filter(Nombre=nombre,Tipo=tipo,TipoLoteMej="Lote").exists()
    
    if inf == True:
            mensaje="La infraestructura ya existe"
            messages.success(request, mensaje)
    else:  
        minf=Infraestructura.objects.get(Id=idif)
        minf.Nombre=nombre
        minf.Tipo=tipo
        minf.TipoLoteMej="Lote"
        minf.save()
        mensaje="Datos Actualizados"
        registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaInfraestructura/')


###################################################################
# Infraestructura Mejora

def infraestructuram(request):
    return render(request,"ConfiguracionApp/infraestructuraMej.html")

def registrarInfraestructuram(request):
    
    nombre=request.POST['nombreifm'].upper()
    tipo=request.POST['tipoifm']
    estadoifm="activo"
   
    inf=Infraestructura.objects.filter(Nombre=nombre,Tipo=tipo,TipoLoteMej="Mejora").exists()
    
    if inf == True:
            mensaje="La infraestructura ya existe"
            messages.warning(request, mensaje)
    else:
        infraestructura=Infraestructura.objects.create(Nombre=nombre,Tipo=tipo,TipoLoteMej="Mejora",Estado=estadoifm)
        mensaje="Infraestructura registrada"
        registroBit(request, Actividad=mensaje, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/infraestructuram/')

def listaInfraestructuram(request):
    listaif=Infraestructura.objects.filter(TipoLoteMej="Mejora",Estado="activo")
    return render(request, "ConfiguracionApp/listaInfraestructuram.html", {"infraestructura":listaif})

def eliminarInfm(request, id):
    estad="inactivo" 
    inpm =InspeccionMejoEspSerInfRie.objects.filter(IdInfraestructura=id).exists()
    inf= Infraestructura.objects.get(Id=id)
    if inpm == True and inf.Estado=="activo":
        inf.Estado =estad
        inf.save()
        mensaje="La Infraestructura fue dada de baja"
        messages.success(request, mensaje)
    else:             
        inf.delete()
        mensaje="Infraestructura eliminada"
        messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaInfraestructuram')

def editarInfm(request, id):
    linf=Infraestructura.objects.get(Id=id)  
    return render(request,"ConfiguracionApp/editarInfraestructuram.html", {"infm":linf})


def ModificarInfm(request):  
    idif=request.POST['idifm']
    nombre=request.POST['nombreifm']
    tipo=request.POST['tipoifm']
    
    inf=Infraestructura.objects.filter(Nombre=nombre,Tipo=tipo,TipoLoteMej="Mejora").exists()
    
    if inf == True:
            mensaje="La infraestructura ya existe"
            messages.warning(request, mensaje)
    else:
        minf=Infraestructura.objects.get(Id=idif)
        minf.Nombre=nombre
        minf.Tipo=tipo
        minf.TipoLoteMej="Mejora"
        minf.save()
        mensaje="Datos Actualizados"
        registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaInfraestructuram/')

###################################################################
# Tipo de Operacion

def toperacion(request):
       return render(request,"ConfiguracionApp/tipooperacion.html")

def registrarTOperacion(request):
    
    tipooperacion=request.POST['toperacion'].upper()     
   
    tip=TipoOper.objects.filter(Nombre=tipooperacion).exists()
    
    if tip == True:
            mensaje="El Tipo de Operación ya existe"
            messages.warning(request, mensaje)
    else:
        tipoOperacion=TipoOper.objects.create(Nombre=tipooperacion,Estado="activo")
        mensaje="Tipo de operación registrada"
        registroBit(request, Actividad=mensaje, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/toperacion/')

def listaToperaciones(request):
    listato=TipoOper.objects.all()
    return render(request, "ConfiguracionApp/listaToperaciones.html", {"toperaciones":listato})

def eliminarTO(request, id):
    estad="inactivo" 
    d=DeclaracionJuraCli.objects.filter(IdTipoOper=id).exists()
    top= TipoOper.objects.get(Id=id)
    if d == True and top.Estado=="activo":
        top.Estado =estad
        top.save()
        mensaje="El Tipo de Operacion fue dada de baja"
        messages.success(request, mensaje)
    else:             
        top.delete()
        mensaje="Tipo Operación eliminado"
        messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaToperaciones')

def editarTO(request, id):
       linfto=TipoOper.objects.get(Id=id) 
       return render(request,"ConfiguracionApp/editarTipooperacion.html", {"to":linfto})

def ModificarTO(request): 
    idto=request.POST['idt']
    tipooperacion=request.POST['toperacion'].upper()     
   
    tip=TipoOper.objects.filter(Nombre=tipooperacion).exists()
    
    if tip == True:
        mensaje="El Tipo de Operación ya existe"
        messages.warning(request, mensaje)
    else:
        mto=TipoOper.objects.get(Id=idto)
        mto.Nombre=tipooperacion
        mto.save()
        mensaje="Datos Actualizados"
        registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaToperaciones/')

##########################  
#  tasa
def tasa(request):
    return render(request, "ConfiguracionApp/tasa.html")

def registrartasa(request):
    numerocredito=request.POST['numerocredito'].upper()
    interes=request.POST['interes']
    estado=1

    tas=TasaInte.objects.filter(NumeroCred=numerocredito,Interes=interes).exists()
    
    if tas == True:
            mensaje="La Tasa de interes ya existe"
            messages.warning(request, mensaje)
    else:
        tasa= TasaInte.objects.create(NumeroCred=numerocredito, Interes=interes,Estado=estado)
        
        mensaje="Se ha guardado los datos"
        registroBit(request, Actividad=mensaje, Nivel="Registro")
        messages.success(request, mensaje)
    return render(request, "ConfiguracionApp/tasa.html")

def listarTasa(request):
    tasa=TasaInte.objects.all()
    return render(request, "ConfiguracionApp/listartasa.html",{"TasaInteres":tasa})

def editarTasa(request, id):
    tasa= TasaInte.objects.get(Id=id)
    return render(request, "ConfiguracionApp/editarTasa.html",{"tasa":tasa})

def ModificarTasa(request):
    idtas=request.POST['idt']
    numerocredito=request.POST['numerocredito']
    interes=request.POST['interes']

    tas=TasaInte.objects.filter(NumeroCred=numerocredito,Interes=interes).exists()
    print(tas)
    if tas == True:
            mensaje="La Tasa de interes ya existe"
            messages.warning(request, mensaje)
    else:
        mtasa= TasaInte.objects.get(Id=idtas)
        mtasa.NumeroCred=numerocredito
        mtasa.Interes=interes
        mtasa.save()
        mensaje="Datos Actualizados"
        registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
        messages.success(request, mensaje)

    return redirect('listarTasa')

#############################
# Alternativa

def alternativa(request):
    tasa=TasaInte.objects.all()
    return render(request, "ConfiguracionApp/alternativas.html",{"TasaInteres":tasa})

def registraral(request):
    alternativa=request.POST['alternativa'].upper()
    montominimo=request.POST['montominimo']
    montomaximo=request.POST['montomaximo']
    plazo=request.POST['plazo']
    pla=int(plazo)
    plazomese=pla*12
    id=request.POST['interes']
    interes=TasaInte.objects.get(Id=id)
    interes.Id=id
    estado=1

    consulta=Alternativa.objects.filter(Alternativa=alternativa,IdTasaInte=interes).exists()
    
    if consulta==True :
        mensaje="El nombre de la linea de financiamiento ya existe"
        messages.warning(request, mensaje)
        return redirect('/ConfiguracionApp/listarAl')
    else:
        tasa= Alternativa.objects.create(Alternativa=alternativa,MontoMini=montominimo,MontoMaxi=montomaximo,
                                    Plazo=plazo,PlazoMese=plazomese,IdTasaInte=interes,Estado=estado)
        mensaje="Se ha registro la alternativa "
        registroBit(request, Actividad=mensaje + alternativa, Nivel="Registro")
        messages.success(request, mensaje)
    return redirect('alternativa')
    

def listarAl(request):
    tasa=Alternativa.objects.all()
    return render(request, "ConfiguracionApp/listarAl.html",{"Alternativa":tasa})

def editarAlt(request, id):
    tasa=TasaInte.objects.all()
    alternativa= Alternativa.objects.get(Id=id)
    return render(request, "ConfiguracionApp/editarAlternativa.html",{"TasaInteres":tasa,"alternativa":alternativa})

def ModificarAlternativa(request):
    idal=request.POST['idalt']
    alternativa=request.POST['alternativa']
    montominimo=request.POST['montominimo']
    montomaximo=request.POST['montomaximo']
    plazo=request.POST['plazo']
    pla=int(plazo)
    plazomese=pla*12
    id=request.POST['interes']
    interes=TasaInte.objects.get(Id=id)
    interes.Id=id

    print(alternativa)
    consulta=Alternativa.objects.filter(Alternativa=alternativa,IdTasaInte=interes).exists()
    
    if consulta==True :
        mensaje="El nombre de la linea de financiamiento ya existe"
        messages.warning(request, mensaje)
        return redirect('/ConfiguracionApp/listarAl')
    else:
        malternativa= Alternativa.objects.get(Id=idal)
        malternativa.Alternativa=alternativa
        malternativa.MontoMini=montominimo
        malternativa.MontoMaxi=montomaximo
        malternativa.Plazo=plazo
        malternativa.PlazoMese=plazomese
        malternativa.IdTasaInte=interes
        malternativa.save()
        
        mensaje="Datos Actualizados "
        registroBit(request, Actividad=mensaje + alternativa, Nivel="Actualizacion")
        messages.success(request, mensaje)
    return redirect('listarAl')
########################### 
# Rngo financiamiento

def rangoFinanciamiento(request):
    salario=Salario.objects.filter(Estado="activo")
    alter=Alternativa.objects.all()
    ran_alter = json.dumps(list(alter.values()), default=str)
    ran_data = list(salario.values())
     # Serializa el campo Decimal usando la función personalizada y el DjangoJSONEncoder
    for item in ran_data:
        if 'SalarioMini' in item:
            item['SalarioMini'] = float(item['SalarioMini'])
        if 'SalarioMaxi' in item:
            item['SalarioMaxi'] = float(item['SalarioMaxi'])
        if 'FechaInic' in item and item['FechaInic'] is not None:
            item['FechaInic'] = item['FechaInic'].strftime('%Y-%m-%d')
        if 'FechaFina' in item and item['FechaFina'] is not None:
            item['FechaFina'] = item['FechaFina'].strftime('%Y-%m-%d')
    ran_json = json.dumps(ran_data)# Convertir la lista a JSON
         
    return render(request, "ConfiguracionApp/rangoFinan.html",{"salario":salario, "alternativa":alter, "sal":ran_json, "alter":ran_alter})

def registrarRanFin(request):

    idalter=request.POST['alternativas'] # id alternativa
    idsal=request.POST['salario'] # id salario
    montominimo=request.POST['montominimo']
    montomaximo=request.POST['montomaximo']
    vecesfinan=float(request.POST['vecesFin'])
    
    alter=Alternativa.objects.get(Id=idalter)
    alter.Id=idalter

    salar=Salario.objects.get(Id=idsal)
    salar.Id=idsal

    rangoFinan=RangoFina.objects.create(VecesFina=vecesfinan,MontoMini=montominimo,MontoMaxi=montomaximo,IdAlternativa=alter,IdSalario=salar)

    mensaje="Se ha registrado rango de financiamiento "
    registroBit(request, Actividad=mensaje + str(rangoFinan.MontoMini) +" - " + str(rangoFinan.MontoMaxi), Nivel="Registro")
    messages.success(request, mensaje)
    return redirect("../rangoFinanciamiento")#rangoFinan
#Lista de rangos de financiamiento

def listarRanFin(request):
    lisRanF=RangoFina.objects.all()
    lisAlt=Alternativa.objects.all()
    listarmuni=Departamento.objects.all()
    return render(request,"ConfiguracionApp/listarRanFin.html", {"LisFinan":lisRanF, "alternativa":lisAlt})

def lisAltRan(request):
    id=request.GET['id']
    lista_rangos=[]
    rangos=""
    if request.is_ajax():
        try:
            rangos=RangoFina.objects.filter(IdAlternativa=id)
            for item in rangos:
                lista_rangos.append({"id":item.Id, "salario":item.IdSalario.TipoSala, "minimo":item.MontoMini, "maximo":item.MontoMaxi, "vecesF":item.VecesFina})
        except Exception:
            None
        print("pasoo"+str(rangos))
        serialized_data = json.dumps(lista_rangos,default=str)
        #serialized_data = serialize("safe",[lista_muni])
        return HttpResponse(serialized_data, content_type="application/json")


def modRanFin(request, id):
    rango= RangoFina.objects.get(Id=id)
    alter= Alternativa.objects.all()
    sala= Salario.objects.filter(Estado="activo")
    ran_alter = json.dumps(list(alter.values()),default=str) 
    ran_data = list(sala.values())
     # Serializa el campo Decimal usando la función personalizada y el DjangoJSONEncoder
    for item in ran_data:
        if 'SalarioMini' in item:
            item['SalarioMini'] = float(item['SalarioMini'])
        if 'SalarioMaxi' in item:
            item['SalarioMaxi'] = float(item['SalarioMaxi'])
        if 'FechaInic' in item and item['FechaInic'] is not None:
            item['FechaInic'] = item['FechaInic'].strftime('%Y-%m-%d')
        if 'FechaFina' in item and item['FechaFina'] is not None:
            item['FechaFina'] = item['FechaFina'].strftime('%Y-%m-%d')
    ran_json = json.dumps(ran_data)# Convertir la lista a JSON
    return render (request, "ConfiguracionApp/rangoFinanedit.html", {"rangosF":rango, "alternativa":alter, "salario":sala, "sal":ran_json, "alter":ran_alter})


def editRanFin(request):
    id=request.POST['id']
    idalter=request.POST['alternativas'] # id alternativa
    idsal=request.POST['salario'] # id salario
    montominimo=request.POST['montominimo']
    montomaximo=request.POST['montomaximo']
    vecesfinan=float(request.POST['vecesFin'])
    
    alter=Alternativa.objects.get(Id=idalter)
    sal= Salario.objects.get(Id=idsal)
    
    ranFin=RangoFina.objects.filter(IdAlternativa=alter.Id, IdSalario=sal.Id).exists
    if ranFin == True:
            mensaje="El rango para esa alternativa y salario ya existe"
            messages.warning(request, mensaje)
    else:
            ranF = RangoFina.objects.get(Id=id)
            ranF.VecesFina=vecesfinan
            ranF.MontoMaxi=montomaximo
            ranF.MontoMini=montominimo
            ranF.IdAlternativa=alter
            ranF.IdSalario=sal
            ranF.save()
            mensaje="Rango de financiamiento actualizado"
            registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
            messages.success(request, mensaje)
    return redirect('/ConfiguracionApp/listaRanFin')

def modiMuni(request, idmuni):
    muni = Municipio.objects.get(Id=idmuni)
    listarde=Departamento.objects.all()
    return render(request, "DireccionApp/modiMuni.html", {"Muni":muni,"Departamento":listarde})

#######################################################
# tipos de viviendas
def tvivienda(request):
    return render(request,"ConfiguracionApp/modeloVivienda.html")

def registrarModeloV(request):
       
    topovivienda=request.POST['tipovivienda']
    modelo=request.FILES['modelov']
    montoc=request.POST['montov']
    descripcion =request.POST['descripcion']
   
    mod=ModeloVivi.objects.filter(TipoVivi=topovivienda,MontoCons=montoc).exists()
    
    if mod == True:
            mensaje="El modelo de vivienda ya existe"
            messages.warning(request, mensaje)
    else:
        modelovivienda=ModeloVivi.objects.create(TipoVivi=topovivienda,Modelo=modelo,MontoCons=montoc,Descripcion=descripcion)
        mensaje="Modelo de vivienda registrada "
        registroBit(request, Actividad=mensaje + topovivienda, Nivel="Registro")
        messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/tvivienda/')

def listarModeloV(request):
    modelosv=ModeloVivi.objects.all()  
    return render(request,"ConfiguracionApp/listaModeloVivienda.html", {"modelos":modelosv})

def editarMV(request, id):
       mmodelosv=ModeloVivi.objects.get(Id=id) 
       return render(request,"ConfiguracionApp/editarModeloVivienda.html", {"mmv":mmodelosv})

def modificarMV(request): 
    idmv=request.POST['idmv']
    montoc=request.POST['montov']
    descripcion =request.POST['descripcion']

    dmodelov=request.POST['dmodelov']
    try:
        modelo=request.FILES['modelov']
    except :
        modelo=""

    mmod=ModeloVivi.objects.get(Id=idmv)     

    if dmodelov == "" :
        mmod.Modelo=modelo

    if dmodelov != "" and modelo !="":
        mmod.Modelo=modelo

    mmod.MontoCons=montoc
    mmod.Descripcion=descripcion
    mmod.save()
   
    mensaje="Datos Actualizados"
    registroBit(request, Actividad=mensaje, Nivel="Actualizacion")
    messages.success(request, mensaje)

    return redirect('/ConfiguracionApp/listaModeloV/')
