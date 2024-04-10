from django.shortcuts import render, redirect
from django.contrib import messages
from ClienteApp.models import Perfil
from SolicitudesApp.models import *
from DeclaracionJurClienteApp.models import *
from TesisApp.views import registroBit

# Create your views here.

def declaracionjc(request, id):

    sol= DeclaracionJuraCli.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= DeclaracionJuraCli.objects.get(IdSolicitud=id)
    
        return redirect('editarDJ', id=solv.Id)     
    else:
        try:
            listato=TipoOper.objects.filter(Estado="activo")
        except TipoOper.DoesNotExist:
            listato=""
        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
        try:
            d=  Detalle.objects.get(IdSolicitud=id)
        except Detalle.DoesNotExist:
            d=""
        return render(request, "DeclaracionJurClienteApp/declaracionjc.html", {"s":s,"d":d,"operaciones":listato}) 

def registrarDj(request): 
  
    ids=request.POST['ids']
    nombrepna=request.POST['nombrepn']
    duipna=request.POST['ndui']
    toperacion=request.POST['tipoop']
    ncredito=request.POST['ncredito']
    monto=request.POST['monto']   
    plazo=request.POST['plazo']
    cuota=request.POST['cuota']
    formapago=request.POST['fpago']
    cancelacionda=request.POST['creditocan']
    rpagosa=request.POST['rpagosa']
    try:
       procedenciafond=request.POST['procedenciaf']
    except :
        procedenciafond=""
    
    idto=TipoOper.objects.get(Id=toperacion)
    idto.Id=toperacion
    idsol= Solicitud.objects.get(Id=ids)
    idsol.Id=ids 

    declaracionjc= DeclaracionJuraCli.objects.create(NombrePersNat=nombrepna,DuiPersNat=duipna,IdTipoOper=idto,NumeroCred=ncredito,Monto=monto,Plazo=plazo,Cuota=cuota,FormaPago=formapago,CanceladoAcueCuo=cancelacionda,RealizarPagoAdi=rpagosa,ProcedenciaFond=procedenciafond,IdSolicitud=idsol)
   
    iddjc= DeclaracionJuraCli.objects.all().last() #obtengo la ultima declaracion registrada 


    bandera= request.POST['passAE']  # guarda datos de 
    if(bandera == '1'):
        try:
            empleadoen=request.POST['empleadoen']
        except :
            empleadoen=""
        try:
            profecinalind=request.POST['profecionind']
        except :
            profecinalind=""  
        try:
            conocimientoen=request.POST['conocimientoen']
        except :
            conocimientoen=""   
        try:
            empresarioen=request.POST['empresarioen']
        except :
            empresarioen=""   
        try:
            especificaro=request.POST['otrosesp']
        except :
            especificaro=""   
        
       
    declaracionjcaern=DeclaracionActiEco.objects.create(EmpleadoEn=empleadoen,ProfecionalInde=profecinalind,ConocimientosEn=conocimientoen,EmpresarioEn=empresarioen,EspecificarOtraAct=especificaro,IdDeclaracionJuraCli=iddjc)
   
    bandera= request.POST['passGN']  # guarda datos de 
    if(bandera == '1'):
        
        try:
            empresa=request.POST['empresad']
        except :
            empresa=""  
        try:
            industriade=request.POST['industiad']
        except :
            industriade=""  
        try:
            comercio=request.POST['comerciod']
        except :
            comercio=""  
        try:
            especificarot=request.POST['espotros']
        except :
            especificarot=""  
       
    declaracionjcjnm=DeclaracionJiroNeg.objects.create(Empresa=empresa,IndustriaDe=industriade,ComercioDe=comercio,EspecificarOtro=especificarot,IdDeclaracionJuraCli=iddjc)
   
    mensaje="Datos guardados"
    registroBit(request, "Se registro Declaracion Jurada " + nombrepna, "Registro")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=declaracionjc.IdSolicitud.IdPerfil.Id)  # id de perfil 

def listaDJ(request,id):
    listj=  DeclaracionJuraCli.objects.filter(IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "DeclaracionJurClienteApp/listaDJ.html", {"listj":listj})

def editarDJ(request, id):
    listato=TipoOper.objects.all()

    try:
        dj=  DeclaracionJuraCli.objects.get(Id=id)
    except DeclaracionJuraCli.DoesNotExist:
        dj=""
    try:
        dja=  DeclaracionActiEco.objects.get(Id=id)
    except DeclaracionActiEco.DoesNotExist:
        dja=""
    try:
        djn=  DeclaracionJiroNeg.objects.get(Id=id)
    except DeclaracionJiroNeg.DoesNotExist:
        djn=""
    idSol=dj.IdSolicitud.Id
    try:
        s=  Solicitud.objects.get(Id=idSol)
    except Solicitud.DoesNotExist:
        s=""

    try:
        d=  Detalle.objects.get(IdSolicitud=idSol)
    except Detalle.DoesNotExist:
        d=""

    return render(request, "DeclaracionJurClienteApp/editarDeclaracionjc.html", {"s":s,"d":d,"operaciones":listato,"dj":dj,"dja":dja,"djn":djn}) 


def modificarDJ(request): 
  
    idj=request.POST['idj']
    nombrepna=request.POST['nombrepn']
    duipna=request.POST['ndui']
    toperacion=request.POST['tipoop']
    ncredito=request.POST['ncredito']
    monto=request.POST['monto']   
    plazo=request.POST['plazo']
    cuota=request.POST['cuota']
    formapago=request.POST['fpago']
    cancelacionda=request.POST['creditocan']
    rpagosa=request.POST['rpagosa']
    try:
       procedenciafond=request.POST['procedenciaf']
    except :
        procedenciafond=""
    
    idto=TipoOper.objects.get(Id=toperacion)
    idto.Id=toperacion

    declaracionjc= DeclaracionJuraCli.objects.get(Id=idj)
    declaracionjc.NombrePersNat=nombrepna
    declaracionjc.DuiPersNat=duipna
    declaracionjc.IdTipoOper=idto
    declaracionjc.NumeroCred=ncredito
    declaracionjc.Monto=monto
    declaracionjc.Plazo=plazo
    declaracionjc.Cuota=cuota
    declaracionjc.FormaPago=formapago
    declaracionjc.CanceladoAcueCuo=cancelacionda
    declaracionjc.RealizarPagoAdi=rpagosa
    declaracionjc.ProcedenciaFond=procedenciafond
    declaracionjc.save()


    bandera= request.POST['passAE']  # guarda datos de 
    if(bandera == '1'):
        try:
            empleadoen=request.POST['empleadoen']
        except :
            empleadoen=""
        try:
            profecinalind=request.POST['profecionind']
        except :
            profecinalind=""  
        try:
            conocimientoen=request.POST['conocimientoen']
        except :
            conocimientoen=""   
        try:
            empresarioen=request.POST['empresarioen']
        except :
            empresarioen=""   
        try:
            especificaro=request.POST['otrosesp']
        except :
            especificaro=""   
        
       
    declaracionjcaern=DeclaracionActiEco.objects.get(IdDeclaracionJuraCli=idj)
    declaracionjcaern.EmpleadoEn=empleadoen
    declaracionjcaern.ProfecionalInde=profecinalind
    declaracionjcaern.ConocimientosEn=conocimientoen
    declaracionjcaern.EmpresarioEn=empresarioen
    declaracionjcaern.EspecificarOtraAct=especificaro
    declaracionjcaern.save()
   
    bandera= request.POST['passGN']  # guarda datos de 
    if(bandera == '1'):
        
        try:
            empresa=request.POST['empresad']
        except :
            empresa=""  
        try:
            industriade=request.POST['industiad']
        except :
            industriade=""  
        try:
            comercio=request.POST['comerciod']
        except :
            comercio=""  
        try:
            especificarot=request.POST['espotros']
        except :
            especificarot=""  
       
    declaracionjcjnm=DeclaracionJiroNeg.objects.get(IdDeclaracionJuraCli=idj)
    declaracionjcjnm.Empresa=empresa
    declaracionjcjnm.IndustriaDe=industriade
    declaracionjcjnm.ComercioDe=comercio
    declaracionjcjnm.EspecificarOtro=especificarot
    declaracionjcjnm.save()
   
    mensaje="Datos actualizados"
    registroBit(request, "Se actualizó Declaración Jurada " + nombrepna, "Actualización")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=declaracionjc.IdSolicitud.IdPerfil.Id)  
 

