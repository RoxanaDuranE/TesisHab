from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from ClienteApp.models import *
from HistorialApp.models import *
from EvaluacionIvEFApp.models import *
from EvaluacionMicroApp.models import *
from ListaChequeoApp.models import ListaCheq
import json
from django.db.models import Q

from TesisApp.views import registroBit


# Create your views here.


def listaPerfil(request): 
    listper=Perfil.objects.filter(Estado="activo")
    return render(request, "HistorialApp/listaHis.html", {"perfil":listper})

def rangoHist(request):
    return render(request, "HistorialApp/rangoHis.html")

def registroHis(request):
    hismax=request.POST['histmax']
    hismin=request.POST['histmin']
    est= request.POST['est']
    porc=request.POST['porc']
    try:
        estado= RangoHist.objects.filter(Tipo=est).exists()
    except:
        estado=False
    try: 
        superpuesto = RangoHist.objects.filter(Q(Minimo__lte=hismax, Maximo__gte=hismin)).exists()
    except:
        superpuesto=''
    #return not superpuesto


    if estado == True or superpuesto == True:
        mensaje="Ese rango DICOM ya existe o pertenece a otro rango"
        messages.warning(request, mensaje)
    else:
        rango=RangoHist.objects.create(Minimo=hismin, Maximo=hismax, Tipo=est, Porcentaje=porc)
        
        mensaje="Rango registrado"
        registroBit(request, "Se registro rango DICOM " + est, "Registro")

        messages.success(request, mensaje)

    return redirect("rangoh")

def listaRango(request): 
    rango=RangoHist.objects.all()
    return render(request, "HistorialApp/listaRang.html", {"rango":rango})

#Modificar rangos de historial

def editarRango(request, idr):
    
    try:
        rango = RangoHist.objects.get(Id=idr)
    except RangoHist.DoesNotExist:
        rango=""

    return render(request, "HistorialApp/editrangoHis.html", {"rango":rango})

def modificarRango(request ):
    hismax=request.POST['histmax']
    hismin=request.POST['histmin']
    est= request.POST['est']
    porc=request.POST['porc']

    try:
        estado= RangoHist.objects.filter(Tipo=est).exists()
    except:
        estado=False
    try: 
        superpuesto = RangoHist.objects.filter(Q(id!=id, Minimo__lte=hismax, Maximo__gte=hismin)).exists()
    except:
        superpuesto=''
    #return not superpuesto


    if estado == True or superpuesto == True:
        mensaje="Ese rango DICOM ya existe o pertenece a otro rango"
        messages.warning(request, mensaje)
    else:
        rango=RangoHist.objects.create(Minimo=hismin, Maximo=hismax, Tipo=est, Porcentaje=porc)
        
        mensaje="Rango modificado"
        registroBit(request, "Se actualizó rango DICOM " + est, "Actualización")

        messages.success(request, mensaje)

    return '/'


#Resgistrar puntaje del cliente
def regisRanCli(request, id):
    
    per = Solicitud.objects.get(Id=id)
    ran = RangoHist.objects.all()
    ran_data = list(ran.values())
     # Serializa el campo Decimal usando la función personalizada y el DjangoJSONEncoder
    for item in ran_data:
        if 'Porcentaje' in item:
            item['Porcentaje'] = float(item['Porcentaje'])
            
    ran_json = json.dumps(ran_data, default=str)# Convertir la lista a JSON
    return render(request, "HistorialApp/regisRangoCli.html", {"per": per, "ran_json": ran_json, "ran":ran})



def regisPunt(request):
    fe=request.POST['fec']
    punt=request.POST['punt']
    idp=request.POST['idp']
    idh= request.POST['idh']

    idpr=Solicitud.objects.get(Id= idp)
    idpr.Id=idp
    idhi= RangoHist.objects.get(Id=idh)
    idhi.Id=idh
    if idpr.Tipo=='micro':
        eva= BalanceSituMic.objects.get(IdPerfil=idpr.IdPerfil,Estado=1)
        
    else:
        eva=EgresosFami.objects.get(IdPerfil=idpr.IdPerfil,Estado=1)
    try:
        regis=RegistroHist.objects.filter(IdSolicitud=idpr).exists()
    except:
        regis=False
    if(regis != True):
        print(regis)
        if(idhi.Porcentaje==0):
            regis=RegistroHist.objects.create(Puntaje=punt, Fecha=fe, IdRango=idhi, IdSolicitud=idpr)
            idpr.Observaciones="Su puntaje de DICOM no aplica para financiamiento"
            idpr.EstadoSoli=6 #Denegar la solicitud porque el puntaje es muy bajo
            idpr.save()
            idpr.IdPerfil.EstadoSoli=10 # Indicar en perfil que ya se registro dicom
            idpr.IdPerfil.save()
            eva.Estado=2 #Desactivar evaluacion si el DICOM es bajo
            eva.save()
                    
            mensaje="Su solicitud de credito NO procede, su puntaje DICOM es muy bajo"
            registroBit(request, "Se registro puntaje DICOM bajo del cliente " + idpr.IdPerfil.Dui, "Registro")

        else:# El 65% de su credito al que puede aplicar
            regis=RegistroHist.objects.create(Puntaje=punt, Fecha=fe, IdRango=idhi, IdSolicitud=idpr)
            if idpr.IdPerfil.EstadoSoli<10:
                idpr.IdPerfil.EstadoSoli=10
                idpr.IdPerfil.save()
            else:
                idpr.IdPerfil.save()
            mensaje="Puntaje DICOM registrado"
            registroBit(request, "Se registro puntaje DICOM del cliente " + idpr.IdPerfil.Dui, "Registro")

        messages.success(request, mensaje)
    else:
        mensaje="La solicitud ya posee un puntaje registrado"
    # puntaje es mayor a 450 y menor o igual a 550 el 75% del credito
    #puntaje mayor a 550 y menor o igual a 999 el 100% de lo solicitado 
    #mensaje="Puntaje registrado"
        messages.warning(request, mensaje)

         #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.get(IdSolicitud=idpr)
    lchequo.InformeDico ="Si"
    lchequo.save()
    return redirect('administrarPerfil', id=idpr.IdPerfil.Id)



def listaPerfil(request): 
    listper=Perfil.objects.filter(Estado="activo")
    return render(request, "HistorialApp/listaHis.html", {"perfil":listper})

# Editar puntaje
def listaPunCli(request):
    listaRanC=RegistroHist.objects.all()
    return render(request, "HistorialApp/listaPuntaje.html", {"puntaje":listaRanC})

def editarPuntCli(request, idpCli):
    punC = RegistroHist.objects.get(Id=idpCli)
    #falta sacar el rango 
    #dire = Agencia.objects.only('municipio','direccion','telefono','telefono2')
    try:
        listarDepto=Departamento.objects.all()
    except Departamento.DoesNotExist:
        listarDepto=""  
    try:
        rango = RangoHist.objects.all()
    except RangoHist.DoesNotExist:
        rango=""

     # Convertir la lista a JSON
    rango_json = json.dumps(list(rango.values()), default=str)  


    return render(request, "HistorialApp/editRangoCli.html", {"punC":punC, "rango_json": rango_json})

def modificarPuntajeC(request):
    
    idpu=request.POST['idp']
    idh=request.POST['idh']
    puntaje=request.POST['punt']
    
    idpr=Solicitud.objects.get(Id= idpu)
    idpr.Id=idpu
    ranh=RangoHist.objects.get(Id=idh)
    puntC=RegistroHist.objects.get(Id=idpu)
    if puntC.IdSolicitud.Tipo=='micro':
        eva= BalanceSituMic.objects.get(IdPerfil=puntC.IdSolicitud.IdPerfil.Id)
        
    else:
        eva=EgresosFami.objects.get(IdPerfil=puntC.IdSolicitud.IdPerfil.Id)
    #Validar que si el rango guardado es menor a 400 debe modificar el estado de la solicitud, perfil y evaluacion
    if(puntC.IdRango.Porcentaje==0 and ranh.Porcentaje>0):
        puntC.IdSolicitud.Observaciones='NULL'
        puntC.IdSolicitud.EstadoSoli=3
        puntC.save()
        
        #puntC.IdSolicitud.IdPerfil.EstadoSoli=10
        #puntC.IdSolicitud.IdPerfil.save()
        eva.Estado=1
        eva.save()
        puntC.Puntaje=puntaje
        puntC.IdRango=ranh
        puntC.save()
        
        mensaje="Puntaje DICOM actualizado"
        registroBit(request, "Se actualizó puntaje DICOM del cliente " + puntC.IdSolicitud.IdPerfil.Dui, "Actualización")

    elif (puntC.IdRango.Porcentaje>0 and ranh.Porcentaje==0):
        puntC.IdSolicitud.Observaciones='Su puntaje de DICOM no aplica para financiamiento'
        puntC.IdSolicitud.EstadoSoli=3
        puntC.save()
       # puntC.IdSolicitud.IdPerfil.EstadoSoli=10
        #puntC.IdSolicitud.IdPerfil.save()
        eva.Estado=2
        eva.save()
        puntC.Puntaje=puntaje
        puntC.IdRango=ranh
        puntC.save()
        mensaje="Puntaje DICOM actualizado. Puntaje no aplica para credito"
        registroBit(request, "Se actualizó puntaje DICOM del cliente " + puntC.IdSolicitud.IdPerfil.Dui + " No aplica para credito", "Actualización")
    else:# Si el porcentaje es mayor a 0 la solicitud no es denegada y sigue su proceso
           
        puntC.Puntaje=puntaje
        puntC.IdRango=ranh
        puntC.save()
        #puntC.IdSolicitud.IdPerfil.EstadoSoli=10
        #puntC.IdSolicitud.IdPerfil.save()
        mensaje="Datos actualizados"
        registroBit(request, "Se actualizó puntaje DICOM del cliente " + puntC.IdSolicitud.IdPerfil.Dui, "Actualización")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=puntC.IdSolicitud.IdPerfil.Id)


def con(request):
    dire = Agencia.objects.only('Municipio','Direccion')
    return render(request,"ConfiguracionApp/consulta.html",{"dire":dire})  
