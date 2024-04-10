from datetime import date
import json
from django.db import IntegrityError
from django.http import FileResponse
from django.core.serializers import serialize
from django.shortcuts import render,redirect, HttpResponse
from django.http.response import JsonResponse
from django.contrib import messages
from fpdf import FPDF
from django.contrib.auth.decorators import login_required
from SolicitudesApp.models import *
from ClienteApp.models import Perfil
from TesisApp.models import Usuario
from EvaluacionMicroApp.models import *
from ConfiguracionApp.models import Alternativa, ModeloVivi, Agencia, Ocupacion
from django.db.models import Q
from ListaChequeoApp.models import *
from TesisApp.views import registroBit
from NaturalApp import views as nat


# Create your views here.
def registroSolicitudMicro(request):    
    return render(request,"SolicitudesApp/solicitudMicro.html")

def registrarSolicitud(request, idCliente):
   #try:
        try:
            listao=Ocupacion.objects.filter(Estado="activo")
        except Ocupacion.DoesNotExist:
            listao=""
        cliente = Perfil.objects.get(Id=idCliente)
        try:
            balance = BalanceSituMic.objects.get(Estado="1", IdPerfil = idCliente )
        except :
            balance =""
        try:
            estado = EstadoResuMic.objects.get(IdBalanceSituMic = balance.Id)
        except :
            estado =""
        try:
            capacidad = CapacidadPagoMic.objects.get(IdEgresoFlujMic=estado.Id)
        except :
            capacidad =""
        
        alternativas = Alternativa.objects.all()
        modelos = ModeloVivi.objects.all()
        return render(request, "SolicitudesApp/solicitudMicro.html", {"ocupaciones":listao,
            "cliente":cliente, "balance":balance, "estado":estado, "alternativas":alternativas,"modelos":modelos, "capacidaPago":capacidad})
    #except Exception:
     #   return None


def modificarSolicitud(request, idSolicitud):
    try:
            listao=Ocupacion.objects.filter(Estado="activo")
    except Ocupacion.DoesNotExist:
            listao=""
   
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
         balance = BalanceSituMic.objects.get(Estado="1",IdPerfil = id_cliente)
         try:
             estado = EstadoResuMic.objects.get(IdBalanceSituMic = balance.Id)
         except EstadoResuMic.DoesNotExist:
             None
    except BalanceSituMic.DoesNotExist:
          balance = ""   
          estado =  ""
          
    
    alternativas = Alternativa.objects.all()
    modelos = ModeloVivi.objects.all()

    soli = [solici, dps, dpc, gpf, mdl, mdlc, dob, ds, ec, rp, cmt,med]
    return render(request, "SolicitudesApp/modificarSolicitudMicro.html", {"ocupaciones":listao,
        "soli":soli,
        "alternativas":alternativas,
        "modelos":modelos,
        "balance":balance, 
        "estado":estado
        })

def listaSC(request):
    listSoli = Solicitud.objects.filter(Estado="Completado", Tipo="micro")
    return render(request, "SolicitudesApp/listaSCompleta.html", {"solicitudes":listSoli})


def listaSCA(request, id): # solicitudes completas por agencia
    listSoli = Solicitud.objects.filter(Q(Estado="Completado") & Q(Tipo="micro")& Q(IdPerfil__IdAgencia=id))
    return render(request, "SolicitudesApp/listaSCompleta.html", {"solicitudes":listSoli})

def listaSolicitud(request):    
    listSoli = Solicitud.objects.filter(Estado="Incompleto", Tipo="micro")
    return render(request, "SolicitudesApp/listSolicitudes.html", {"solicitudes":listSoli})
    
def registroSolicitud(request):
    tipoobra=request.POST['tipoobra']
    fecha= request.POST['fechaSM']
    cliente=Perfil.objects.get(Id= request.POST['idCliente'])
    n= request.POST['n']
    comunidad= request.POST['comunidadM'].upper()
    area= request.POST['areaM']
    estado= request.POST['estadoM']
    estado_soli=1
    if(estado=="Completado"):
        estado_soli=2

    soli= Solicitud.objects.create(TipoObra=tipoobra,Fecha=fecha, Numero=n, Comunidad=comunidad, Area=area, Tipo="micro", Estado=estado,IdPerfil=cliente, EstadoSoli=estado_soli )
    
    cliente.EstadoSoli=4
    cliente.save()


    idSoli= Solicitud.objects.get(Fecha=fecha,Tipo="micro",IdPerfil=cliente)
   
   # soli.perfil.add(cliente)        para guardar en la tabla solicitud_perfil

    #idSoli= solicitud.objects.all().last() #obtengo la ultima solicitud registrada   
       #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.create(Fecha=fecha,SolicitudCred="Si",Estado="incompleto",IdSolicitud=idSoli)


    bandera= request.POST['passDPM']  # guarda datos personales
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
        GeneroClie=Genero , EstadoClie=estadoC,IdSolicitud=idSoli )
        
   
    bandera= request.POST['passDPMC']  # guarda datos personales codeudor o conyuge
    if(bandera == '1'):   
        sinFE=0                 #sin fecha de expiracion
        sinFN=0                 #sin fecha de nacimiento
        tipo=request.POST['tipoSM']
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
            idocu=Ocupacion.objects.get(Id=Profecion)     
        except:
            Profecion=""
        estadoF=1

        
        if(Profecion!=""):
            datos1 = DatosPersFia.objects.create(Tipo=tipo, NombreFiad=nombre, ApellidoFiad=apellido, DuiFiad=dui,LugarDuiFia=lugarExp,
        FechaDuiFia=fechaExp, FechaNaciFia=fechaNac,LugarNaciFia=lugarNac,EdadFiad=edad ,EstadoCiviFiad=aestadoCivil,
        GeneroFiad=Genero , IdOcupacionFia= idocu,EstadoFiad=estadoF, IdSolicitud=idSoli )
        else:
            datos1 = DatosPersFia.objects.create(Tipo=tipo, NombreFiad=nombre, ApellidoFiad=apellido, DuiFiad=dui,LugarDuiFia=lugarExp,
        FechaDuiFia=fechaExp, FechaNaciFia=fechaNac,LugarNaciFia=lugarNac,EdadFiad=edad ,EstadoCiviFiad=aestadoCivil,
        GeneroFiad=Genero ,EstadoFiad=estadoF, IdSolicitud=idSoli )
    #fin datos personales


    bandera= request.POST['passGP'] #inicia guardar grupo familiar
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

    bandera= request.POST['passDLM'] #inicia guardar domicilio y lugar de microempresa
    if(bandera == '1'):
       direActS =request.POST['direActS']# guarda direccion del solicitante
       puntoRefS =request.POST['puntoRefS']
       telefonoS =request.POST['telefonoS']
       condicionS =request.POST['condicionS']       
       resideS=request.POST['resideS']
       lugrTrabS =request.POST['lugrMicroS']
       actividadMicro =request.POST['actividadS']
       tiempoS =request.POST['tiempoS']       
       salarioS =request.POST['salarioS']
       if(salarioS==""):
            salarioS='0'
       direccionMS =request.POST['direccionMS']
       telefonoMS =request.POST['telefonoMS']
       tipo="Solicitante"

       domicilioS = Domicilio.objects.create(Direccion=direActS, Referencia=puntoRefS,Telefono=telefonoS, ResideDesd=resideS, 
       CondicionVivi=condicionS, LugarTrab=lugrTrabS,  ActividadMicr=actividadMicro, TiempoEmprTieFun=tiempoS, SalarioIngr=salarioS, 
       DireccionTrabMic=direccionMS, TelefonoTrabMic=telefonoMS, Tipo=tipo, IdSolicitud=idSoli) 
       
    bandera= request.POST['passDLMC'] #inicia guardar domicilio y lugar de microempresa
    if(bandera == '1'):
       
       direActC =request.POST['direActC']# guarda direccion del conyuge o codeudor     
       puntoRefC =request.POST['puntoRefC']
       telefonoC =request.POST['telefonoC']
       condicionC =request.POST['condicionC'] 
       resideC=request.POST['resideC']
       lugrTrabC =request.POST['lugrMicroC']
       actividadMicroC =request.POST['actividadC']
       tiempoC =request.POST['tiempoC']
       salarioC =request.POST['salarioC']
       if(salarioC==""):
            salarioC='0'
       direccionMC =request.POST['direccionMC']
       telefonoMC =request.POST['telefonoMC']
       tipo=request.POST['tipoSM']

       domicilioS = Domicilio.objects.create(Direccion=direActC, Referencia=puntoRefC,Telefono=telefonoC, ResideDesd=resideC, 
       CondicionVivi=condicionC, LugarTrab=lugrTrabC, ActividadMicr=actividadMicroC, TiempoEmprTieFun=tiempoC, SalarioIngr=salarioC, 
       DireccionTrabMic=direccionMC,TelefonoTrabMic=telefonoMC, Tipo=tipo, IdSolicitud=idSoli)
    #fin domicilio y lugar de microempresa 

    bandera= request.POST['passDOR'] #inicia guardar datos de la obra a realizar
    if(bandera == '1'):
       destinoME =request.POST['destinoME']
       duenoME =request.POST['duenoME']
       parentescoME =request.POST['parentescoME']
       direExacta=request.POST['direccionE'] 
       detalleObra =request.POST['detalleObra'] 
       detalleadic =request.POST['detalleAD']  
       PresupuestoME =request.POST['PresupuestoME']
       if(PresupuestoME==""):
            PresupuestoME='0'
       #print(destinoME)
       alternativa=Alternativa.objects.get(Id=destinoME)
       modeloVivienda= ModeloVivi.objects.get(Id=detalleObra)
       modeloVivienda.Id=detalleObra
       
       dor = DatosObra.objects.create(IdAlternativa=alternativa, Dueno= duenoME, Parentesco=parentescoME,DireccionExac=direExacta ,
      IdModeloVivi=modeloVivienda,DetalleAdic=detalleadic, Presupuesto=PresupuestoME, IdSolicitud=idSoli) 
    #fin datos de la obra a realizar


    bandera= request.POST['passDS'] #inicia guardar detalle de la solicitud
    if(bandera == '1'):
       montoME =request.POST['montoME']
       if(montoME==""):
            montoME='0'
       plazoME =request.POST['plazoME']
       cuotaME =request.POST['cuotaME']
       if(cuotaME==""):
            cuotaME='0'
       formaPagoME =request.POST['formaPagoME']   
       FechaPagoME =request.POST['FechaPagoME']

       ds = Detalle.objects.create(Monto=montoME, Plazo= plazoME, Cuota=cuotaME, 
      FormaPago=formaPagoME, FechaPago= FechaPagoME, IdSolicitud=idSoli) 
    #fin detalle de la solicitud

    bandera= request.POST['passEC'] #inicia experiencia crediticia
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

        #else:
           # print("paso")
            #experiencia = experienciCrediticia.objects.create( posee=1,estadoE=estadoE, idSolicitud=idSoli)
    #fin experiencia crediticia  


    bandera= request.POST['passRPF'] #inicia referencias personales y familiares
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
    
    bandera= request.POST['passCM'] #inicia guardar comentarios
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

    registroBit(request, "Se registro  formulario Solicitud Microempresa" + soli.IdPerfil.Dui, "Registro")
    
    return redirect('administrarPerfil', id=soli.IdPerfil.Id)  # id de perfil 
    

def modSoli(request):
# Inicia modifcar solicitud
#datos generales de la solicitd   ------------------------
    idSoli=request.POST['idSoli']
    tipoobra=request.POST['tipoobra']
    n= request.POST['nMod']
    comunidad= request.POST['comunidadMod']
    area= request.POST['areaMM']
    estado= request.POST['estadoMod']
    estado_soli=1
    if(estado=="Completado"):
        estado_soli=2

    soli = Solicitud.objects.get(Id=idSoli)
    soli.TipoObra = tipoobra
    soli.Numero = n
    soli.Comunidad = comunidad
    soli.Area = area
    soli.Estado = estado
    soli.EstadoSoli = estado_soli
    soli.save()

#Inicia modificar datos personales del solicitande -----    
    lugarExp=request.POST['lugExS']
    fechaExp=request.POST['fechExS']
    if(fechaExp==""):       #valido que la fecha no este vacia sino no guarda
            fechaExp="9999-01-01"
    lugarNac=request.POST['lugNaS']
    aestadoCivil=request.POST['estadoCivilS']
    Genero= request.POST['generoS']
    Profecion= request.POST['profecionS']
    #tipo="Solicitante"    
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
            'EstadoClie':'1',    
            'IdSolicitud':soli })
    

#Inicia modificar para el conyuge o codeudor
    bandera= request.POST['passDPMC']  # guarda datos personales
    if(bandera == '1'):  
        id= request.POST['idC']
        tipo=request.POST['tipoSM']
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
        idocu=Ocupacion.objects.get(Id=Profecion)
        
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
            'IdOcupacionFia': idocu,    
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
                'IdOcupacionFia': idocu,      
                'EstadoFiad':'1',      
                'IdSolicitud':soli })
            
#Inicia modificar grupo familiar
    idGP=request.POST.getlist('idGP')
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
            defaults={ 'Nombre':nombreGP[i], 
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

#Inicia modificar direccion del solicitante
    bandera= request.POST['passDLM'] 
    if(bandera == '1'):
        direActS =request.POST['direActS']
        puntoRefS =request.POST['puntoRefS']
        telefonoS =request.POST['telefonoS']
        condicionS =request.POST['condicionS']       
        resideS=request.POST['resideS']
        lugrTrabS =request.POST['lugrMicroS']
        actividadMicro =request.POST['actividadS']
        tiempoS =request.POST['tiempoS']
        
        salarioS =request.POST['salarioS']
        if(salarioS==""):
            salarioS=0.00
        direccionMS =request.POST['direccionMS']
        telefonoMS =request.POST['telefonoMS']
        tipo="Solicitante"
        print(salarioS)
        domicilioS = Domicilio.objects.update_or_create(IdSolicitud=soli,Tipo="Solicitante",
        defaults={ 'Direccion':direActS,
            'Referencia':puntoRefS,
            'Telefono':telefonoS, 
            'ResideDesd':resideS, 
            'CondicionVivi':condicionS,
            'LugarTrab':lugrTrabS,
            'ActividadMicr':actividadMicro,
            'TiempoEmprTieFun':tiempoS,
            'SalarioIngr':salarioS, 
            'DireccionTrabMic':direccionMS,       
            'TelefonoTrabMic':telefonoMS,}) 

#inicia actualizaar doicilio conyuge o codeudor
    bandera= request.POST['passDLMC'] 
    if(bandera == '1'):
        idd=request.POST['idDomicilioCC']   
        direActC =request.POST['direActC']
        puntoRefC =request.POST['puntoRefC']
        telefonoC =request.POST['telefonoC']
        condicionC =request.POST['condicionC']       
        resideC=request.POST['resideC']
        lugrTrabC =request.POST['lugrMicroC']
        actividadMicro =request.POST['actividadC']
        tiempoC =request.POST['tiempoC']
        salarioC =request.POST['salarioC']
        if(salarioC==""):
            salarioC=0
        direccionMC =request.POST['direccionMC']
        telefonoMC =request.POST['telefonoMC']
        tipo=request.POST['tipoSM']

        if(idd==""):
                domicilioC = Domicilio.objects.update_or_create(IdSolicitud=idSoli, tipo=tipo,
            defaults={ 'Direccion':direActC,
                'Referencia':puntoRefC,
                'Telefono':telefonoC, 
                'ResideDesd':resideC, 
                'CondicionVivi':condicionC,
                'LugarTrab':lugrTrabC,
                'ActividadMicr':actividadMicro,
                'TiempoEmprTieFun':tiempoC,
                'SalarioIngr':salarioC, 
                'DireccionTrabMic':direccionMC,        
                'TelefonoTrabMic':telefonoMC,
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
                'ActividadMicr':actividadMicro,
                'TiempoEmprTieFun':tiempoC,
                'SalarioIngr':salarioC, 
                'DireccionTrabMic':direccionMC,        
                'TelefonoTrabMic':telefonoMC,
                'Tipo':tipo,
                'IdSolicitud':soli}) 

#Inicia modificar datos de la obra a realiar
    bandera= request.POST['passDOR'] 
    if(bandera == '1'):
        destinoME =request.POST['destinoME']
        duenoME =request.POST['duenoME']
        parentescoME =request.POST['parentescoME']
        direExacta=request.POST['direccionE'] 
        detalleObra =request.POST['detalleObra']   
        PresupuestoME =request.POST['PresupuestoME']
        if(PresupuestoME==""):
            PresupuestoME=0.00
        detalleAlt=Alternativa.objects.get(Id=destinoME)
        detalleObra=ModeloVivi.objects.get(Id=detalleObra)
        dor = DatosObra.objects.update_or_create(IdSolicitud=idSoli,
        defaults={ 'IdAlternativa':detalleAlt, 
        'Dueno': duenoME, 
        'Parentesco':parentescoME, 
        'DireccionExac':direExacta, 
        'IdModeloVivi':detalleObra, 
        'Presupuesto':PresupuestoME, 
        'IdSolicitud':soli}) 
    
#Inicia modificar detalle de la solicitud  
    bandera= request.POST['passDS'] 
    if(bandera == '1'):
        montoME =request.POST['montoME']
        if(montoME==""):
            montoME=0
        plazoME =request.POST['plazoME']
        cuotaME =request.POST['cuotaME']
        if(cuotaME==""):
            cuotaME=0
        formaPagoME =request.POST['formaPagoME']   
        FechaPagoME =request.POST['FechaPagoME']
        
        ds = Detalle.objects.update_or_create(IdSolicitud=idSoli, 
        defaults={ 'Monto':montoME, 
        'Plazo': plazoME, 
        'Cuota':cuotaME, 
        'FormaPago':formaPagoME, 
        'FechaPago': FechaPagoME, 
        'IdSolicitud':soli})

#Inicia modificar experiencia crediticia
    idExC=request.POST.getlist('idExC')
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
                defaults={'Lugar':lugarEC[i],
            'Monto':montoEC[i], 
            'FechaOtor':fechaEC[i],
            'Estado':estadoEC[i],  
            'Cuota':cuotaEC[i], 
            'PoseeExpe':False,
            'IdSolicitud':soli})  

#inicia modificar referencias personales
    idRF=request.POST.getlist('idRF')
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
    bandera= request.POST['passCM'] #inicia guardar comentarios
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
        

    registroBit(request, "Se actualizo formularSolicitud Microempresa " + soli.IdPerfil.Dui, "Actualizacion")
    return redirect('administrarPerfil', id=soli.IdPerfil.Id)  # id de perfil 

# lista de reportes para el comite
def listaRF(request,id):
    listSoli = Solicitud.objects.filter(Estado="Completado", Tipo="micro",EstadoSoli=3,IdPerfil__IdAgencia=id)
    return render(request, "SolicitudesApp/listaReportesF.html", {"solicitudes":listSoli})

def listaRFAdmin(request):
    listaAg=Agencia.objects.all()
    return render(request, "SolicitudesApp/listaReportesFAdmin.html", {"agencia":listaAg})

def agencRFA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Estado="Completado", Tipo="micro",EstadoSoli=3, IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")


#########################################################
#lista de solicitudes pendientes de aprobacion 
def listaSolicitudesPA(request,id): 
    # consulta las solicitudes que estan activas y pendientes de aprobacion
    listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=3, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)

    return render(request, "SolicitudesApp/listaSolicitudPA.html", {"solicitudes":listperpa})

#lista de solicitudes pendientes de aprobacion  Admin
def listaSolicitudesPAAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "SolicitudesApp/listaSolicitudPAAdmin.html", {"agencia":listaAg})

def agencPAA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=3, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            print(listperpa)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")


#lista de solicitudes aprobadas
def listaSolicitudesApr(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=4, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "SolicitudesApp/listaSAprobadas.html", {"solicitudes":listperpa})

#lista de solicitudes aprobadas Admin
def listaSolicitudesAprAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "SolicitudesApp/listaSAprobadasAdmin.html", {"agencia":listaAg})

def agencAA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=4, IdPerfil__EstadoSoli=11, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

def evaluarSol(request, id): 
    try:
        s = Solicitud.objects.get(Id=id)
    except Solicitud.DoesNotExist:
        s=""
    try:
        dt=Detalle.objects.get(IdSolicitud=s.Id)
    except Detalle.DoesNotExist:
        dt=""

    return render(request, "SolicitudesApp/evaluarSolicitud.html", {"s":s,"dt":dt})

def evaluarSolApr(request, id): 
    try:
        s = Solicitud.objects.get(Id=id)
    except Solicitud.DoesNotExist:
        s=""
    try:
        dt=Detalle.objects.get(IdSolicitud=s.Id)
    except Detalle.DoesNotExist:
        dt=""

    return render(request, "SolicitudesApp/modificarEvaluarSolicitud.html", {"s":s,"dt":dt})

def evaluarSolObs(request, id): 
    try:
        s = Solicitud.objects.get(Id=id)
    except Solicitud.DoesNotExist:
        s=""
    try:
        dt=Detalle.objects.get(IdSolicitud=s.Id)
    except Detalle.DoesNotExist:
        dt=""

    return render(request, "SolicitudesApp/modificarEvaluarSolicitud.html", {"s":s,"dt":dt})

def evaluarSolDen(request, id): 
    try:
        s = Solicitud.objects.get(Id=id)
    except Solicitud.DoesNotExist:
        s=""
    try:
        dt=Detalle.objects.get(IdSolicitud=s.Id)
    except Detalle.DoesNotExist:
        dt=""

    return render(request, "SolicitudesApp/modificarEvaluarSolicitud.html", {"s":s,"dt":dt})


def registrarEvaluacion(request):
    id=request.POST['ids']
    eval=request.POST['evaluacion'] # si es 4 = aprobado, 5 = observado, 6= denegado
    try:
        obs=request.POST['observacion']
    except :
        obs=""
    #print(id)
    evaluar=""
    if eval==4:
        evaluar="Aprobo"
    elif eval==5:
        evaluar="Observo"
    elif eval==6:
        evaluar="Denego"
    else:
        evaluar="Evaluo"
    msol=Solicitud.objects.get(Id=id)
    msol.EstadoSoli=eval
    msol.Observaciones=obs
    msol.save()
    ida=msol.IdPerfil.IdAgencia
    ag=ida.Id
    mensaje="Datos guardados"
    registroBit(request, "Se "+ evaluar +" la solicitud " + msol.IdPerfil.Dui, "Evaluacion")
    messages.success(request, mensaje)
    usua=request.user.iduser
    usu=Usuario.objects.get(iduser=usua)
    if usu.cargo==1 or usu.cargo==6:
        if msol.Tipo=='micro':
            return redirect('listaSolicitudesPAAdmin')
        else:   
            return nat.listaSolicitudesPAAdmin(request)
    else:
        if msol.Tipo=='micro':
            return redirect('listaSolicitudesPA', ag)
        else:   
            return nat.listaSolicitudesPA(request, ag)

def modificarEvaluacion(request):
    id=request.POST['ids']
    eval=request.POST['evaluacion'] # si es 4 = aprobado, 5 = observado, 6= denegado
    try:
        obs=request.POST['observacion']
    except :
        obs=""
    #print(id)
    evaluar=""
    if eval==4:
        evaluar="Aprobo"
        mensj="Se "+ evaluar +" la solicitud "
    elif eval==5:
        evaluar="Observo"
        mensj="Se "+ evaluar +" la solicitud "
    elif eval==6:
        evaluar="Denego"
        mensj="Se "+ evaluar +" la solicitud "
    else:
        evaluar="Evaluo"
        mensj="Se "+ evaluar +" la solicitud "
    msol=Solicitud.objects.get(Id=id)
    msol.EstadoSoli=eval
    msol.Observaciones=obs
    msol.save()
    ida=msol.IdPerfil.IdAgencia
    ag=ida.Id
    
    mensaje="Datos actualizados"
    registroBit(request, mensj + msol.IdPerfil.Dui, "Evaluacion")
    messages.success(request, mensaje)
    usua=request.user.iduser
    usu=Usuario.objects.get(iduser=usua)
    if usu.cargo==1 or usu.cargo==6:
        if msol.Tipo=='micro':
            return redirect('listaSolicitudesPAAdmin')
        else:   
            return nat.listaSolicitudesPAAdmin(request)
    else:
        if msol.Tipo=='micro':
            return redirect('listaSolicitudesPA', ag)
        else:   
            return nat.listaSolicitudesPA(request, ag)
    

#lista de solicitudes observadas= 5
def listaSolicitudesObs(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=5, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "SolicitudesApp/listaSObservadas.html", {"solicitudes":listperpa})

#lista de solicitudes observadas  Admin
def listaSolicitudesObsAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "SolicitudesApp/listaSObservadasAdmin.html", {"agencia":listaAg})

def agencOA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=5, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

#lista de solicitudes  denegadas=6
def listaSolicitudesDen(request,id): 
    listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=6, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
    return render(request, "SolicitudesApp/listaSDenegadas.html", {"solicitudes":listperpa})

#lista de solicitudes denegadas  Admin
def listaSolicitudesDenAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "SolicitudesApp/listaSDenegadasAdmin.html", {"agencia":listaAg})

def agencDA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listperpa=""
    if request.is_ajax():
        try:
            listperpa = Solicitud.objects.filter(Tipo="micro",EstadoSoli=6, IdPerfil__Estado='activo', IdPerfil__IdAgencia=id)
            for item in listperpa:
                lista_agenciaC.append({"id":item.Id,"dui":item.IdPerfil.Dui, "nombre":item.IdPerfil.Nombres, "apellido":item.IdPerfil.Apellidos,"telefono":item.IdPerfil.Telefono, "agencia":item.IdPerfil.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

def obtenerRango(request):
    id = request.GET['id']   
    alternativa = "-0"
    if request.is_ajax():  
        try: 
            alternativa = Alternativa.objects.get(Id=id) 
            serialized_data =  serialize("json", [ alternativa ])
        except Exception: 
            serialized_data = json.dumps( alternativa , default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})