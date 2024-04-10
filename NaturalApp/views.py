import json
from django.http.response import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render,redirect, HttpResponse
from ClienteApp.models import *
from django.contrib import messages
from ConfiguracionApp.models import Alternativa, ModeloVivi, Agencia
from ListaChequeoApp.models import ListaCheq
from NaturalApp.models import *
from SolicitudesApp.models import *
from EvaluacionIvEFApp.models import *
from datetime import  datetime
from time import strftime, strptime
from django.db.models import Q

from TesisApp.views import registroBit


# Create your views here.
def registrarSolicitudNatu(request, idCliente):
   #try:
        cliente = Perfil.objects.get(Id=idCliente)
        egresosf = EgresosFami.objects.get(Estado="1", IdPerfil= idCliente )
        ingresosf = IngresosFami.objects.get(IdEgresosFami = egresosf.Id)
        capacidad = CapacidadPagoFam.objects.get(IdEgresosFami=egresosf.Id)
        alternativas = Alternativa.objects.all()
        modelos = ModeloVivi.objects.all()
        return render(request, "NaturalApp/solicitudNatural.html", {
            "cliente":cliente, "ingresosf":ingresosf, "alternativas":alternativas,"modelos":modelos, "capacidaPago":capacidad})

    
def registroSolicitudN(request):
    tipoobra=request.POST['tipoobra']
    fecha= request.POST['fechaSN']
    cliente=Perfil.objects.get(Id= request.POST['idCliente'])
    n= request.POST['n']
    comunidad= request.POST['comunidadN'].upper()
    area= request.POST['areaN']
    tipoingreso= request.POST['tipoingreso']
    estado= request.POST['estadoN']
    estado_soli=1
    if(estado=="Completado"):
        estado_soli=2

    soli= Solicitud.objects.create(TipoObra=tipoobra,Fecha=fecha, Numero=n, Comunidad=comunidad, Area=area, Tipo="natural",TipoIngr=tipoingreso, Estado=estado,IdPerfil=cliente, EstadoSoli=estado_soli )
    
    cliente.EstadoSoli=4
    cliente.save()


    idSoli= Solicitud.objects.get(Fecha=fecha,Tipo="natural",IdPerfil=cliente)
   
    registroBit(request, "Se registro formulario Solicitud personal " + idSoli.IdPerfil.Dui, "Registro")
    
    #      #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.create(Fecha=fecha,SolicitudCred="Si",Estado="incompleto",IdSolicitud=idSoli) 
    

    bandera= request.POST['passDPN']  # guarda datos personales
    if(bandera == '1'):        
        
        lugarExp=request.POST['lugExS']        
        fechaExp=request.POST['fechExS']        
        lugarNac=request.POST['lugNaS']
        fechaNac=request.POST['fechNaS']
        edad= request.POST['edadS']
        aestadoCivil=request.POST['estadoCivilS']
        Genero= request.POST['generoS']
        Profecion= request.POST['profecionS']
        estadoC=1
        if(fechaExp==""):
            fechaExp="9999-01-01"
        
        datos = DatosPers.objects.create(LugarDuiCli=lugarExp, FechaDuiCli=fechaExp, LugarNaciCli=lugarNac,EstadoCiviCli=aestadoCivil,
        GeneroClie=Genero , Profesion= Profecion,EstadoClie=estadoC,IdSolicitud=idSoli )
        
   
    bandera= request.POST['passDPNC']  # guarda datos personales
    if(bandera == '1'):   
        sinFE=0                 #sin fecha de expiracion
        sinFN=0                 #sin fecha de nacimiento
        tipo=request.POST['tipoSN']
        nombre= request.POST['nombreC']     #para el conyuge o codeudor
        apellido= request.POST['apellidoC']
        dui= request.POST['duiC']
        lugarExp=request.POST['lugExC']
        fechaExp=request.POST['fechExC']
        if(fechaExp==""):
            fechaExp="9999-01-01"
            
        lugarNac=request.POST['lugNaC']
        fechaNac=request.POST['fechNaC']
        if(fechaNac==""):  
            fechaNac="9999-01-01"
            
        edad= request.POST['edadC']
        if(edad==""):
            edad="0"
        aestadoCivil=request.POST['estadoCivilC']
        Genero= request.POST['generoC']
        try:
            Profecion= request.POST['profecionC']
        except :
           Profecion= " "
       
        estadoF=1

        
        datos1 = DatosPersFia.objects.create(Tipo=tipo, NombreFiad=nombre, ApellidoFiad=apellido, DuiFiad=dui,LugarDuiFia=lugarExp,
        FechaDuiFia=fechaExp, FechaNaciFia=fechaNac,LugarNaciFia=lugarNac,EdadFiad=edad ,EstadoCiviFiad=aestadoCivil,
        GeneroFiad=Genero , ProfecionFiad= Profecion,EstadoFiad=estadoF, IdSolicitud=idSoli )
    #fin datos personales


    bandera= request.POST['passGPN'] #inicia guardar grupo familiar
    if(bandera == '1'):
       nombreGP =request.POST.getlist('nombreGP') 
       edadGP =request.POST.getlist('edadGP')
       salarioGP =request.POST.getlist('salarioGP')   
       trabajoGP=request.POST.getlist('trabajoGP')
       parentescoGP =request.POST.getlist('parentescoGP')
       
       for i in range(len(nombreGP)):
        if (nombreGP[i] != ""):
            if(salarioGP[i] ==""):
                salarioGP[i] ="0"
            grupo = GrupoFami.objects.create(Nombre=nombreGP[i], Edad=edadGP[i], Salario=salarioGP[i], Trabajo=trabajoGP[i],
            Parentesco=parentescoGP[i], IdSolicitud=idSoli)

    #fin grupo familiar

    bandera= request.POST['passDLN'] #inicia guardar domicilio y lugar de trabajo
    if(bandera == '1'):
       direActS =request.POST['direActS']# guarda direccion del solicitante
       puntoRefS =request.POST['puntoRefS']
       telefonoS =request.POST['telefonoS']
       condicionS =request.POST['condicionS']       
       resideS=request.POST['resideS']
       lugrTrabS =request.POST['lugrTrabS']
       jefS =request.POST['jefeS']
       tiempoS =request.POST['tiempoS']       
       salarioS =request.POST['salarioS']
       if(salarioS==""):
            salarioS='0'
       direccionNS =request.POST['direccionNS']
       telefonoNS =request.POST['telefonoNS']
       tipo="Solicitante"

       domicilioS = Domicilio.objects.create(Direccion=direActS, Referencia=puntoRefS,Telefono=telefonoS, ResideDesd=resideS, 
       CondicionVivi=condicionS, LugarTrab=lugrTrabS,  JefeInme=jefS, TiempoEmprTieFun=tiempoS, SalarioIngr=salarioS, 
       DireccionTrabMic=direccionNS, TelefonoTrabMic=telefonoNS, Tipo=tipo, IdSolicitud=idSoli) 
       
    bandera= request.POST['passDLNC'] #inicia guardar domicilio y lugar de trabajo
    if(bandera == '1'):
       
       direActC =request.POST['direActC']# guarda direccion del conyuge o codeudor     
       puntoRefC =request.POST['puntoRefC']
       telefonoC =request.POST['telefonoC']
       condicionC =request.POST['condicionC'] 
       resideC=request.POST['resideC']
       lugrTrabC =request.POST['lugrTrabC']
       jefC =request.POST['jefeC']
       tiempoC =request.POST['tiempoC']
       salarioC =request.POST['salarioC']
       if(salarioC==""):
            salarioC='0'
       direccionNC =request.POST['direccionNC']
       telefonoNC =request.POST['telefonoNC']
       tipo=request.POST['tipoSN']

       domicilioS = Domicilio.objects.create(Direccion=direActC, Referencia=puntoRefC,Telefono=telefonoC, ResideDesd=resideC, 
       CondicionVivi=condicionC, LugarTrab=lugrTrabC, JefeInme=jefC, TiempoEmprTieFun=tiempoC, SalarioIngr=salarioC, 
       DireccionTrabMic=direccionNC,TelefonoTrabMic=telefonoNC, Tipo=tipo, IdSolicitud=idSoli)
    #fin domicilio y lugar de trabajo 

    bandera= request.POST['passDORN'] #inicia guardar datos de la obra a realizar
    if(bandera == '1'):
       destinoNE =request.POST['destinoNE']
       duenoNE =request.POST['duenoNE']
       parentescoNE =request.POST['parentescoNE']
       direExacta=request.POST['direccionE'] 
       detalleObra =request.POST['detalleObra'] 
       detalleadic =request.POST['detalleAD']  
       PresupuestoME =request.POST['PresupuestoNE']
       if(PresupuestoME==""):
            PresupuestoME='0'

       destinoAlt=Alternativa.objects.get(Id=destinoNE)
       modeloVivienda= ModeloVivi.objects.get(Id=detalleObra)
       modeloVivienda.Id=detalleObra
       
       dor = DatosObra.objects.create(IdAlternativa=destinoAlt, Dueno= duenoNE, Parentesco=parentescoNE,DireccionExac=direExacta ,
      IdModeloVivi=modeloVivienda,DetalleAdic=detalleadic, Presupuesto=PresupuestoME, IdSolicitud=idSoli) 
    #fin datos de la obra a realizar


    bandera= request.POST['passDSN'] #inicia guardar detalle de la solicitud
    if(bandera == '1'):
       montoNE =request.POST['montoNE']
       if(montoNE==""):
            montoNE='0'
       plazoNE =request.POST['plazoNE']
       cuotaNE =request.POST['cuotaNE']
       if(cuotaNE==""):
            cuotaNE='0'
       formaPagoNE =request.POST['formaPagoNE']   
       FechaPagoNE =request.POST['FechaPagoNE']

       ds = Detalle.objects.create(Monto=montoNE, Plazo= plazoNE, Cuota=cuotaNE, 
      FormaPago=formaPagoNE, FechaPago= FechaPagoNE, IdSolicitud=idSoli) 
    #fin detalle de la solicitud

    bandera= request.POST['passECN'] #inicia experiencia crediticia
    if(bandera == '1'):
       lugarEC =request.POST.getlist('lugarEC') 
       montoEC =request.POST.getlist('montoEC')       
       fechaEC =request.POST.getlist('fechaEC')       
       estadoEC=request.POST.getlist('estadoEC')
       cuotaEC =request.POST.getlist('cuotaEC')
      # posee =request.POST['sinEC'] 

      # print(posee)
      # if(posee != True):
       for i in range(len(lugarEC)):
         if (lugarEC[i] != ""):
            if(montoEC[i]==""):
                 montoEC[i]='0'            
            if(cuotaEC[i]==""):
                cuotaEC[i]='0'
            if(fechaEC[i]==""):
                experiencia = ExperienciaCred.objects.create(Lugar=lugarEC[i], Monto=montoEC[i],
             Estado=estadoEC[i],  Cuota=cuotaEC[i], PoseeExpe=0, IdSolicitud=idSoli)
            else:
                experiencia = ExperienciaCred.objects.create(Lugar=lugarEC[i], Monto=montoEC[i], FechaOtor=fechaEC[i],
             Estado=estadoEC[i],  Cuota=cuotaEC[i], PoseeExpe=0, IdSolicitud=idSoli)


    bandera= request.POST['passRPFN'] #inicia referencias personales y familiares
    if(bandera == '1'):
       nombreRPF =request.POST.getlist('nombreRPF') 
       parentescoRPF =request.POST.getlist('parentescoRPF')
       domicilioRPF =request.POST.getlist('domicilioRPF')
       telefonoRPF=request.POST.getlist('telefonoRPF')

       
       for i in range(len(nombreRPF)):
        if (nombreRPF[i] != ""):
            refere = Referencias.objects.create( Nombre=nombreRPF[i], Parentesco=parentescoRPF[i], 
            Domicilio=domicilioRPF[i], Telefono=telefonoRPF[i], IdSolicitud=idSoli)
    #fin referencias personales y familiares  
    
    bandera= request.POST['passCMN'] #inicia guardar comentarios
    if(bandera == '1'):
       
       try:
            comIniciativa =request.POST['comIniciativa']
       except :
            comIniciativa = " "
       try:
            comEvaluacion =request.POST['comEvaluacion']
       except :
            comEvaluacion= " "
       try:
            comGarantia =request.POST['comGarantia']
       except :
            comGarantia= " "

       c = Comentarios.objects.create(ComentarioNeceVivMej=comIniciativa, ComentarioEvalEst= comEvaluacion, ComentarioGaraOfr=comGarantia, IdSolicitud=idSoli) 
    #fin comentarios

     # inicio medio por el cual se informo
    try:
        redes =request.POST['redes']
    except :
        redes= " "
    try:
        pvv =request.POST['pvv']
    except :
        pvv= " "
    try:
        referenciado =request.POST['referenciado']
    except :
        referenciado= " "
    try:
        perifoneo =request.POST['perifoneo']
    except :
        perifoneo= " "
    try:
        radio =request.POST['radio']
    except :
        radio= " "
    try:
        feriav =request.POST['feriav']
    except :
        feriav= " "
    try:
        campanap =request.POST['campaprom']
    except :
        campanap= " "
    try:
        otros =request.POST['otros']
    except :
        otros= " "
    try:
        especifique =request.POST['espeotromed']
    except :
        especifique= " "


    medio = Medio.objects.create(RedesSoci=redes,Pvv=pvv,Referenciado=referenciado,Perifoneo=perifoneo,Radio=radio,FeriaVivi=feriav,CampanaProm=campanap,Otros=otros,Especifique=especifique, IdSolicitud=idSoli)

    # fin medio"""

    return redirect('administrarPerfil', id=soli.IdPerfil.Id)  # id de perfil 

def listarSNC(request): 
    listSolinc = Solicitud.objects.filter(Estado="Completado", Tipo="natural")
    return render(request, "NaturalApp/listarSNC.html", {"solicitudes":listSolinc})

def listarSNCA(request, id): # solicitudes completas por agencia
    listSoli = Solicitud.objects.filter(Q(Estado="Completado") & Q(Tipo="natural")& Q(IdPerfil__IdAgencia=id))
    return render(request, "NaturalApp/listarSNC.html", {"solicitudes":listSoli})


def listarSN(request): 
    listSolin = Solicitud.objects.filter(Estado="Incompleto",Tipo="natural")
    return render(request, "NaturalApp/listarSN.html", {"solicitudes":listSolin})

def editarSolicitudN(request, idSolicitud):
   
    try:
        solici = Solicitud.objects.get(Id=idSolicitud)
    except Solicitud.DoesNotExist:
        solici=""

    try:
        gpf=GrupoFami.objects.filter(IdSolicitud=idSolicitud)
    except GrupoFami.DoesNotExist:
        gpf=""

    try:
        dps=DatosPers.objects.get(IdSolicitud=idSolicitud)
        if(dps.FechaDuiCli.strftime("%Y-%m-%d") == "9999-01-01"):
            dps.FechaDuiCli=""                   
    except DatosPers.DoesNotExist:
        dps=""

    try:
        dpc=DatosPersFia.objects.get( Q(IdSolicitud=idSolicitud) & Q(Q(Tipo="codeudor") | Q(Tipo="conyuge")))
        if(dpc.FechaDuiFia.strftime("%Y-%m-%d") == "9999-01-01"):
            dpc.FechaDuiFia=""
        if(dpc.FechaNaciFia.strftime("%Y-%m-%d") == "9999-01-01"):
            dpc.FechaNaciFia=""
        if(dpc.EdadFiad == "0"):
            dpc.EdadFiad  =""
    except DatosPersFia.DoesNotExist:
       dpc=""   
   
    try:
        mdl=Domicilio.objects.get(IdSolicitud=idSolicitud, Tipo="Solicitante")
    except Domicilio.DoesNotExist:
        mdl=""
    try:
        mdlc=Domicilio.objects.get(Q(IdSolicitud=idSolicitud)  & Q(Q(Tipo="codeudor") | Q(Tipo="conyuge")))
    except Domicilio.DoesNotExist:
        mdlc=""

    try:
        dob=DatosObra.objects.get(IdSolicitud=idSolicitud)
    except DatosObra.DoesNotExist:
        dob=""

    try:
        ds=Detalle.objects.get(IdSolicitud=idSolicitud)
    except Detalle.DoesNotExist:
        ds=""

    try:
        ec=ExperienciaCred.objects.filter(IdSolicitud=idSolicitud)
    except ExperienciaCred.DoesNotExist:
        ec=""
    try:
        rp=Referencias.objects.filter(IdSolicitud=idSolicitud)
    except Referencias.DoesNotExist:
        rp=""

    try:
        cmt=Comentarios.objects.get(IdSolicitud=idSolicitud)
    except Comentarios.DoesNotExist:
        cmt=""

    try: 
        med=Medio.objects.get(IdSolicitud=idSolicitud)
    except Medio.DoesNotExist:
        med=""

    id_cliente = solici.IdPerfil.Id
    try:
         egresosf  = EgresosFami.objects.get(IdPerfil = id_cliente, Estado=1)
         try:
             ingresosf = IngresosFami.objects.get(IdEgresosFami=egresosf.Id)
         except IngresosFami.DoesNotExist:
             None
         try:
             capacidad = CapacidadPagoFam.objects.get(IdEgresosFami=egresosf.Id)
         except CapacidadPagoFam.DoesNotExist:
             None
    except EgresosFami.DoesNotExist:
          egresosf = ""   
          ingresosf =  ""
          capacidad=  ""
          
    
    alternativas = Alternativa.objects.all()
    modelos = ModeloVivi.objects.all()

    soli = [solici, dps, dpc, gpf, mdl, mdlc, dob, ds, ec, rp, cmt,med]
    return render(request, "NaturalApp/modificarSolicitudNatural.html", {
        "soli":soli,
        "alternativas":alternativas,
        "modelos":modelos,
        "ingresosf":ingresosf, 
        "capacidaPago":capacidad
        })



def modSoliNatural(request):
# Inicia modifcar solicitud
#datos generales de la solicitd   
    idSoli=request.POST['idSoliN']
    tipoobra=request.POST['tipoobraModN']
    n= request.POST['nModN']
    comunidad= request.POST['comunidadModN']
    area= request.POST['areaMN']
    tipoing = request.POST['tipoingresoModN']
    estado= request.POST['estadoMod']
    estado_soli=1
    if(estado=="Completado"):
        estado_soli=2

    soli = Solicitud.objects.get(Id=idSoli)
    soli.TipoObra = tipoobra
    soli.Numero = n
    soli.Comunidad = comunidad
    soli.Area = area
    soli.TipoIngr = tipoing
    soli.Estado = estado
    soli.EstadoSoli = estado_soli
    soli.save()

#Inicia modificar datos personales del solicitande    
    lugarExp=request.POST['lugExS']
    fechaExp=request.POST['fechExS']
    if(fechaExp==""):                   #valido que la fecha no este vacia sino no guarda
            fechaExp="9999-01-01"
    lugarNac=request.POST['lugNaS']
    aestadoCivil=request.POST['estadoCivilS']
    Genero= request.POST['generoS']
    Profecion= request.POST['profecionS']

    try:
        datos = DatosPers.objects.get(IdSolicitud=idSoli)
    except:
        datos=''

    datos = DatosPers.objects.update_or_create(IdSolicitud=idSoli,
            defaults={
            'LugarDuiCli':lugarExp,
            'FechaDuiCli':fechaExp,     
            'LugarNaciCli':lugarNac,
            'EstadoCiviCli':aestadoCivil,
            'GeneroClie':Genero  ,
            'Profesion': Profecion,    
            'EstadoClie':'1',    
            'IdSolicitud':soli })
    

#Inicia modificar para el conyuge o codeudor
    bandera= request.POST['passDPNC']  # guarda datos personales
    if(bandera == '1'):  
        id= request.POST['idC']
        tipo=request.POST['tipoSN']
        nombre= request.POST['nombreC']     
        apellido= request.POST['apellidoC']
        dui= request.POST['duiC']
        lugarExp=request.POST['lugExC']
        fechaExp=request.POST['fechExC']
        if(fechaExp==""):
                fechaExp="9999-01-01"
        lugarNac=request.POST['lugNaC']
        fechaNac=request.POST['fechNaC']
        if(fechaNac==""):  
                fechaNac="9999-01-01"
        edad= request.POST['edadC']
        if(edad==""):
                edad="0"
        aestadoCivil=request.POST['estadoCivilC']
        Genero= request.POST['generoC']
        Profecion= request.POST['profecionC']
        
        if(id==""):
            datos = DatosPersFia.objects.update_or_create(IdSolicitud=idSoli,
            defaults={'Tipo' :tipo,
            'NombreFiad':nombre,
            'ApellidoFiad':apellido,
            'DuiFiad':dui ,
            'LugarDuiFia':lugarExp,
            'FechaDuiFia':fechaExp,
            'FechaNaciFia':fechaNac,        
            'LugarNaciFia':lugarNac,         
            'EdadFiad':edad,
            'EstadoCiviFiad':aestadoCivil,
            'GeneroFiad':Genero  ,
            'ProfecionFiad': Profecion,    
            'EstadoFiad':'1',    
            'IdSolicitud':soli })
        else:
            datos = DatosPersFia.objects.update_or_create(Id=id,
                defaults={'Tipo' :tipo,
                'NombreFiad':nombre,
                'ApellidoFiad':apellido,
                'DuiFiad':dui ,
                'LugarDuiFia':lugarExp,
                'FechaDuiFia':fechaExp,
                'FechaNaciFia':fechaNac,        
                'LugarNaciFia':lugarNac,         
                'EdadFiad':edad,
                'EstadoCiviFiad':aestadoCivil,
                'GeneroFiad':Genero  ,
                'ProfecionFiad': Profecion,   
                'EstadoFiad':'1',      
                'IdSolicitud':soli })
            
#Inicia modificar grupo familiar
    idGP=request.POST.getlist('idGPN')
    nombreGP =request.POST.getlist('nombreGP') 
    edadGP =request.POST.getlist('edadGP')
    salarioGP =request.POST.getlist('salarioGP')
    trabajoGP=request.POST.getlist('trabajoGP')
    parentescoGP =request.POST.getlist('parentescoGP')
     
    for i in range(len(nombreGP)):
     if (nombreGP[i] != ""):        
        if(salarioGP[i] ==""):
                salarioGP[i] ="0.00"
        
        if(idGP[i]!=""):
            grupo = GrupoFami.objects.update_or_create(IdSolicitud=idSoli,Id=idGP[i],
            defaults={ 'nombre':nombreGP[i], 
            'Edad':edadGP[i], 
            'Salario':salarioGP[i], 
            'Trabajo':trabajoGP[i],
            'Parentesco':parentescoGP[i], 
            'IdSolicitud':soli})
            
        else: #si registro un nuevo familiar ejecuta la orden sin enviar id de la tabla ya que no existe ese campo
            grupo1 = GrupoFami.objects.update_or_create(IdSolicitud=idSoli, Nombre=nombreGP[i], Parentesco=parentescoGP[i],
            defaults={ 'Nombre':nombreGP[i], 
            'Edad':edadGP[i], 
            'Salario':salarioGP[i], 
            'Trabajo':trabajoGP[i],
            'Parentesco':parentescoGP[i], 
            'IdSolicitud':soli})

#Inicia modificar domicilio del solicitante
    bandera= request.POST['passDLN'] 
    if(bandera == '1'):
        direActS =request.POST['direActS']
        puntoRefS =request.POST['puntoRefS']
        telefonoS =request.POST['telefonoS']
        condicionS =request.POST['condicionS']       
        resideS=request.POST['resideS']
        lugrTrabS =request.POST['lugrTrabS']
        jefS =request.POST['jefeS']
        tiempoS =request.POST['tiempoS']
        
        salarioS =request.POST['salarioS']
        if(salarioS==""):
            salarioS=0.00
        direccionNS =request.POST['direccionNS']
        telefonoNS =request.POST['telefonoNS']
        tipo="Solicitante"
        print(salarioS)
        domicilioS = Domicilio.objects.update_or_create(IdSolicitud=idSoli,Tipo="Solicitante",
        defaults={ 'Direccion':direActS,
            'Referencia':puntoRefS,
            'Telefono':telefonoS, 
            'ResideDesd':resideS, 
            'CondicionVivi':condicionS,
            'LugarTrab':lugrTrabS,
            'JefeInme':jefS,
            'TiempoEmprTieFun':tiempoS,
            'SalarioIngr':salarioS, 
            'DireccionTrabMic':direccionNS,       
            'TelefonoTrabMic':telefonoNS,
            'Tipo':tipo,
            'IdSolicitud':soli}) 

#inicia actualizaar domicilio conyuge o codeudor
    bandera= request.POST['passDLNC'] 
    if(bandera == '1'):
        idd=request.POST['idDomicilioCCN']   
        direActC =request.POST['direActC']
        puntoRefC =request.POST['puntoRefC']
        telefonoC =request.POST['telefonoC']
        condicionC =request.POST['condicionC']       
        resideC=request.POST['resideC']
        lugrTrabC =request.POST['lugrTrabC']
        jefC =request.POST['jefeC']
        tiempoC =request.POST['tiempoC']
        salarioC =request.POST['salarioC']
        if(salarioC==""):
            salarioC=0
        direccionNC =request.POST['direccionNC']
        telefonoNC =request.POST['telefonoNC']
        tipo=request.POST['tipoSN']

        if(idd==""):
                domicilioC = Domicilio.objects.update_or_create(IdSolicitud=idSoli, tipo=tipo,
            defaults={ 'Direccion':direActC,
                'Referencia':puntoRefC,
                'Telefono':telefonoC, 
                'ResideDesd':resideC, 
                'CondicionVivi':condicionC,
                'LugarTrab':lugrTrabC,
                'JefeInme':jefC,
                'TiempoEmprTieFun':tiempoC,
                'SalarioIngr':salarioC, 
                'DireccionTrabMic':direccionNC,        
                'TelefonoTrabMic':telefonoNC,
                'Tipo':tipo,
                'IdSolicitud':soli}) 

        else:
            domicilioC = Domicilio.objects.update_or_create(IdSolicitud=idSoli, Id=idd,
            defaults={ 'Direccion':direActC,
                'Referencia':puntoRefC,
                'Telefono':telefonoC, 
                'ResideDesd':resideC, 
                'CondicionVivi':condicionC,
                'LugarTrab':lugrTrabC,
                'JefeInme':jefC,
                'TiempoEmprTieFun':tiempoC,
                'SalarioIngr':salarioC, 
                'DireccionTrabMic':direccionNC,        
                'TelefonoTrabMic':telefonoNC,
                'Tipo':tipo,
                'IdSolicitud':soli}) 

#Inicia modificar datos de la obre a realiar
    bandera= request.POST['passDORN'] 
    if(bandera == '1'):
        destinoNE =request.POST['destinoNE']
        duenoNE =request.POST['duenoNE']
        parentescoNE =request.POST['parentescoNE']
        direExacta=request.POST['direccionE'] 
        detalleObra =request.POST['detalleObra']
        detalleadic =request.POST['detalleAD']     
        PresupuestoNE =request.POST['PresupuestoNE']
        if(PresupuestoNE==""):
            PresupuestoNE=0.00
        destinoAlt=Alternativa.objects.get(Id=destinoNE)    
        detalleObra=ModeloVivi.objects.get(Id=detalleObra)
        dor = DatosObra.objects.update_or_create(IdSolicitud=idSoli,
        defaults={ 'IdAlternativa':destinoAlt, 
        'Dueno': duenoNE, 
        'Parentesco':parentescoNE, 
        'DireccionExac':direExacta, 
        'IdModeloVivi':detalleObra, 
        'DetalleAdic':detalleadic,
        'Presupuesto':PresupuestoNE, 
        'IdSolicitud':soli}) 
    
#Inicia modificar detalle de la solicitud  
    bandera= request.POST['passDSN'] 
    if(bandera == '1'):
        montoNE =request.POST['montoNE']
        if(montoNE==""):
            montoNE=0
        plazoNE =request.POST['plazoNE']
        cuotaNE =request.POST['cuotaNE']
        if(cuotaNE==""):
            cuotaNE=0
        formaPagoNE =request.POST['formaPagoNE']   
        FechaPagoNE =request.POST['FechaPagoNE']
        
        ds = Detalle.objects.update_or_create(IdSolicitud=idSoli, 
        defaults={ 'Monto':montoNE, 
        'Plazo': plazoNE, 
        'Cuota':cuotaNE, 
        'FormaPago':formaPagoNE, 
        'FechaPago': FechaPagoNE, 
        'IdSolicitud':soli})

#Inicia modificar experiencia crediticia
    idExC=request.POST.getlist('idExCN')
    lugarEC =request.POST.getlist('lugarEC') 
    montoEC =request.POST.getlist('montoEC')
    fechaEC =request.POST.getlist('fechaEC')
    estadoEC=request.POST.getlist('estadoEC')
    cuotaEC =request.POST.getlist('cuotaEC')       
       
    for i in range(len(lugarEC)):     
        
     if(lugarEC[i] != ""):
        if(montoEC[i]==""):
                 montoEC[i]='0.00'            
        if(cuotaEC[i]==""):
                cuotaEC[i]='0.00'
        if(idExC[i]!=""):    
                if(fechaEC[i]==""):  
                    experiencia = ExperienciaCred.objects.update_or_create(IdSolicitud=idSoli, Id=idExC[i],
                defaults={'Lugar':lugarEC[i],
            'Monto':montoEC[i], 
            'Estado':estadoEC[i],  
            'Cuota':cuotaEC[i], 
            'PoseeExpe':False,
            'IdSolicitud':soli})
                else:
                    experiencia = ExperienciaCred.objects.update_or_create(IdSolicitud=idSoli, Id=idExC[i],
                defaults={'Lugar':lugarEC[i],
            'Monto':montoEC[i], 
            'FechaOtor':fechaEC[i],
            'Estado':estadoEC[i],  
            'Cuota':cuotaEC[i], 
            'PoseeExpe':False,
            'IdSolicitud':soli})        
        else:
            if(fechaEC[i]==""):  
                    experiencia = ExperienciaCred.objects.update_or_create(IdSolicitud=idSoli,Lugar=lugarEC[i],Monto=montoEC[i],Estado=estadoEC[i], 
                defaults={'Lugar':lugarEC[i],
            'Monto':montoEC[i], 
            'Estado':estadoEC[i],  
            'Cuota':cuotaEC[i], 
            'PoseeExpe':False,
            'IdSolicitud':soli})
            else:
                    experiencia = ExperienciaCred.objects.update_or_create(IdSolicitud=idSoli,FechaOtor=fechaEC[i], Lugar=lugarEC[i],Monto=montoEC[i],Estado=estadoEC[i],
                defaults={'lugar':lugarEC[i],
            'Monto':montoEC[i], 
            'FechaOtor':fechaEC[i],
            'Estado':estadoEC[i],  
            'Cuota':cuotaEC[i], 
            'PoseeExpe':False,
            'IdSolicitud':soli})  

#inicia modificar referencias personales
    idRF=request.POST.getlist('idRFN')
    nombreRPF =request.POST.getlist('nombreRPF') 
    parentescoRPF =request.POST.getlist('parentescoRPF')
    domicilioRPF =request.POST.getlist('domicilioRPF')
    telefonoRPF=request.POST.getlist('telefonoRPF')

    for i in range(len(nombreRPF )):
     
      
      if(nombreRPF [i] != ""):
        if(idRF[i]==""):
            refer = Referencias.objects.update_or_create(IdSolicitud=idSoli, 
            defaults={'Nombre':nombreRPF[i],
            'Parentesco':parentescoRPF[i], 
            'Domicilio':domicilioRPF[i],
            'Telefono':telefonoRPF[i],  
            'IdSolicitud':soli})
        else: 
            refer = Referencias.objects.update_or_create(IdSolicitud=idSoli, Id=idRF[i],
            defaults={'Nombre':nombreRPF[i],
            'Parentesco':parentescoRPF[i], 
            'Domicilio':domicilioRPF[i],
            'Telefono':telefonoRPF[i],  
            'IdSolicitud':soli})

#Inicia modificar comentarios
    bandera= request.POST['passCMN'] #inicia guardar comentarios
    if(bandera == '1'):
        comIniciativa =request.POST['comIniciativa']
        comEvaluacion =request.POST['comEvaluacion']
        comGarantia =request.POST['comGarantia']
        print(comEvaluacion)
        comn = Comentarios.objects.update_or_create(IdSolicitud=idSoli,
            defaults={'ComentarioNeceVivMej' :comIniciativa,
            'ComentarioEvalEst':comEvaluacion,
            'ComentarioGaraOfr':comGarantia,     
            'IdSolicitud':soli })

    # inicio medio por el cual se informo
        try:
            redes =request.POST['redes']
        except :
            redes= " "
        try:
            pvv =request.POST['pvv']
        except :
            pvv= " "
        try:
            referenciado =request.POST['referenciado']
        except :
            referenciado= " "
        try:
            perifoneo =request.POST['perifoneo']
        except :
            perifoneo= " "
        try:
            radio =request.POST['radio']
        except :
            radio= " "
        try:
            feriav =request.POST['feriav']
        except :
            feriav= " "
        try:
            campanap =request.POST['campaprom']
        except :
            campanap= " "
        try:
            otros =request.POST['otros']
        except :
            otros= " "
        try:
            especifique =request.POST['espeotromed']
        except :
            especifique= " "


        medio = Medio.objects.update_or_create(IdSolicitud=idSoli,
            defaults={'RedesSoci':redes,
                    'Pvv':pvv,
                    'Referenciado':referenciado,
                    'Perifoneo':perifoneo,
                    'Radio':radio,
                    'FeriaVivi':feriav,
                    'CampanaProm':campanap,
                    'Otros':otros,
                    'Especifique':especifique,
                    'IdSolicitud':soli
            })
        
    registroBit(request, "Se actualizo formulario Solicitud personal " + soli.IdPerfil.Dui, "Actualizacion")

    return redirect('administrarPerfil', id=soli.IdPerfil.Id)  # id de perfil 

# lista de reportes para el comite
def listaRF(request,id):
    listSoli = Solicitud.objects.filter(Estado="Completado", Tipo="natural",EstadoSoli=3, IdPerfil__IdAgencia=id)
    return render(request, "NaturalApp/listaReportesF.html", {"solicitudes":listSoli})

def listaRFAdmin(request):
    listaAg=Agencia.objects.all()
    return render(request, "NaturalApp/listaReportesFAdmin.html", {"agencia":listaAg})

def agencRFA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Estado="Completado", Tipo="natural",EstadoSoli=3, IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

#########################################################
#lista de solicitudes pendientes de aprobacion 
def listaSolicitudesPA(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=3, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "NaturalApp/listaSolicitudPA.html", {"solicitudes":listperpa})

#lista de solicitudes pendientes de aprobacion  Admin
def listaSolicitudesPAAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "NaturalApp/listaSolicitudPAAdmin.html", {"agencia":listaAg})

def agencPAA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=3, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    

#lista de solicitudes aprobadas
def listaSolicitudesApr(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=4, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "NaturalApp/listaSAprobadas.html", {"solicitudes":listperpa})

#lista de solicitudes aprobadas Admin
def listaSolicitudesAprAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "NaturalApp/listaSAprobadasAdmin.html", {"agencia":listaAg})

def agencAA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=4, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    
#lista de solicitudes observadas= 5
def listaSolicitudesObs(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=5, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "NaturalApp/listaSObservadas.html", {"solicitudes":listperpa})

#lista de solicitudes observadas  Admin
def listaSolicitudesObsAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "NaturalApp/listaSObservadasAdmin.html", {"agencia":listaAg})

def agencOA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=5, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

#lista de solicitudes  denegadas=6
def listaSolicitudesDen(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=6, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "NaturalApp/listaSDenegadas.html", {"solicitudes":listperpa})

#lista de solicitudes denegadas  Admin
def listaSolicitudesDenAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "NaturalApp/listaSDenegadasAdmin.html", {"agencia":listaAg})

def agencDA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="natural",EstadoSoli=6, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

def obtenerRangoNat(request):
    id = request.GET['id']   
    alternativa = "-0"
    if request.is_ajax():  
        try: 
            alternativa = Alternativa.objects.get(Id=id) 
            serialized_data =  serialize("json", [  alternativa ])
        except Exception: 
            serialized_data = json.dumps( alternativa , default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})



