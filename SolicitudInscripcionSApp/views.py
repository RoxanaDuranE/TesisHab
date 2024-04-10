from django.shortcuts import render, redirect
from django.contrib import messages
from ClienteApp.models import Perfil
from ListaChequeoApp.models import ListaCheq
from SolicitudesApp.models import *
from SolicitudInscripcionSApp.models import *
from django.db.models import Subquery
from django.db.models import Q
import json

from TesisApp.views import registroBit

# Create your views here.

def solicitudI(request, id):
    sol= SolicitudInscSeg.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= SolicitudInscSeg.objects.get(IdSolicitud=id)
    
        return redirect('editarSIS', id=solv.Id)   
    else:
        try:
            s= Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""

        try:
            dp=DatosPers.objects.get(IdSolicitud=id)
        except DatosPers.DoesNotExist:
            dp=""

        try:
            d=  Domicilio.objects.get(IdSolicitud=id, Tipo="Solicitante")
        except Domicilio.DoesNotExist:
            d=""
        
        try:
            dt=  Detalle.objects.get(IdSolicitud=id)
        except Detalle.DoesNotExist:
            dt=""
            
        try:
            listae=SolicitudInscSegEnf.objects.filter(Estado="activo",Personal="No")
        except SolicitudInscSegEnf.DoesNotExist:
            listae=""

        
        return render(request, "SolicitudInscripcionSApp/solicitud.html", {"s":s, "dp":dp, "d":d, "dt":dt,"enfermedades":listae})


def registrarDs(request): 
  
    ids=request.POST['ids']
    montoaa=request.POST['montoaa']
    nuevoma=request.POST['nuevom']
    montot=request.POST['montot']
    plazo=request.POST['plazo']
    garantia=request.POST['garantia']
    estatura=request.POST['estatura']
    peso=request.POST['peso']
    dbeneficiario=request.POST['beneficiario']

    if(montoaa=="" ):
        montoaa = 0.00
    if(nuevoma=="" ):
        nuevoma = 0.00
    if(montot=="" ):
        montot = 0.00

    idsol= Solicitud.objects.get(Id=ids)
    idsol.Id=ids 

    solicitudis=SolicitudInscSeg.objects.create(MontosAsegAnt=montoaa,NuevoMontAse=nuevoma,MontoTotaAse=montot,Plazo=plazo,Garantia=garantia,Estatura=estatura,Peso=peso,DesignoBene=dbeneficiario,IdSolicitud=idsol)

    idsi= SolicitudInscSeg.objects.all().last() #obtengo la ultima solicitud registrada 

    bandera= request.POST['passDS'] #inicia declaración de salud
    if(bandera == '1'):
       idsisenf =request.POST.getlist('idenf')
       idperfil =request.POST.getlist('idc') #identificador del cliente 
       fechap =request.POST.getlist('fechapad') 
       tratamientor =request.POST.getlist('tratamientor')
       situaciona =request.POST.getlist('situaciona')
       estado="activo"
       
       for i in range(len(fechap)):
        if (fechap[i] != ""):
            sispadecimiento = SolicitudInscSegPad.objects.create(IdSolicitudInscSegEnf=SolicitudInscSegEnf.objects.get(Id=idsisenf[i]), IdPerfil=Perfil.objects.get(Id=idperfil[i]), FechaPade=fechap[i],
             TratamientoReci =tratamientor[i],  SituacionActu=situaciona[i], Estado=estado)
    #fin declaración de salud  

    # Inicia otro padecimiento
    try:
        personal=request.POST['personal']
    except :
        personal=""
    try:
        nombreenf=request.POST['padecimientoOt'].upper() 
    except :
        nombreenf=""

    estadoenf="activo" 
    enf=SolicitudInscSegEnf.objects.filter(NombreEnfe=nombreenf).exists()
    
    if enf == True:
            mensaje="la enfermedad o padecimiento ya existe"
            messages.warning(request, mensaje)
    elif nombreenf != "":
        enfermedades=SolicitudInscSegEnf.objects.create(NombreEnfe=nombreenf,Estado=estadoenf,Personal=personal)
        # Obtener el ID de la instancia de enfermedades
        siseid= SolicitudInscSegEnf.objects.get(Id=enfermedades.Id)
        siseid.Id = enfermedades.Id

        fechapO = request.POST.get('fechaOt', None) # si no se selecciona una fecha establece un valos vacio

        try:
            tratamientorO=request.POST['tratamientoOt']
        except :
            tratamientorO=""
        try:
            situacionaO=request.POST['situacionOt']
        except :
            situacionaO=""

        sispadecimientoOt = SolicitudInscSegPad.objects.create(IdSolicitudInscSegEnf=siseid, IdPerfil=Perfil.objects.get(Id=request.POST['idpot']), FechaPade=fechapO,
                TratamientoReci =tratamientorO, SituacionActu=situacionaO, Estado=estado)

    # fin otro padecimiento

    bandera= request.POST['passDO']  # guarda datos de declaracion de deformidades, amputaciones o defecto fisico
    if(bandera == '1'):
        tienedadf=request.POST['tiened']
        try:
            detallesdadf=request.POST['detalled']
        except :
            detallesdadf=""
        
        fumacp=request.POST['fumacp']
        try:
           cuantosd=request.POST['cuantosd']
        except :
            cuantosd=""
        
        bebidadalc=request.POST['ibebidas']
        try:
           frecuenciaalc=request.POST['frecuanciab']
        except :
            frecuenciaalc=""
       
        tratamientomd=request.POST['tratamientomd']
        try:
           detalletmd=request.POST['detalletm']
        except :
            detalletmd=""
        
        practicaad=request.POST['practicaadp']   
        try:
           clasead=request.POST['clase']
        except :
            clasead=""
        try:
          frecuenciaad=request.POST['frecuencia']
        except :
            frecuenciaad=""
        
        segurodd=request.POST['segurod']
   


    solicitudisdadf=SolicitudInscSegDefAmpDefFis.objects.create(TieneDefoAmpDefFis=tienedadf,DetallesDefoAmpDefFis=detallesdadf,FumaCigaPip=fumacp,CuantosDia=cuantosd,BebidasAlco=bebidadalc,FrecuenciaBebiAlc=frecuenciaalc,TratamientoMedi=tratamientomd,DetalleTratMed=detalletmd,PracticaActiDep=practicaad,ClaseActiDep=clasead,FrecuenciaActiDep=frecuenciaad,SeguroDese=segurodd,IdSolicitudInscSeg=idsi)
    
     #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.get(IdSolicitud=idsol)
    lchequo.DeclaracionSalu ="Si"
    lchequo.save()
    
    mensaje="Datos guardados"
    registroBit(request, "Se registro formulario Inscrippcion Seguro " + idsol.IdPerfil.Dui, "Regisrtro")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=solicitudis.IdSolicitud.IdPerfil.Id)  # id de perfil 
 

def listaIs(request,id):
    lists=  SolicitudInscSeg.objects.filter(IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "SolicitudInscripcionSApp/listaIS.html", {"lists":lists})


def editarSIS(request, id): # id de Solicitudis
    try:
        si=  SolicitudInscSeg.objects.get(Id=id)
    except SolicitudInscSeg.DoesNotExist:
        si=""
    try:
        sid=  SolicitudInscSegDefAmpDefFis.objects.get(IdSolicitudInscSeg=si.Id)
    except SolicitudInscSegDefAmpDefFis.DoesNotExist:
        sid=""
    
    idSol=si.IdSolicitud.Id
    try:
        s=  Solicitud.objects.get(Id=idSol)
    except Solicitud.DoesNotExist:
        s=""

    try:
        dp=DatosPers.objects.get(IdSolicitud=idSol)
    except DatosPers.DoesNotExist:
        dp=""

    try:
        d=  Domicilio.objects.get(IdSolicitud=idSol, Tipo="Solicitante")
    except Domicilio.DoesNotExist:
        d=""
    
    try:
        listae=SolicitudInscSegEnf.objects.filter(Estado="activo", Personal="No")
    except SolicitudInscSegEnf.DoesNotExist:
        listae=""
    
    #pad=SolicitudisPadecimiento.objects.filter(idp=s.perfil.id)
    #padgen=SolicitudisEnfermedad.objects.filter(estado="activo", personal="No", id__in=Subquery(pad))
    #padper=SolicitudisEnfermedad.objects.filter(estado="activo", personal="Si", id__in=Subquery(pad))
    #print(pad)

    # Consulta para obtener registros con personal="No" o personal="Si"
    resultados = SolicitudInscSegPad.objects.filter( Q(IdPerfil=s.IdPerfil.Id)  &  Q(IdSolicitudInscSegEnf__Personal="No")  ).distinct()

    lista_padecimientos=[]
    # Itera sobre los resultados
    for resultado in resultados:
        lista_padecimientos.append({'id':resultado.Id,'idenf':resultado.IdSolicitudInscSegEnf.Id,'enfermedad':resultado.IdSolicitudInscSegEnf.NombreEnfe,'fecha':(resultado.FechaPade).isoformat(),'tratamiento':resultado.TratamientoReci,'situacion':resultado.SituacionActu,})
    lista_padecimientos_json = json.dumps(lista_padecimientos)
    #print(lista_padecimientos_json)
        # Accede a los datos que necesitas, por ejemplo:
        #print(f"ID: {resultado.id},enfermedad: {resultado.idsisenf.nombreenf}, Fecha: {resultado.fechap}, Tratamiento: {resultado.tratamientor}, Situación: {resultado.situaciona}")
    
    
    # compruebo si la solicitud tiene una enfermedad personal
    conSi = SolicitudInscSegPad.objects.filter(Q(IdPerfil=s.IdPerfil.Id)  &   Q(IdSolicitudInscSegEnf__Personal="Si")).exists()

    if conSi==True:
        # Consulta para obtener registros con  personal="Si"
        resultadosSi = SolicitudInscSegPad.objects.get(Q(IdPerfil=s.IdPerfil.Id)  &  Q(IdSolicitudInscSegEnf__Personal="Si"))
        #for rS in resultadosSi:
        #print(f"ID: {resultadosSi.idsisenf.nombreenf}")
    else:
        resultadosSi =""


    
    return render(request, "SolicitudInscripcionSApp/editarSolicitud.html", {"s":s, "dp":dp, "d":d,"si":si,"sid":sid,"enfermedades":listae,"reSi":resultadosSi,"lista_padecimientos_json":lista_padecimientos_json})



def modificarSIS(request): 
  
    idsi=request.POST['idsi']
    montoaa=request.POST['montoaa']
    nuevoma=request.POST['nuevom']
    montot=request.POST['montot']
    plazo=request.POST['plazo']
    garantia=request.POST['garantia']
    estatura=request.POST['estatura']
    peso=request.POST['peso']
    dbeneficiario=request.POST['beneficiario']


    solicitudis=SolicitudInscSeg.objects.get(Id=idsi)
    solicitudis.MontosAsegAnt=montoaa
    solicitudis.NuevoMontAse=nuevoma
    solicitudis.MontoTotaAse=montot
    solicitudis.Plazo=plazo
    solicitudis.Garantia=garantia
    solicitudis.Estatura=estatura
    solicitudis.Peso=peso
    solicitudis.DesignoBene=dbeneficiario
    solicitudis.save()

    bandera= request.POST['passDS'] #inicia declaración de salud
    #print(bandera)
    if(bandera == '1'):
       idpd =request.POST.getlist('idpad')
       idsisenf =request.POST.getlist('idenf')
       idperfil =request.POST.getlist('idc') #identificador del cliente 
       fechap =request.POST.getlist('fechapad') 
       tratamientor =request.POST.getlist('tratamientor')
       situaciona =request.POST.getlist('situaciona')
       estado="activo"
      # print(idpd)

        # Iterar sobre los datos para crear o actualizar registros
    for i in range(len(idpd)):
        if i < len(fechap) and idpd[i] != "":
            # Si hay un valor válido en idsisenf, actualizar el objeto existente
            ssp_obj = SolicitudInscSegPad.objects.get(Id=idpd[i])
            msispadecimiento= SolicitudInscSegPad.objects.update_or_create( Id=ssp_obj.Id, 
                defaults={
                # 'idp': idperfil[i],
                    'FechaPade': fechap[i],
                    'TratamientoReci': tratamientor[i],
                    'SituacionActu': situaciona[i]
                }
            )
        elif fechap[i] != "":  # Si idimgp está vacío o no hay un valor válido en idpd, crear un nuevo objeto
            msispadecimiento = SolicitudInscSegPad.objects.create(IdSolicitudInscSegEnf=SolicitudInscSegPad.objects.get(Id=idsisenf[i]), IdPerfil=Perfil.objects.get(Id=idperfil[i]), FechaPade=fechap[i],
             TratamientoReci =tratamientor[i],  SituacionActu=situaciona[i], Estado=estado)
       
    #fin declaración de salud

     # Inicia otro padecimiento
    try:
        personal=request.POST['personal']
    except :
        personal=""
    try:
        nombreenf=request.POST['padecimientoOt'].upper() 
    except :
        nombreenf=""
   
    idpotp= request.POST['idpotp'] # id del padecimiento ingresado por el cliente
    fechapO = request.POST.get('fechaOt', None)
    try:
        tratamientorO=request.POST['tratamientoOt']
    except :
        tratamientorO=""
    try:
        situacionaO=request.POST['situacionOt']
    except :
        situacionaO=""

    estadoenf="activo" 
    enf=SolicitudInscSegEnf.objects.filter(NombreEnfe=nombreenf).exists()
    
    if  idpotp !="" :
        msispadecimientoOt = SolicitudInscSegPad.objects.get(Id=idpotp) # modifica los datos del padecimiento
        msispadecimientoOt.FechaPade=fechapO
        msispadecimientoOt.TratamientoReci =tratamientorO 
        msispadecimientoOt.SituacionActu=situacionaO
        msispadecimientoOt.save()

        menfermedades=SolicitudInscSegEnf.objects.get(Id=msispadecimientoOt.IdSolicitudInscSegEnf.Id)
        menfermedades.NombreEnfe=nombreenf
        menfermedades.save()
    elif enf == False and nombreenf != "" :
        enfermedades=SolicitudInscSegEnf.objects.create(NombreEnfef=nombreenf,Estado=estadoenf,Personal=personal)
        # Obtener el ID de la instancia de enfermedades
        siseid= SolicitudInscSegEnf.objects.get(Id=enfermedades.Id)
        siseid.Id = enfermedades.Id

        sispadecimientoOt = SolicitudInscSegPad.objects.create(IdSolicitudInscSegEnf=siseid, IdPerfil=Perfil.objects.get(Id=request.POST['idpot']), FechaPade=fechapO,
                TratamientoReci =tratamientorO, SituacionActu=situacionaO, Estado=estado)
    
    # fin otro padecimiento


    bandera= request.POST['passDO']  # guarda datos de declaracion de deformidades, amputaciones o defecto fisico
    if(bandera == '1'):
        tienedadf=request.POST['tiened']
        try:
            detallesdadf=request.POST['detalled']
        except :
            detallesdadf=""
        
        fumacp=request.POST['fumacp']
        try:
           cuantosd=request.POST['cuantosd']
        except :
            cuantosd=""
        
        bebidadalc=request.POST['ibebidas']
        try:
           frecuenciaalc=request.POST['frecuanciab']
        except :
            frecuenciaalc=""
       
        tratamientomd=request.POST['tratamientomd']
        try:
           detalletmd=request.POST['detalletm']
        except :
            detalletmd=""
        
        practicaad=request.POST['practicaadp']   
        try:
           clasead=request.POST['clase']
        except :
            clasead=""
        try:
          frecuenciaad=request.POST['frecuencia']
        except :
            frecuenciaad=""
        
        segurodd=request.POST['segurod']
   


    solicitudisdadf=SolicitudInscSegDefAmpDefFis.objects.get(IdSolicitudInscSeg=idsi)
    solicitudisdadf.TieneDefoAmpDefFis=tienedadf
    solicitudisdadf.DetallesDefoAmpDefFis=detallesdadf
    solicitudisdadf.FumaCigaPip=fumacp
    solicitudisdadf.CuantosDia=cuantosd
    solicitudisdadf.BebidasAlco=bebidadalc
    solicitudisdadf.FrecuenciaBebiAlc=frecuenciaalc
    solicitudisdadf.TratamientoMedi=tratamientomd
    solicitudisdadf.DetalleTratMed=detalletmd
    solicitudisdadf.PracticaActiDep=practicaad
    solicitudisdadf.ClaseActiDep=clasead
    solicitudisdadf.FrecuenciaActiDep=frecuenciaad
    solicitudisdadf.SeguroDese=segurodd
    solicitudisdadf.save()

    mensaje="Datos Actualizados"
    registroBit(request, "Se actualizo formulario Inscripcion seguro " + solicitudis.IdSolicitud.IdPerfil.Dui, "Actualizacion")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=solicitudis.IdSolicitud.IdPerfil.Id)  # id de perfil 
 


