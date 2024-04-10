import json
from django.shortcuts import render,redirect, HttpResponse
from ClienteApp.models import *
from email import message
from django.contrib import messages
from ConfiguracionApp.models import Agencia
from EvaluacionIvEFApp.models import *
from SolicitudesApp.models import *
from TesisApp.views import registroBit

# Create your views here.
def evaluacionf(request, id):
    cliente = Perfil.objects.get(Id=id)
    return render(request,"EvaluacionIvEFApp/evaluacionIvE.html", {"perfil":cliente})

def registrarEvaluacion(request): 
    # bienes 
    try:    
        numerob=request.POST.getlist('numerob')
    except :
        numerob=""    
    try:    
        descripcionbien=request.POST.getlist('descripcionbien')
    except :
        descripcionbien=""    
    try:    
        preciocop=request.POST.getlist('preciocop')
    except :
        preciocop=""    
    try:    
        cuotam=request.POST.getlist('cuotam')
    except :
        cuotam=""    

    print(numerob)

    # egresos
    idp=request.POST['idp']
    alimentaciongf=request.POST['alimentaciongf']
    educaciongf=request.POST['educaciongf']
    transporte=request.POST['transporte']
    saludiio=request.POST['saludiio']
    afpiio=request.POST['afpiio']
    servicios =request.POST['servicios']
    alquiler=request.POST['alquiler']
    planilla=request.POST['planilla']
    ventanilla=request.POST['ventanilla']
    hphes =request.POST['hphes']
    otrosdes=request.POST['otrosdes']
    recreacion=request.POST['recreacion']
    imprevistos =request.POST['imprevistos']
    totalp =request.POST['totalp']

    if(alimentaciongf=="" ):
        alimentaciongf = 0.00    
    if(educaciongf=="" ):
        educaciongf = 0.00
    if(transporte=="" ):
        transporte = 0.00
    if(saludiio=="" ):
        saludiio = 0.00
    if(afpiio=="" ):
        afpiio = 0.00
    if(servicios=="" ):
        servicios = 0.00
    if(alquiler=="" ):
        alquiler = 0.00
    if(planilla=="" ):
        planilla = 0.00
    if(ventanilla=="" ):
        ventanilla = 0.00
    if(hphes=="" ):
        hphes = 0.00
    if(otrosdes=="" ):
        otrosdes = 0.00
    if(recreacion=="" ):
        recreacion = 0.00
    if(imprevistos=="" ):
        imprevistos = 0.00
    if(totalp=="" ):
        totalp = 0.00

    # ingresos
    familiar =request.POST['familiar']
    otrosing =request.POST['otrosing']
    totald =request.POST['totald']

    if(familiar=="" ):
        familiar = 0.00

    if(otrosing=="" ):
        otrosing = 0.00

    if(totald=="" ):
        totald = 0.00

    #capacidad pago
    pendeudamientoa =request.POST['pendeudamientoa']
    disponible =request.POST['disponible']
    pdisponible =request.POST['pdisponible']
    cuota =request.POST['cuota']
    pcuota =request.POST['pcuota']
    superavit =request.POST['superavit']
    deficit =request.POST['deficit']

    if(pendeudamientoa=="" ):
        pendeudamientoa = '0.00%'   

    if(disponible=="" ):
        disponible = 0.00

    if(pdisponible==" " ):
        pdisponible = '0.00%'

    if(cuota=="" ):
        cuota = 0.00

    if(pcuota=="" ):
        pcuota = '0.00%'

    if(superavit=="" or superavit=="-"):
        superavit = 0.00

    if(deficit=="" or deficit=="-"):
        deficit = 0.00

    idperf=Perfil.objects.get(Id=idp)
    idperf.Id=idp

    egresosf=EgresosFami.objects.create(Alimentacion=alimentaciongf,Educacion=educaciongf,Transporte=transporte,Salud=saludiio,Afp=afpiio,Servicios=servicios,Alquiler=alquiler,PorcentajePlan=planilla,PorcentajeVent=ventanilla,PorcentajeHplhes=hphes,OtrosDesc=otrosdes,Recreacion=recreacion,Imprevistos=imprevistos ,Total=totalp,Estado=1,IdPerfil=idperf)
    
    #actualizo estado para administrar el perfil del cliente
    idperf.EstadoSoli=3
    idperf.save()
    
    ideg= EgresosFami.objects.all().last() #obtengo el ultimo registro

    ingresosf=IngresosFami.objects.create(Familiar=familiar,OtrosIngr=otrosing,TotalIngr=totald,IdEgresosFami=ideg)

    capacidadpagof=CapacidadPagoFam.objects.create(PorcentajeEnde=pendeudamientoa,Disponible=disponible,PorcentajeDisp=pdisponible,Cuota=cuota,PorcentajeCuot=pcuota,Superavit=superavit,Deficit=deficit,Estado="activo",IdEgresosFami=ideg)
    
    for i in range(len(numerob)):
        if (numerob[i] != ""):
            bienesh = BienesHoga.objects.create( Numero=numerob[i], DescripcionBien=descripcionbien[i], 
            PrecioComp=preciocop[i], CuotaMens=cuotam[i], IdEgresosFami=ideg)

    mensaje="Datos guardados"
    registroBit(request, "Se registro formulario de Evaluacion Ingresos vs Egresos " + idperf.Dui, "Registro")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=egresosf.IdPerfil.Id)  # id de perfil 

def listaEvaluacion(request,id):
    listae=CapacidadPagoFam.objects.filter(Estado="activo",IdEgresosFami__IdPerfil__IdAgencia=id)
    return render(request, "EvaluacionIvEFApp/listaEvaluacion.html", {"evaluaciones":listae})

def listaEvaluacionAdmin(request):
    listaAg=Agencia.objects.all()
    return render(request, "EvaluacionIvEFApp/listaEvaluacionAdmin.html", {"agencia":listaAg})

def agencEF(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listae=""
    if request.is_ajax():
        try:
            listae=CapacidadPagoFam.objects.filter(Estado="activo",IdEgresosFami__IdPerfil__IdAgencia=id)
            
            for item in listae:
                lista_agenciaC.append({"id":item.Id,"nombre":item.IdEgresosFami.IdPerfil.Nombres, "apellido":item.IdEgresosFami.IdPerfil.Apellidos, "disponible":item.Disponible, "cuota":item.Cuota,"ide":item.IdEgresosFami.Id,"idp":item.IdEgresosFami.IdPerfil.Id})

        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

def editarEvaluacion(request, id):
    ide=int(id)
    try:    
        egf=  EgresosFami.objects.get(Id=ide)
    except EgresosFami.DoesNotExist:
        egf="" 
    try: 
        cliente = Perfil.objects.get(Id=egf.IdPerfil.Id)
    except Perfil.DoesNotExist:
        cliente=""        
    try:    
        igf=  IngresosFami.objects.get(IdEgresosFami=ide)
    except IngresosFami.DoesNotExist:
        igf="" 
    try:    
        cpf=  CapacidadPagoFam.objects.get(IdEgresosFami=ide)
    except CapacidadPagoFam.DoesNotExist:
        cpf="" 
    try:
        bns=BienesHoga.objects.filter(IdEgresosFami=ide)
    except BienesHoga.DoesNotExist:
        bns=""
    return render(request,"EvaluacionIvEFApp/modificarEvaluacionIvE.html", {"perfil":cliente,"egresos":egf,"ingresos":igf,"cpago":cpf,"bienes":bns})

def modificarEvaluacion(request): 
    # egresos
    ide=request.POST['ide']
    alimentaciongf=request.POST['alimentaciongf']
    educaciongf=request.POST['educaciongf']
    transporte=request.POST['transporte']
    saludiio=request.POST['saludiio']
    afpiio=request.POST['afpiio']
    servicios =request.POST['servicios']
    alquiler=request.POST['alquiler']
    planilla=request.POST['planilla']
    ventanilla=request.POST['ventanilla']
    hphes =request.POST['hphes']
    otrosdes=request.POST['otrosdes']
    recreacion=request.POST['recreacion']
    imprevistos =request.POST['imprevistos']
    totalp =request.POST['totalp']

    if(alimentaciongf==" " ):
        alimentaciongf = 0.00    
    if(educaciongf==" " ):
        educaciongf = 0.00
    if(transporte==" " ):
        transporte = 0.00
    if(saludiio==" " ):
        saludiio = 0.00
    if(afpiio==" " ):
        afpiio = 0.00
    if(servicios==" " ):
        servicios = 0.00
    if(alquiler==" " ):
        alquiler = 0.00
    if(planilla==" " ):
        planilla = 0.00
    if(ventanilla==" " ):
        ventanilla = 0.00
    if(hphes==" " ):
        hphes = 0.00
    if(otrosdes==" " ):
        otrosdes = 0.00
    if(recreacion==" " ):
        recreacion = 0.00
    if(imprevistos==" " ):
        imprevistos = 0.00
    if(totalp==" " ):
        totalp = 0.00

    # ingresos
    familiar =request.POST['familiar']
    otrosing =request.POST['otrosing']
    totald =request.POST['totald']

    if(familiar==" " ):
        familiar = 0.00

    if(otrosing==" " ):
        otrosing = 0.00

    if(totald==" " ):
        totald = 0.00

    #capacidad pago
    pendeudamientoa =request.POST['pendeudamientoa']
    disponible =request.POST['disponible']
    pdisponible =request.POST['pdisponible']
    cuota =request.POST['cuota']
    pcuota =request.POST['pcuota']
    superavit =request.POST['superavit']
    deficit =request.POST['deficit']

    if(pendeudamientoa==" " ):
        pendeudamientoa = '0.00%'   

    if(disponible==" " ):
        disponible = 0.00

    if(pdisponible==" " ):
        pdisponible = '0.00%'

    if(cuota==" " ):
        cuota = 0.00

    if(pcuota==" " ):
        pcuota = '0.00%'

    if(superavit==" " or superavit=="-"):
        superavit = 0.00

    if(deficit==" " or deficit=="-"):
        deficit = 0.00
    
    #modificar egresos
    megf=EgresosFami.objects.get(Id=ide)
    megf.Alimentacion=alimentaciongf
    megf.Educacion=educaciongf
    megf.Transporte=transporte
    megf.Salud=saludiio
    megf.Afp=afpiio
    megf.Servicios=servicios
    megf.Alquiler=alquiler
    megf.PorcentajePlan=planilla
    megf.PorcentajeVent=ventanilla
    megf.PorcentajeHplhes=hphes
    megf.OtrosDesc=otrosdes
    megf.Recreacion=recreacion
    megf.Imprevistos=imprevistos 
    megf.Total=totalp
    megf.save()

    #modificar ingresos
    migf=IngresosFami.objects.get(IdEgresosFami=ide)
    migf.Familiar=familiar
    migf.OtrosIngr=otrosing
    migf.TotalIngr=totald
    migf.save()

    #modificar capacidad de pago
    mcpf=CapacidadPagoFam.objects.get(IdEgresosFami=ide)
    mcpf.PorcentajeEnde=pendeudamientoa
    mcpf.Disponible=disponible
    mcpf.PorcentajeDisp=pdisponible
    mcpf.Cuota=cuota
    mcpf.PorcentajeCuot=pcuota
    mcpf.Superavit=superavit
    mcpf.Deficit=deficit
    mcpf.save()

    #modificar bienes
    ide = EgresosFami.objects.get(Id=ide)
    idb=request.POST.getlist('idbns')
    nb=request.POST.getlist('numerob')
    descb =request.POST.getlist('descripcionbien') 
    preb =request.POST.getlist('preciocop')
    cuotab =request.POST.getlist('cuotam') 
    print(len(nb))

    for i in range(len(nb)):
        print('paso')
        if (descb[i] != ""):
            if(idb[i]==""):#si registro un nuevo bien ejecuta la orden sin enviar id de la tabla ya que no existe ese campo
                bns = BienesHoga.objects.update_or_create(IdEgresosFami=ide,Numero=nb[i],DescripcionBien=descb[i],PrecioComp=preb[i],
                defaults={'Numero':nb[i],
                'DescripcionBien':descb[i],
                'PrecioComp':preb[i],
                'CuotaMens':cuotab[i],
                'IdEgresosFami':ide
                })            
            else: 
                bns = BienesHoga.objects.update_or_create(IdEgresosFami=ide,Id=idb[i],
                defaults={'Numero':nb[i],
                'DescripcionBien':descb[i],
                'PrecioComp':preb[i],
                'CuotaMens':cuotab[i],
                'IdEgresosFami':ide
                })


    mensaje="Datos Actualizados"
    registroBit(request, "Se actualizó formulario de evaluacion de Ingreso vs Egresos " + ide.IdPerfil.Dui, "Actualización")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=megf.IdPerfil.Id)  # id de perfil 

def darBajaF(request, id, idp): # id capacidad de pago, id de perfil
    estad="inactivo" 
    d=Solicitud.objects.filter(IdPerfil=idp,EstadoSoli=3).exists()
    cap= CapacidadPagoFam.objects.get(Id=id)
    egr= EgresosFami.objects.get(Id=cap.IdEgresosFami.Id)
    if d == True :
        mensaje="La Evaluación No puede darse de baja"
        messages.warning(request, mensaje)
    elif cap.Estado=="activo" and egr.Estado==1:          
        cap.Estado =estad
        cap.save()
        egr.Estado=0
        egr.save()

        mensaje="La Evaluación fue dada de baja "
        registroBit(request, mensaje + egr.IdPerfil.Dui, "Desactivacion")
        messages.success(request, mensaje)
    return redirect('/EvaluacionIvEFApp/listaEvaluacion')
