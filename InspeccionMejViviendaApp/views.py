import json
from django.shortcuts import render, redirect
from django.contrib import messages
from ConfiguracionApp.models import *
from InspeccionMejViviendaApp.models import *
from ListaChequeoApp.models import ListaCheq
from django.http import JsonResponse
from TesisApp.views import registroBit

# Create your views here.


def inspeccion(request, id ): 
    sol= InspeccionMejo.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= InspeccionMejo.objects.get(IdSolicitud=id)
    
        return redirect('editarIM', id=solv.Id)   
    else:
        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
         
        try:
            listaii=Infraestructura.objects.filter(Tipo=2,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listaii=""

        try:
            listaee=Infraestructura.objects.filter(Tipo=3,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listaee=""
        
        try:
            listava=Infraestructura.objects.filter(Tipo=4,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listava=""

        try:
            listasb=Infraestructura.objects.filter(Tipo=5,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listasb=""
        
        try:
            listaif=Infraestructura.objects.filter(Tipo=6,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listaif=""
        
        try:
            listar=Infraestructura.objects.filter(Tipo=7,TipoLoteMej="Mejora",Estado="activo")
        except Infraestructura.DoesNotExist:
            listar=""

        try:
            do= DatosObra.objects.get(IdSolicitud=id)
        except DatosObra.DoesNotExist:
            do=""

        return render(request, "InspeccionMejViviendaApp/inspeccion.html", {"s":s,"listaii":listaii,"listaee":listaee,"listava":listava,"listasb":listasb,"listaif":listaif,"listar":listar,"do":do}) 

  
  
def registrarDIM(request): 
    
    if request.is_ajax and request.method == "POST":
            dtig =json.loads(request.POST.get('valoresifm'))
            print(dtig)
            for objif in dtig:
                ids=objif['ids']
                fecha=objif['fecham']
                hora=objif['horam']
                telp=objif['telpm']
                tels=objif['telsm']
                terceraed=objif['terceraedm']
                adultos=objif['adultosm']
                ninos=objif['ninosm']
                personadis=objif['personadism']
                propietarioinm=objif['propietarioinmm']
                parentescosm=objif['parentescosm']
                latitud=objif['latitudm']
                longitud=objif['longitudm']
                inmueble=objif['inmueblem']
                usoact=objif['usoactm']
                exotrav=objif['exotravm']
                usoacotv=objif['usoacotvm']
                comentariosrl=objif['comentariosrl']
                             
                print(ids)
                print(fecha)

                idsol= Solicitud.objects.get(Id=ids)
                idsol.Id=ids

                inspeccionM=InspeccionMejo.objects.create(Fecha=fecha,Hora=hora,TelefonoPrim=telp,TelefonoSegu=tels,TerceraEdad=terceraed,Adultos=adultos,Ninos=ninos,PersonaDisc=personadis,PropietarioInmu=propietarioinm,ParentescoSoli=parentescosm,Latitud=latitud,Longitud=longitud,Inmueble=inmueble,UsoActu=usoact,ExisteOtrViv=exotrav,UsoActuOtrViv=usoacotv,ComentariosRelv=comentariosrl,IdSolicitud=idsol)             
                registroBit(request, "Se registro formulario Inspeccion de Mejora " + idsol.IdPerfil.Dui, "Registro")
            
   
            idipm= InspeccionMejo.objects.all().last() #obtengo la ultima solicitud registrada 
    # fin

      #inicia Infraestructura de Imnueble
    
            data =json.loads( request.POST.get('valoresidi'))
            print(data)
            for obj in data:
                idc=obj['id']
                valor=obj['existeii']
                estado=obj['estadoii']
                tipo=obj['tiposist']
                idif= Infraestructura.objects.get(Id=idc)
                idif.Id=idc
                
                print(idc)
                print(valor)
                print(estado)
                print(tipo)
                
                infraestructuraInmuebleipm = InfraestructuraInmuInsMej.objects.create(IdInfraestructura=idif,Existe=valor,Estado=estado,TipoSist=tipo, IdInspeccionMejo=idipm)

    # fin

   #inicia espacios encontrados
    
            dataee =json.loads(request.POST.get('valoresee'))
            print(dataee)
            for obj in dataee:
                idce=obj['ide']
                valore=obj['valore']
                idife= Infraestructura.objects.get(Id=idce)
                idife.Id=idce
                
                print(idce)
                print(valore)

                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.create(IdInfraestructura=idife,Existe=valore, IdInspeccionMejo=idipm)        
    # fin
    

      #inicia servicios basicos
    
            datasb =json.loads(request.POST.get('valoressbm'))
            print(datasb)
            for obj in datasb:
                idcs=obj['ids']
                valors=obj['valors']
                idifs= Infraestructura.objects.get(Id=idcs)
                idifs.Id=idcs
                
                print(idce)
                print(valore)

                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.create(IdInfraestructura=idifs,Existe=valors, IdInspeccionMejo=idipm)        
    # fin

        #inicia infraestructura
    
            dataim =json.loads(request.POST.get('valoresim'))
            print(dataim)
            for obj in dataim:
                idci=obj['idi']
                valori=obj['valori']
                idifim= Infraestructura.objects.get(Id=idci)
                idifim.Id=idci
                
                print(idce)
                print(valore)

                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.create(IdInfraestructura=idifim,Existe=valori, IdInspeccionMejo=idipm)        
    # fin

      #inicia vias de acceso
            dtv =json.loads(request.POST.get('valoresvm'))
            print(dtv)
            for obj in dtv:
                tipovia=obj['tipovia']
                print(tipovia)

            viasAccesoipm =  ViasAcceInsMej.objects.create(TipoVias=tipovia, IdInspeccionMejo=idipm)  

    # fin

      #inicia riesgos
    
            datar =json.loads(request.POST.get('valorestbrm'))
            print(datar)
            for obj in datar:
                idcr=obj['idr']
                valorr=obj['valorr']
                idir= Infraestructura.objects.get(Id=idcr)
                idir.Id=idcr
                
                print(idcr)
                print(valorr)

                inspeccionesirmr = InspeccionMejoEspSerInfRie.objects.create(IdInfraestructura=idir,Existe=valorr, IdInspeccionMejo=idipm)        
    # fin

    #inicia distancia riesgos
            dtdr =json.loads(request.POST.get('valorestbdrm'))
            print(dtdr)
            for objif in dtdr:
                distanciatl=objif['distanciatlm']
                distanciarc=objif['distanciarcm']
                distancialc=objif['distancialcm']
                distanciata=objif['distanciatam']

            riesgosipm = RiesgosInsMej.objects.create(DistanciaTalu=distanciatl,DistanciaRiosCer=distanciarc,DistanciaLadeCer=distancialc,DistanciaTorrCer=distanciata, IdInspeccionMejo=idipm)  

    # 

    #inicia etapas del plan de mejoramiento
    
            dataet =json.loads(request.POST.get('valorestbetp'))
            print(dataet)
            for obj in dataet:
                valet=obj['valETP']
                etapa=obj['etapa']
               
                
                print(valet)
                print(etapa)

                planMejoramientoipm = PlanMejoInsMej.objects.create(Etapas=valet,Descripcion=etapa, IdInspeccionMejo=idipm)        
    # fin

     #inicia factibilidades tecnicas mejora
            dttfm =json.loads(request.POST.get('valoresftm'))
            print(dttfm)
            for obj in dttfm:
                factpm=obj['factpm']
                print(factpm)

            factibilidadipm = FactibilidadInsMej.objects.create(Detalle=factpm, IdInspeccionMejo=idipm)  

    #  

    #inicia descripción del mejoramiento acordado 
            dtdm =json.loads(request.POST.get('valoresdm'))
            print(dtdm)
            for obj in dtdm:
                descripcionma=obj['descripcionma']
                diasestm=obj['diasestm']
                print(descripcionma)

            dMejoramientoipm = DescripcionMejoInsMej.objects.create(Descripcion=descripcionma,DiasEsti=diasestm, IdInspeccionMejo=idipm)  

    #

    #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.get(IdSolicitud=idsol)
    lchequo.InspeccionTecn ="Si"
    lchequo.save()

    response_data = {'status': 'success', 'message': 'Archivos recibidos y procesados correctamente.'}
    return JsonResponse(response_data)


    #mensaje="Datos guardados"
    #messages.success(request, mensaje)
    #return redirect('administrarPerfil', id=inspeccionM.ids.perfil.id)  # id de perfil 


def registrarDIME(request): 
    
        if 'esquemaubicacions' in request.FILES:
            esquemaubicacions = request.FILES['esquemaubicacions']
        else:
            esquemaubicacions = None 

        if 'esquemaubicacionm' in request.FILES:
            esquemaubicacionm = request.FILES['esquemaubicacionm']
        else:
            esquemaubicacionm = None 

        idipm= InspeccionMejo.objects.all().last() #obtengo la ultima solicitud registrada 
        esquemasipm = EsquemasInspMej.objects.create(EsquemaSiti=esquemaubicacions,EsquemaMejo=esquemaubicacionm, IdInspeccionMejo=idipm)  
            
        response_data = {'status': 'success', 'message': 'Archivos recibidos y procesados correctamente.'}
        return JsonResponse(response_data)


    #mensaje="Datos guardados"
    #messages.success(request, mensaje)
    #return redirect('administrarPerfil', id=inspeccionM.ids.perfil.id)  # id de perfil 

def listaIM(request,id): 
    listaIm=FactibilidadInsMej.objects.filter(IdInspeccionMejo__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "InspeccionMejViviendaApp/listaim.html", {"listaim":listaIm})


def editarIM(request, id): # id de inspeccion mejora
    try:
        ipm=  InspeccionMejo.objects.get(Id=id)
    except InspeccionMejo.DoesNotExist:
        ipm=""
    try:
        s=  Solicitud.objects.get(Id=ipm.IdSolicitud.Id)
    except Solicitud.DoesNotExist:
        s=""
    
    try:
        do= DatosObra.objects.get(IdSolicitud=ipm.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
    
    try:
        vias_acceso= ViasAcceInsMej.objects.get(IdInspeccionMejo=ipm)
    except ViasAcceInsMej.DoesNotExist:
        vias_acceso=""

    try:
        riesgo_distancia= RiesgosInsMej.objects.get(IdInspeccionMejo=ipm)
    except RiesgosInsMej.DoesNotExist:
        riesgo_distancia=""

    try:
        factibilida_tecnica= FactibilidadInsMej.objects.get(IdInspeccionMejo=ipm)
    except FactibilidadInsMej.DoesNotExist:
        factibilida_tecnica=""

    try:
        descripcion_mejora= DescripcionMejoInsMej.objects.get(IdInspeccionMejo=ipm)
    except DescripcionMejoInsMej.DoesNotExist:
        descripcion_mejora=""

    try:
        lista_plan=PlanMejoInsMej.objects.filter(IdInspeccionMejo=ipm)
    except PlanMejoInsMej.DoesNotExist:
        lista_plan=""

    try:
        listaii=Infraestructura.objects.filter(Tipo=2,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listaii=""

    try:
        listaee=Infraestructura.objects.filter(Tipo=3,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listaee=""
    
    try:
        listava=Infraestructura.objects.filter(Tipo=4,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listava=""

    try:
        listasb=Infraestructura.objects.filter(Tipo=5,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listasb=""
    
    try:
        listaif=Infraestructura.objects.filter(Tipo=6,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listaif=""
    
    try:
        listar=Infraestructura.objects.filter(Tipo=7,TipoLoteMej="Mejora",Estado="activo")
    except Infraestructura.DoesNotExist:
        listar=""

    liip = InfraestructuraInmuInsMej.objects.filter(IdInspeccionMejo=ipm.Id)
    liip_data = [
        {
            'existe': item.Existe,
            'estado': item.Estado,
            'tiposistema': item.TipoSist,
            'id': item.Id,
            'idif':item.IdInfraestructura.Id,
        }
        for item in liip
        ]

    liip_json = json.dumps(liip_data)

    lista_general=InspeccionMejoEspSerInfRie.objects.filter(IdInspeccionMejo=ipm.Id)

    lista_espacios_encontrados_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "3":
            lista_espacios_encontrados_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.Id,})
    lista_espacios_encontrados_json = json.dumps(lista_espacios_encontrados_datos)

    lista_servicios_basicos_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "5":
            lista_servicios_basicos_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.Id,})
    lista_servicios_basicos_json = json.dumps(lista_servicios_basicos_datos)

    lista_infraetructura_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "6":
            lista_infraetructura_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.Id,})
    lista_infraetructura_json = json.dumps(lista_infraetructura_datos)

    lista_riesgos_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "7":
            lista_riesgos_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.Id,})
    lista_riesgos_json = json.dumps(lista_riesgos_datos)
    
    return render(request, "InspeccionMejViviendaApp/editarInspeccion.html", {"ipm":ipm,"s":s,"do":do,
        "listaii":listaii,"listaee":listaee,"listava":listava,"listasb":listasb,"listaif":listaif,
        "listar":listar,"liip_json": liip_json,"vias_acceso":vias_acceso,"riesgo_distancia":riesgo_distancia, 
        "lista_espacios_encontrados_json":lista_espacios_encontrados_json,"lista_plan":lista_plan,
        "lista_servicios_basicos_json":lista_servicios_basicos_json, "factibilida_tecnica":factibilida_tecnica,
        "lista_infraetructura_json":lista_infraetructura_json, "descripcion_mejora":descripcion_mejora,
        "lista_riesgos_json":lista_riesgos_json}) #

def actualizarIM(request):
     if request.is_ajax and request.method == "POST":
        dtig =json.loads(request.POST.get('valoresifm'))
        for objif in dtig:
                ids=objif['ids']
                idIM=objif['idIM']
                fecha=objif['fecham']
                hora=objif['horam']
                telp=objif['telpm']
                tels=objif['telsm']
                terceraed=objif['terceraedm']
                adultos=objif['adultosm']
                ninos=objif['ninosm']
                personadis=objif['personadism']
                propietarioinm=objif['propietarioinmm']
                parentescosm=objif['parentescosm']
                latitud=objif['latitudm']
                longitud=objif['longitudm']
                inmueble=objif['inmueblem']
                usoact=objif['usoactm']
                exotrav=objif['exotravm']
                usoacotv=objif['usoacotvm']
                comentariosrl=objif['comentariosrl']

                idsol= Solicitud.objects.get(Id=ids)
                idsol.Id=ids
                inspeccionM=InspeccionMejo.objects.update_or_create(Id=idIM,
            defaults={
            'Fecha':fecha,'Hora':hora,'TelefonoPrim':telp,'TelefonoSegu':tels,
            'TerceraEdad':terceraed,'Adultos':adultos,'Ninos':ninos,'PersonaDisc':personadis,    
            'PropietarioInmu':propietarioinm,'ParentescoSoli':parentescosm,'Latitud':latitud,
            'Longitud':longitud,'Inmueble':inmueble,'UsoActu':usoact,'ExisteOtrViv':exotrav,
            'UsoActuOtrViv':usoacotv,'ComentariosRelv':comentariosrl,'IdSolicitud':idsol, 
            })
        registroBit(request, "Se actualizó formulario Inspeccion de Mejora " + idsol.IdPerfil.Dui, "Actualización")        
                
        data =json.loads( request.POST.get('valoresidi'))
        for obj in data:
            idc=obj['id']
            valor=obj['existeii']
            estado=obj['estadoii']
            tipo=obj['tiposist']
            idif= Infraestructura.objects.get(Id=idc)
            idif.Id=idc
            
            infraestructuraInmuebleipm = InfraestructuraInmuInsMej.objects.update_or_create(
            IdInfraestructura=idif,IdInspeccionMejo=idIM,defaults={
            'IdInfraestructura':idif,'Existe':valor,'Estado':estado,'TipoSist':tipo, 
            })
    #inicia espacios encontrados
        dataee =json.loads(request.POST.get('valoresee'))
        for obj in dataee:
                idce=obj['ide']
                valore=obj['valore']
                idife= Infraestructura.objects.get(Id=idce)
                #idife.id=idce   
                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.update_or_create(IdInfraestructura=idife,IdInspeccionMejo=idIM,
                defaults={'Existe':valore, }) 

    # fin
    #inicia servicios basicos    
        datasb =json.loads(request.POST.get('valoressbm'))
        for obj in datasb:
                idcs=obj['ids']
                valors=obj['valors']
                idifs= Infraestructura.objects.get(Id=idcs)
                idifs.Id=idcs
                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.update_or_create(IdInfraestructura=idifs,IdInspeccionMejo=idIM,
                defaults={'Existe':valors, })             
    # fin

    #inicia infraestructura    
        dataim =json.loads(request.POST.get('valoresim'))
        for obj in dataim:
                idci=obj['idi']
                valori=obj['valori']
                idifim= Infraestructura.objects.get(Id=idci)
                idifim.Id=idci
                inspeccionesirm = InspeccionMejoEspSerInfRie.objects.update_or_create(IdInfraestructura=idifim,IdInspeccionMejo=idIM,
                defaults={'Existe':valori })          
    # fin

    #inicia vias de acceso
        dtv =json.loads(request.POST.get('valoresvm'))
        for obj in dtv:
                tipovia=obj['tipovia']
                viasAccesoipm =  ViasAcceInsMej.objects.update_or_create(IdInspeccionMejo=idIM,defaults={
                    'TipoVias':tipovia, })    
    # fin

    #inicia riesgos    
        datar =json.loads(request.POST.get('valorestbrm'))
        for obj in datar:
                idcr=obj['idr']
                valorr=obj['valorr']
                idir= Infraestructura.objects.get(Id=idcr)
                idir.Id=idcr
                inspeccionesirmr = InspeccionMejoEspSerInfRie.objects.update_or_create(IdInfraestructura=idir,IdInspeccionMejo=idIM,
                    defaults={'Existe':valorr, })                 
    # fin

    #inicia distancia riesgos
        dtdr =json.loads(request.POST.get('valorestbdrm'))
        for objif in dtdr:
                distanciatl=objif['distanciatlm']
                distanciarc=objif['distanciarcm']
                distancialc=objif['distancialcm']
                distanciata=objif['distanciatam']

                riesgosipm = RiesgosInsMej.objects.update_or_create(IdInspeccionMejo=idIM,
                    defaults={'DistanciaTalu':distanciatl,'DistanciaRiosCer':distanciarc,
                    'DistanciaLadeCer':distancialc,'DistanciaTorrCer':distanciata, })  

    # fin

    #inicia etapas del plan de mejoramiento    
        dataet =json.loads(request.POST.get('valorestbetp'))
        for obj in dataet:
                valet=obj['valETP']
                etapa=obj['etapa']
                planMejoramientoipm = PlanMejoInsMej.objects.update_or_create(IdInspeccionMejo=idIM,Etapas=valet,
                    defaults={'Etapas':valet,'Descripcion':etapa, })        
    # fin

     #inicia factibilidades tecnicas mejora
        dttfm =json.loads(request.POST.get('valoresftm'))
        for obj in dttfm:
                factpm=obj['factpm']
                factibilidadipm = FactibilidadInsMej.objects.update_or_create(IdInspeccionMejo=idIM,
                    defaults={'Detalle':factpm})  

    #  

    #inicia descripción del mejoramiento acordado 
        dtdm =json.loads(request.POST.get('valoresdm'))
        for obj in dtdm:
                descripcionma=obj['descripcionma']
                diasestm=obj['diasestm']
                dMejoramientoipm = DescripcionMejoInsMej.objects.update_or_create(IdInspeccionMejo=idIM,
                    defaults={'Descripcion':descripcionma,'DiasEsti':diasestm})  

    #
     mensaje="Datos actualizados"
     messages.success(request, mensaje)
     return redirect('administrarPerfil', id=idsol.IdPerfil.Id)  # id de perfil 

############  Primera inspeccion
def pinspeccion(request,id,n): # id de la tabla inspeccion
    try:
        inspeccionM=InspeccionMejo.objects.get(Id=id)
    except InspeccionMejo.DoesNotExist:
        inspeccionM=""
    try:
        do= DatosObra.objects.get(IdSolicitud=inspeccionM.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
    try:
        DMipm = DescripcionMejoInsMej.objects.get(IdInspeccionMejo=id)
    except DescripcionMejoInsMej.DoesNotExist:
        DMipm=""
    
    return render(request,"InspeccionMejViviendaApp/pinspeccion.html", {"ipm":inspeccionM,"do":do,"dpi":DMipm, "n":n})



def registrarPIM(request):
    idim=request.POST['idm']
    try:
        ninspeccion=request.POST['ninspeccionm']
    except :
        ninspeccion=""
    try:
        fecha=request.POST['fecham']
    except :
        fecha=""
    try:
        mejoraar=request.POST['mejoraarm']
    except :
        mejoraar=""
    try:
        esquemam=request.FILES['esquemam']
    except :
        esquemam=""
    try:
        imagen=request.FILES.getlist('imagen')
    except :
        imagen=""

    idipm= InspeccionMejo.objects.get(Id=idim)
    idipm.Id=idim 

    pim= PrimeraInspMej.objects.create(NumeroInsp=ninspeccion,Fecha=fecha,MejoraReal=mejoraar,Esquema=esquemam,IdInspeccionMejo=idipm)
    
    # Obtener el ID de la instancia de pInspeccionm
    pimid= PrimeraInspMej.objects.get(Id=pim.Id)
    pimid.Id = pim.Id
    registroBit(request, "Se registro formulario "+ pimid.NumeroInsp + " Inspeccion de Mejora " + pimid.IdInspeccionMejo.IdSolicitud.IdPerfil.Dui, "Registro")

    for i in range(len(imagen)): #verifica el numero de imagenes que llegan
        if (imagen[i] != ""):
            print(imagen[i])
            print('llego')
            im =ImagenPrimInsMej.objects.create(Imagen=imagen[i],IdPrimeraInspMej=pimid)

    mensaje="Datos guardados"
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=pim.IdInspeccionMejo.IdSolicitud.IdPerfil.Id)  # id de perfil 

def listaPIM(request,id): 
    listaPIm=PrimeraInspMej.objects.filter(IdInspeccionMejo__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "InspeccionMejViviendaApp/listapim.html", {"listapim":listaPIm})

def editarPIM(request,id): # id de la tabla PrimeraInspMej
    try:
        pim=PrimeraInspMej.objects.get(Id=id)
    except PrimeraInspMej.DoesNotExist:
        pim=""
    try:
        inspeccionM=InspeccionMejo.objects.get(Id=pim.IdInspeccionMejo.Id)
    except InspeccionMejo.DoesNotExist:
        inspeccionM=""
    try:
        do= DatosObra.objects.get(IdSolicitud=inspeccionM.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
    try:
        DMipm = DescripcionMejoInsMej.objects.get(IdInspeccionMejo=inspeccionM.Id)
    except DescripcionMejoInsMej.DoesNotExist:
        DMipm=""

    try:
        imgpil= ImagenPrimInsMej.objects.filter(IdPrimeraInspMej=id)
    except ImagenPrimInsMej.DoesNotExist:
        imgpil=""
    
    return render(request,"InspeccionMejViviendaApp/editarPinspeccion.html", {"pim":pim,"ipm":inspeccionM,"do":do,"dpi":DMipm, "imgpil":imgpil})


def modificarPIM(request):
    idpim=request.POST['idim']
    try:
        ninspeccion=request.POST['ninspeccionm']
    except :
        ninspeccion=""
    try:
        fecha=request.POST['fecham']
    except :
        fecha=""
    try:
        mejoraar=request.POST['mejoraarm']
    except :
        mejoraar=""
    datoesq=request.POST['desquema']
    try:
        esquemam=request.FILES['esquemam']
    except :
        esquemam=""
    idimgp =request.POST.getlist('idimg')
    try:
        imagen=request.FILES.getlist('imagen')
    except :
        imagen=""
    

    mpim= PrimeraInspMej.objects.get(Id=idpim)
    mpim.NumeroInsp=ninspeccion
    mpim.Fecha=fecha
    mpim.MejoraReal=mejoraar

    if datoesq == "" :
        mpim.Esquema=esquemam

    if datoesq != "" and esquemam !="":
        mpim.Esquema=esquemam
    
    mpim.save()
    

    for i in range(len(imagen)): #verifica el numero de imagenes que llegan
        if i < len(idimgp) and idimgp[i] != "":
            # Si hay un valor válido en idimgp, actualizar el objeto existente
            pInspeccionm_obj = ImagenPrimInsMej.objects.get(Id=idimgp[i])
            mim = ImagenPrimInsMej.objects.update_or_create(Id=pInspeccionm_obj.Id, IdPrimeraInspMej=mpim, defaults={'Imagen': imagen[i], 'IdPrimeraInspMej': mpim})
        elif (imagen[i] != ""):
            print(imagen[i])
            im =ImagenPrimInsMej.objects.create(Imagen=imagen[i],IdPrimeraInspMej=mpim)

    mensaje="Datos actualizados"
    registroBit(request, "Se actualizo formulario "+ mpim.NumeroInsp +" Inspeccion de Mejora " + mpim.IdInspeccionMejo.IdSolicitud.IdPerfil.Dui, "Actualizacion")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=mpim.IdInspeccionMejo.IdSolicitud.IdPerfil.Id)  # id de perfil           
                
                
                
 
