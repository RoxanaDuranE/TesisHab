import json
from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from ClienteApp.models import *
from ConfiguracionApp.models import Agencia
from EvaluacionMicroApp.models import *
from SolicitudesApp.models import *
from TesisApp.views import registroBit

# Create your views here.
def evaluacionm(request, id):
    cliente = Perfil.objects.get(Id=id)
    return render(request,"EvaluacionMicroApp/evaluacionM.html", {"perfil":cliente})

def registrarEvaluacionm(request): 
    
    idp=request.POST['idp']
    tiponegocio=request.POST['tiponeg']

    # activo
    tcirculantea=request.POST['circulantea']
    caja=request.POST['caja']
    bancos=request.POST['banco']
    cuentaspc=request.POST['cuentaspc']
    inventarios=request.POST['inventario']
    tfijoa=request.POST['fijoa']
    mobiliario=request.POST['mobiliario']
    terrenos=request.POST['terreno']
    vehiculos=request.POST['vehiculo']
    totalactivo=request.POST['totalact']

    if(tcirculantea=="" ):
        tcirculantea = 0.00
    if(caja=="" ):
        caja = 0.00
    if(bancos=="" ):
        bancos = 0.00
    if(cuentaspc=="" ):
        cuentaspc = 0.00
    if(inventarios=="" ):
        inventarios = 0.00
    if(tfijoa=="" ):
        tfijoa = 0.00
    if(mobiliario=="" ):
        mobiliario = 0.00
    if(terrenos=="" ):
        terrenos = 0.00
    if(vehiculos=="" ):
        vehiculos = 0.00
    if(totalactivo=="" ):
        totalactivo = 0.00
    
    # pasivo
    tcirculantep=request.POST['circulantep']
    proveedores=request.POST['proveedor']
    cuentaspp=request.POST['cuantaspp']
    prestamoscp=request.POST['prestamocp']
    fijop=request.POST['fijop']
    prestamoslp=request.POST['prestamolp']
    totalpasivo=request.POST['totalpasivo']
    patrimonio=request.POST['patrimonio']
    capital=request.POST['capital']
    pasivompatrim=request.POST['pasivopat']

    if(tcirculantep==""):
        tcirculantep = 0.00    
    if(proveedores==""):
        proveedores = 0.00
    if(cuentaspp==""):
        cuentaspp = 0.00
    if(prestamoscp==""):
        prestamoscp = 0.00
    if(fijop=="" ):
        fijop = 0.00
    if(prestamoslp==""):
        prestamoslp = 0.00
    if(totalpasivo=="" ):
        totalpasivo = 0.00
    if(patrimonio=="" ):
        patrimonio = 0.00
    if(capital=="" ):
        capital = 0.00
    if(pasivompatrim=="" ):
        pasivompatrim = 0.00

    # estado de resultado
    ventast=request.POST['ventastp']
    costovent=request.POST['costovt']
    utilidadbt=request.POST['utilidadb']
    gastosgral=request.POST['gastosg']
    transporteer=request.POST['transporteer']
    servicioser=request.POST['servicioser']
    impuestos=request.POST['impuestos']
    alquilerer=request.POST['alquilerer']
    cuotaprest=request.POST['cuotaprest']
    imprevistoser=request.POST['imprevistoser']
    utilidadneta=request.POST['utilidadn']
    mensual=request.POST['mensual']

    if(ventast==""):
        ventast = 0.00    
    if(costovent==""):
        costovent = 0.00
    if(utilidadbt==""):
        utilidadbt = 0.00
    if(gastosgral==""):
        gastosgral = 0.00
    if(transporteer=="" ):
        transporteer = 0.00
    if(servicioser==""):
        servicioser = 0.00
    if(impuestos=="" ):
        impuestos = 0.00
    if(alquilerer=="" ):
        alquilerer = 0.00
    if(cuotaprest=="" ):
        cuotaprest = 0.00
    if(imprevistoser=="" ):
        imprevistoser = 0.00
    if(utilidadneta=="" ):
        utilidadneta = 0.00
    if(mensual=="" ):
        mensual = 0.00

    # egresos
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
   
    if(alimentaciongf==""):
        alimentaciongf = 0.00    
    if(educaciongf==""):
        educaciongf = 0.00
    if(transporte==""):
        transporte = 0.00
    if(saludiio==""):
        saludiio = 0.00
    if(afpiio=="" ):
        afpiio = 0.00
    if(servicios==""):
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
    negocio =request.POST['negocio']
    remesas =request.POST['remesas']
    totald =request.POST['totald']

    if(negocio =="" ):
        negocio = 0.00

    if(remesas =="" ):
        remesas = 0.00

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

    if(pdisponible=="" ):
        pdisponible = '0.00%'

    if(cuota=="" ):
        cuota = 0.00

    if(pcuota=="" ):
        pcuota = '0.00%'

    if(superavit=="" or superavit=="-"):
        superavit = 0.00

    if(deficit=="" or deficit=="-"):
        deficit = 0.00

    idperm=Perfil.objects.get(Id=idp)
    idperm.Id=idp

    balancesm=BalanceSituMic.objects.create(TipoNego=tiponegocio,IdPerfil=idperm,Estado=1)
    # cambia estado de perfil a 2 que es para solicitud micro
    idperm.EstadoSoli=2
    idperm.save()

    idbs= BalanceSituMic.objects.all().last() #obtengo el ultimo registro

    activobsm=ActivoBalaSit.objects.create(TotalCircAct=tcirculantea,Caja=caja,Bancos=bancos,CuentasPorCob=cuentaspc,Inventarios=inventarios,TotalFijoAct=tfijoa,Mobiliario=mobiliario,Terrenos=terrenos,Vehiculos=vehiculos,TotalActi=totalactivo,IdBalanceSituMic=idbs)

    pasivobsm=PasivoBalaSit.objects.create(TotalCircPas=tcirculantep,Proveedores=proveedores,CuentasPorPag=cuentaspp,PrestamosCortPla=prestamoscp,FijoPasi=fijop,PrestamosLargPla=prestamoslp,TotalPasi=totalpasivo,Patrimonio=patrimonio,Capital=capital,PasivoMasPat=pasivompatrim ,IdBalanceSituMic=idbs)


    estadorm=EstadoResuMic.objects.create(VentasTota=ventast,CostoVent=costovent,UtilidadBrut=utilidadbt,GastosGral=gastosgral,Transporte=transporteer,Servicios=servicioser,Impuestos=impuestos,Alquiler=alquilerer,CuotaPres=cuotaprest,ImprevistosEstaRes=imprevistoser,UtilidadNeta=utilidadneta,Mensual=mensual,IdBalanceSituMic=idbs)


    egresosm=EgresoFlujMic.objects.create(Alimentacion=alimentaciongf,Educacion=educaciongf,Transporte=transporte,Salud=saludiio,Afp=afpiio,Servicios=servicios,Alquiler=alquiler,PorcentajePlan=planilla,PorcentajeVent=ventanilla,PorcentajeHplhes=hphes,OtrosDesc=otrosdes,Recreacion=recreacion,Imprevistos=imprevistos ,Total=totalp,IdBalanceSituMic=idbs)
    idem= EgresoFlujMic.objects.all().last() #obtengo el ultimo registro

    ingresosm=IngresoFlujMic.objects.create(Negocio=negocio,Remesas=remesas,TotalIngrMic=totald,IdEgresoFlujMic=idem)

    capacidadpagom=CapacidadPagoMic.objects.create(PorcentajeEnde=pendeudamientoa,Disponible=disponible,PorcentajeDisp=pdisponible,Cuota=cuota,PorcentajeCuot=pcuota,Superavit=superavit,Deficit=deficit,Estado="activo",IdEgresoFlujMic=idem)
    
    mensaje="Datos guardados"
    registroBit(request, "Se registro formulario evaluacion Microempresa de Ingreso vs Egresos " + balancesm.IdPerfil.Dui, "Registro")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=balancesm.IdPerfil.Id)  # id de perfil 

def listaEvaluacionm(request,id):
    listaem=CapacidadPagoMic.objects.filter(Estado="activo",IdEgresoFlujMic__IdBalanceSituMic__IdPerfil__IdAgencia=id)
    return render(request, "EvaluacionMicroApp/listaEvaluacionM.html", {"evaluacionesm":listaem})

def listaEvaluacionmAdmin(request):
    listaAg=Agencia.objects.all()
    return render(request, "EvaluacionMicroApp/listaEvaluacionMAdmin.html", {"agencia":listaAg})

def agencEM(request):
    id=request.GET['id']
    lista_agenciaC=[]
    listaem=""
    if request.is_ajax():
        try:
            listaem=CapacidadPagoMic.objects.filter(Estado="activo",IdEgresoFlujMic__IdBalanceSituMic__IdPerfil__IdAgencia=id)
            
            for item in listaem:
                lista_agenciaC.append({"id":item.Id,"nombre":item.IdEgresoFlujMic.IdBalanceSituMic.IdPerfil.Nombres, "apellido":item.IdEgresoFlujMic.IdBalanceSituMic.IdPerfil.Apellidos, "disponible":item.Disponible, "cuota":item.Cuota,"ide":item.IdEgresoFlujMic.Id,"idp":item.IdEgresoFlujMic.IdBalanceSituMic.IdPerfil.Id})

        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    
def editarEvaluacionm(request, id): # ide de egresos 
    ide=int(id)
    try:    
        egm=  EgresoFlujMic.objects.get(Id=ide)
    except EgresoFlujMic.DoesNotExist:
        egm="" 
    try:    
        blm=  BalanceSituMic.objects.get(Id=egm.IdBalanceSituMic.Id)
    except BalanceSituMic.DoesNotExist:
        blm="" 

    try:    
        atm=  ActivoBalaSit.objects.get(IdBalanceSituMic=egm.IdBalanceSituMic.Id)
    except ActivoBalaSit.DoesNotExist:
        atm=""
    try:    
        psm=  PasivoBalaSit.objects.get(IdBalanceSituMic=egm.IdBalanceSituMic.Id)
    except PasivoBalaSit.DoesNotExist:
        psm=""
    try:    
        etm=  EstadoResuMic.objects.get(IdBalanceSituMic=egm.IdBalanceSituMic.Id)
    except EstadoResuMic.DoesNotExist:
        etm="" 

    try: 
        cliente = Perfil.objects.get(Id=egm.IdBalanceSituMic.IdPerfil.Id)
    except Perfil.DoesNotExist:
        cliente=""        
    try:    
        igm=  IngresoFlujMic.objects.get(IdEgresoFlujMic=ide)
    except IngresoFlujMic.DoesNotExist:
        igm="" 
    try:    
        cpm=  CapacidadPagoMic.objects.get(IdEgresoFlujMic=ide)
    except CapacidadPagoMic.DoesNotExist:
        cpm="" 

    return render(request,"EvaluacionMicroApp/modificarEvaluacionM.html", {"perfil":cliente,"balance":blm,"activo":atm,"pasivo":psm,"estado":etm,"egresos":egm,"ingresos":igm,"cpago":cpm})

def modificarEvaluacionm(request): 
    
    idb=request.POST['idb']
    tiponegocio=request.POST['tiponeg']

    # activo
    tcirculantea=request.POST['circulantea']
    caja=request.POST['caja']
    bancos=request.POST['banco']
    cuentaspc=request.POST['cuentaspc']
    inventarios=request.POST['inventario']
    tfijoa=request.POST['fijoa']
    mobiliario=request.POST['mobiliario']
    terrenos=request.POST['terreno']
    vehiculos=request.POST['vehiculo']
    totalactivo=request.POST['totalact']

    if(tcirculantea=="" ):
        tcirculantea = 0.00
    if(caja=="" ):
        caja = 0.00
    if(bancos=="" ):
        bancos = 0.00
    if(cuentaspc=="" ):
        cuentaspc = 0.00
    if(inventarios=="" ):
        inventarios = 0.00
    if(tfijoa=="" ):
        tfijoa = 0.00
    if(mobiliario=="" ):
        mobiliario = 0.00
    if(terrenos=="" ):
        terrenos = 0.00
    if(vehiculos=="" ):
        vehiculos = 0.00
    if(totalactivo=="" ):
        totalactivo = 0.00
    
    # pasivo
    tcirculantep=request.POST['circulantep']
    proveedores=request.POST['proveedor']
    cuentaspp=request.POST['cuantaspp']
    prestamoscp=request.POST['prestamocp']
    fijop=request.POST['fijop']
    prestamoslp=request.POST['prestamolp']
    totalpasivo=request.POST['totalpasivo']
    patrimonio=request.POST['patrimonio']
    capital=request.POST['capital']
    pasivompatrim=request.POST['pasivopat']

    if(tcirculantep==""):
        tcirculantep = 0.00    
    if(proveedores==""):
        proveedores = 0.00
    if(cuentaspp==""):
        cuentaspp = 0.00
    if(prestamoscp==""):
        prestamoscp = 0.00
    if(fijop=="" ):
        fijop = 0.00
    if(prestamoslp==""):
        prestamoslp = 0.00
    if(totalpasivo=="" ):
        totalpasivo = 0.00
    if(patrimonio=="" ):
        patrimonio = 0.00
    if(capital=="" ):
        capital = 0.00
    if(pasivompatrim=="" ):
        pasivompatrim = 0.00

    # estado de resultado
    ventast=request.POST['ventastp']
    costovent=request.POST['costovt']
    utilidadbt=request.POST['utilidadb']
    gastosgral=request.POST['gastosg']
    transporteer=request.POST['transporteer']
    servicioser=request.POST['servicioser']
    impuestos=request.POST['impuestos']
    alquilerer=request.POST['alquilerer']
    cuotaprest=request.POST['cuotaprest']
    imprevistoser=request.POST['imprevistoser']
    utilidadneta=request.POST['utilidadn']
    mensual=request.POST['mensual']

    if(ventast==""):
        ventast = 0.00    
    if(costovent==""):
        costovent = 0.00
    if(utilidadbt==""):
        utilidadbt = 0.00
    if(gastosgral==""):
        gastosgral = 0.00
    if(transporteer=="" ):
        transporteer = 0.00
    if(servicioser==""):
        servicioser = 0.00
    if(impuestos=="" ):
        impuestos = 0.00
    if(alquilerer=="" ):
        alquilerer = 0.00
    if(cuotaprest=="" ):
        cuotaprest = 0.00
    if(imprevistoser=="" ):
        imprevistoser = 0.00
    if(utilidadneta=="" ):
        utilidadneta = 0.00
    if(mensual=="" ):
        mensual = 0.00

    # egresos
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
   
    if(alimentaciongf==""):
        alimentaciongf = 0.00    
    if(educaciongf==""):
        educaciongf = 0.00
    if(transporte==""):
        transporte = 0.00
    if(saludiio==""):
        saludiio = 0.00
    if(afpiio=="" ):
        afpiio = 0.00
    if(servicios==""):
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
    negocio =request.POST['negocio']
    remesas =request.POST['remesas']
    totald =request.POST['totald']

    if(negocio =="" ):
        negocio = 0.00

    if(remesas =="" ):
        remesas = 0.00

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

    if(pdisponible=="" ):
        pdisponible = '0.00%'

    if(cuota=="" ):
        cuota = 0.00

    if(pcuota=="" ):
        pcuota = '0.00%'

    if(superavit=="" or superavit=="-"):
        superavit = 0.00

    if(deficit=="" or deficit=="-"):
        deficit = 0.00

    # modificar balance micro
    mbm=BalanceSituMic.objects.get(Id=idb)
    mbm.TipoNego=tiponegocio
    mbm.save()

    # modificar activos micro
    mam=ActivoBalaSit.objects.get(IdBalanceSituMic=idb)
    mam.TotalCircAct=tcirculantea
    mam.Caja=caja
    mam.Bancos=bancos
    mam.CuentasPorCob=cuentaspc
    mam.Inventarios=inventarios
    mam.TotalFijoAct=tfijoa
    mam.Mobiliario=mobiliario
    mam.Terrenos=terrenos
    mam.Vehiculos=vehiculos
    mam.TotalActi=totalactivo
    mam.save()

    # modificar pasivos micro
    mpm=PasivoBalaSit.objects.get(IdBalanceSituMic=idb)
    mpm.TotalCircPas=tcirculantep
    mpm.Proveedores=proveedores
    mpm.CuentasPorPag=cuentaspp
    mpm.PrestamosCortPla=prestamoscp
    mpm.FijoPasi=fijop
    mpm.PrestamosLargPla=prestamoslp
    mpm.TotalPasi=totalpasivo
    mpm.Patrimonio=patrimonio
    mpm.Capital=capital
    mpm.PasivoMasPat=pasivompatrim 
    mpm.save()
    

    # modificar estado de resultados micro
    merm=EstadoResuMic.objects.get(IdBalanceSituMic=idb)
    merm.VentasTota=ventast
    merm.CostoVent=costovent
    merm.UtilidadBrut=utilidadbt
    merm.GastosGral=gastosgral
    merm.Transporte=transporteer
    merm.Servicios=servicioser
    merm.Impuestos=impuestos
    merm.Alquiler=alquilerer
    merm.CuotaPres=cuotaprest
    merm.ImprevistosEstaRes=imprevistoser
    merm.UtilidadNeta=utilidadneta
    merm.Mensual=mensual
    merm.save()
    

    # modificar egresos micro
    megm=EgresoFlujMic.objects.get(IdBalanceSituMic=idb)
    megm.Alimentacion=alimentaciongf
    megm.Educacion=educaciongf
    megm.Transporte=transporte
    megm.Salud=saludiio
    megm.Afp=afpiio
    megm.Servicios=servicios
    megm.Alquiler=alquiler
    megm.PorcentajePlan=planilla
    megm.PorcentajeVent=ventanilla
    megm.PorcentajeHplhes=hphes
    megm.OtrosDesc=otrosdes
    megm.Recreacion=recreacion
    megm.Imprevistos=imprevistos 
    megm.Total=totalp
    megm.save()


    # modificar ingresos micro
    migm=IngresoFlujMic.objects.get(IdEgresoFlujMic=megm.Id)
    migm.Negocio=negocio
    migm.Remesas=remesas
    migm.TotalIngrMic=totald
    migm.save()

    # modificar capacidad de pago micro
    mcpgm=CapacidadPagoMic.objects.get(IdEgresoFlujMic=megm.Id)
    mcpgm.PorcentajeEnde=pendeudamientoa
    mcpgm.Disponible=disponible
    mcpgm.PorcentajeDisp=pdisponible
    mcpgm.Cuota=cuota
    mcpgm.PorcentajeCuot=pcuota
    mcpgm.Superavit=superavit
    mcpgm.Deficit=deficit
    mcpgm.save()
    
    mensaje="Datos actualizados"
    registroBit(request, "Se actualizó formulario de evaluacion Microempresa Ingreso vs Egresos " + mbm.IdPerfil.Dui, "Actualización")
    messages.success(request, mensaje)

    return redirect('administrarPerfil', id=mbm.IdPerfil.Id)  # id de perfil 

def darBajaM(request, id, idp): # id capacidad de pago, id de perfil
    estad="inactivo" 
    d=Solicitud.objects.filter(IdPerfil=idp,EstadoSoli=3).exists()
    cap= CapacidadPagoMic.objects.get(Id=id)
    egrm= EgresoFlujMic.objects.get(Id=cap.IdEgresoFlujMic.Id)
    bal= BalanceSituMic.objects.get(Id=egrm.IdBalanceSituMic.Id)
    print(bal)
    if d == True :
        mensaje="La Evaluación No puede darse de baja"
        messages.warning(request, mensaje)
    elif cap.Estado=="activo" and bal.Estado == 1:          
        cap.Estado =estad
        cap.save()
        bal.Estado = 0
        bal.save()
        mensaje="La Evaluación fue dada de baja"
        registroBit(request, "Se dio de baja formulario de Ingreso vs Egresos " + bal.IdPerfil.Dui, "Desactivacion")
        messages.success(request, mensaje)
    return redirect('/EvaluacionMicroApp/listaEvaluacionm')
