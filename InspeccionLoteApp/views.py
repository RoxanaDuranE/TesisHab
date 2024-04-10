import json
from datetime import date
from django.shortcuts import render,redirect
from django.contrib import messages
from ConfiguracionApp.models import *
from InspeccionLoteApp.models import *
from PresupuestoVApp.models import *
from ListaChequeoApp.models import ListaCheq
from TesisApp.views import registroBit

# Create your views here.


def inspeccionl(request, id): 
    sol= InspeccionLote.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= InspeccionLote.objects.get(IdSolicitud=id)
    
        return redirect('editarIL', id=solv.Id)   
    else:
        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
        
        try:
            do= DatosObra.objects.get(IdSolicitud=id)
        except DatosObra.DoesNotExist:
            do=""

        try:
            listad=Infraestructura.objects.filter(Tipo=2,TipoLoteMej="Lote",Estado="activo")
        except Infraestructura.DoesNotExist:
            listad=""

        try:
            listat=Infraestructura.objects.filter(Tipo=3,TipoLoteMej="Lote",Estado="activo")
        except Infraestructura.DoesNotExist:
            listat=""

        try:
            listac=Infraestructura.objects.filter(Tipo=4,TipoLoteMej="Lote",Estado="activo")
        except Infraestructura.DoesNotExist:
            listac=""
        try:
            listacn=Infraestructura.objects.filter(Tipo=5,TipoLoteMej="Lote",Estado="activo")
        except Infraestructura.DoesNotExist: 
            listacn=""
        try:
            listase=Infraestructura.objects.filter(Tipo=6,TipoLoteMej="Lote",Estado="activo")
        except Infraestructura.DoesNotExist:
            listase=""

        return render(request, "InspeccionLoteApp/inspeccionl.html", {"s":s,"do":do, "listad":listad,"listat":listat,"listac":listac,"listacn":listacn,"listase":listase}) #, {"s":s,"d":d}

  
def registrarDIL(request): 
    
    if request.is_ajax and request.method == "POST":
            dtig =json.loads(request.POST.get('valoresif'))
            print(dtig)
            for objif in dtig:
                ids=objif['ids']
                fechal=objif['fechal']
                hora=objif['horal']
                telp=objif['telp']
                tels=objif['tels']
                terceraed=objif['terceraed']
                adultos=objif['adultos']
                ninos=objif['ninos']
                personadis=objif['personadis']
                propietarioinm=objif['propietarioinm']
                latitud=objif['latitud']
                longitud=objif['longitud']
                inmueble=objif['inmueble']
                exotrav=objif['exotrav']
                terrenoagric=objif['terrenoagric']
                anchocv=objif['anchocv']
                largocv=objif['largocv']
                areacv=objif['areacv']
                anchoaf=objif['anchoaf']
                largoaf=objif['largoaf']
                areaaf=objif['areaaf']

                idsol= Solicitud.objects.get(Id=ids)
                idsol.Id=ids

                inspeccionl=InspeccionLote.objects.create(Fecha=fechal,Hora=hora,TelefonoPrim=telp,TelefonoSegu=tels,TerceraEdad=terceraed,Adultos=adultos,Ninos=ninos,PersonaDisc=personadis,PropietarioTerr=propietarioinm,Latitud=latitud,Longitud=longitud,Inmueble=inmueble,ExisteOtraViv=exotrav,TerrenoAgri=terrenoagric,AnchoConsViv=anchocv,LargoConsViv=largocv,AreaConsViv=areacv,AnchoAmplFut=anchoaf,LargoAmplFut=largoaf,AreaAmplFut=areaaf,IdSolicitud=idsol)
                registroBit(request, "Se registro formulario Inspeccion de Lote " + idsol.IdPerfil.Dui, "Registro")
               # print(ids)
               # print(fechal)
   
            idip= InspeccionLote.objects.all().last() #obtengo la ultima solicitud registrada 
    # idip= Inspeccionl.objects.get(id=4)
    

    #inicia Construccones   
            data =json.loads( request.POST.get('valores'))
            print(data)
            for obj in data:
                idc=obj['id']
                valor=obj['valor']
                idif= Infraestructura.objects.get(Id=idc)
                idif.Id=idc
                
                print(idc)
                print(valor)

                inspeccionlcisr = InspeccionLoteConInfSanSerRie.objects.create(IdInfraestructura=idif,Existe=valor, IdInspeccionLote=idip)
    # fin

    #inicia infraestructura   
            dataif =json.loads(request.POST.get('valorestbif'))
            print(dataif)
            for obj in dataif:
                idci=obj['idi']
                valori=obj['valori']
                idifi= Infraestructura.objects.get(Id=idci)
                idifi.Id=idci
                
                print(idci)
                print(valori)

                inspeccionlcisrif = InspeccionLoteConInfSanSerRie.objects.create(IdInfraestructura=idifi,Existe=valori, IdInspeccionLote=idip)        
    # fin

      #inicia saneamiento
    
            datasa =json.loads(request.POST.get('valorestbsa'))
            print(datasa)
            for obj in datasa:
                idcs=obj['idi']
                valors=obj['valori']
                idisa= Infraestructura.objects.get(Id=idcs)
                idisa.Id=idcs
                
                print(idcs)
                print(valors)
                inspeccionlcisrsa = InspeccionLoteConInfSanSerRie.objects.create(IdInfraestructura=idisa,Existe=valors, IdInspeccionLote=idip)        
    # fin

    
     #inicia saneamiento
    
            datasb =json.loads(request.POST.get('valorestbsb'))
            print(datasb)
            for obj in datasb:
                idcsb=obj['idb']
                valorsb=obj['valorb']
                idisb= Infraestructura.objects.get(Id=idcsb)
                idisb.Id=idcsb
                
                print(idcsb)
                print(valorsb)
                inspeccionlcisrsb = InspeccionLoteConInfSanSerRie.objects.create(IdInfraestructura=idisb,Existe=valorsb, IdInspeccionLote=idip)        
    # fin

    
      #inicia riesgos   
            datar =json.loads(request.POST.get('valorestbr'))
            print(datar)
            for obj in datar:
                idcr=obj['idr']
                valorr=obj['valorr']
                idir= Infraestructura.objects.get(Id=idcr)
                idir.Id=idcr
                
                print(idcr)
                print(valorr)

                inspeccionlcisrr = InspeccionLoteConInfSanSerRie.objects.create(IdInfraestructura=idir,Existe=valorr, IdInspeccionLote=idip)        
    # fin

    #inicia distancia riesgos
            dtdr =json.loads(request.POST.get('valorestbdr'))
            print(dtdr)
            for objif in dtdr:
                distanciatl=objif['distanciatl']
                distanciarc=objif['distanciarc']
                distancialc=objif['distancialc']
                distanciata=objif['distanciata']

            riesgosipl = RiesgosInspLot.objects.create(DistanciaTalu=distanciatl,DistanciaRiosCer=distanciarc,DistanciaLadeCer=distancialc,DistanciaTorrAnt=distanciata, IdInspeccionLote=idip)  

    #
    #inicia comentarios y observaciones
            dtco =json.loads(request.POST.get('valoresco'))
            print(dtco)
            for obj in dtco:
                comentariosil=obj['comentariosil']
                observacionesil=obj['observacionesil']
                print(comentariosil)

            comentariosObsipl = ComentariosObseInsLot.objects.create(Comentarios=comentariosil,Observaciones=observacionesil, IdInspeccionLote=idip)  
    # fin

     #inicia vias de acceso
            dtv =json.loads(request.POST.get('valoresv'))
            print(dtv)
            for obj in dtv:
                tipovia=obj['tipovia']

            viasAccesoipl = ViasAcceInsLot.objects.create(TipoVias=tipovia, IdInspeccionLote=idip)  

    #
     #inicia factibilidades tecnicas
            dttf =json.loads(request.POST.get('valoresft'))
            print(dttf)
            for obj in dttf:
                factp=obj['factp']
                print(factp)

            factibilidadipl = FactibilidadInsLot.objects.create(Detalle=factp, IdInspeccionLote=idip)  

    #
     #inicia descripción del proyecto
            dtdp =json.loads(request.POST.get('valoresdp'))
            print(dtdp)
            for obj in dtdp:
                modelov=obj['modelov']
                solucions=obj['solucions']
                obrasa=obj['obrasa']
                obst=obj['obst']
                descripciona=obj['descripciona']
                print(descripciona)

            descripcionProyectoipl = DescripcionProyInsLot.objects.create(ModeloViviCon=modelov,SolucionSaniPro=solucions,ObrasAdicCon=obrasa,ObservacionesTecn=obst, ActividadRespFia=descripciona, IdInspeccionLote=idip) 

    #
      #inicia responsabilidades del solicitante
            dtrs =json.loads(request.POST.get('valoresrs'))
            print(dtrs)
            for obj in dtrs:
                mojonesl=obj['mojonesl']
                linderosl=obj['linderosl']
                resguardom=obj['resguardom']
                auxiliarc=obj['auxiliarc']
                aguap=obj['aguap']
                energiae=obj['energiae']
                print(energiae)

            responSolicitanteipl = ResponsabilidadSoliInsLot.objects.create(MojonesLote=mojonesl,LinderosLote=linderosl,ResguardoMate=resguardom,AuxiliaresCons=auxiliarc,AguaPota=aguap,EnergiaElec=energiae , IdInspeccionLote=idip) 
    #

    #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.get(IdSolicitud=idsol)
    lchequo.InspeccionTecn ="Si"
    lchequo.save()

    return redirect('administrarPerfil', id=inspeccionl.IdSolicitud.IdPerfil.Id)  # id de perfil 

def listaI(request,id): 
    listaI=FactibilidadInsLot.objects.filter(IdInspeccionLote__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "InspeccionLoteApp/listail.html", {"listai":listaI})

def editarIL(request, id): #id inspeccion lote
    try:
        ipl=InspeccionLote.objects.get(Id=id)
    except InspeccionLote.DoesNotExist:
        ipl=""

    try:
        s= Solicitud.objects.get(Id=ipl.IdSolicitud.Id)
    except Solicitud.DoesNotExist:
        s=""
    
    try:
        do= DatosObra.objects.get(IdSolicitud=ipl.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""

    try:
        listad=Infraestructura.objects.filter(Tipo=2,TipoLoteMej="Lote",Estado="activo")
    except Infraestructura.DoesNotExist:
        listad=""

    try:
        listat=Infraestructura.objects.filter(Tipo=3,TipoLoteMej="Lote",Estado="activo")
    except Infraestructura.DoesNotExist:
        listat=""

    try:
        listac=Infraestructura.objects.filter(Tipo=4,TipoLoteMej="Lote",Estado="activo")
    except Infraestructura.DoesNotExist:
        listac=""

    try:
        listacn=Infraestructura.objects.filter(Tipo=5,TipoLoteMej="Lote",Estado="activo")
    except Infraestructura.DoesNotExist: 
        listacn=""

    try:
        listase=Infraestructura.objects.filter(Tipo=6,TipoLoteMej="Lote",Estado="activo")
    except Infraestructura.DoesNotExist:
        listase=""

    #try:
    #    liip = Inspeccionlcisr.objects.filter(idip=ipl.id)
    #    liip_data = [
    #    {
    #        'existe': item.existe,
    #        'estado': item.estado,
    #        'tiposistema': item.tiposistema,
    #        'id': item.id,
    #    }
    #    for item in liip
    #    ]

    #    liip_json = json.dumps(liip_data)
    #except liip.DoesNotExist:
    #    liip=""
    
    lista_general=InspeccionLoteConInfSanSerRie.objects.filter(IdInspeccionLote=ipl.Id)

    lista_construcciones_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "2": # si el tipo 2 se encuentra en la lista_general se agrega  a su respectiva lista
            lista_construcciones_datos.append ( {'existe': item.Existe, 'id': item.Id, })
    lista_construcciones_json = json.dumps(lista_construcciones_datos)

    lista_infraestructura_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "3":
            lista_infraestructura_datos.append ( {'existe': item.Existe, 'id': item.Id, })
    lista_infraestructura_json = json.dumps(lista_infraestructura_datos)

    lista_saneamiento_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "4":
            lista_saneamiento_datos.append ( {'existe': item.Existe, 'id': item.Id, })
    lista_saneamiento_json = json.dumps(lista_saneamiento_datos)

    lista_servicios_basicos_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "5":
            lista_servicios_basicos_datos.append ( {'existe': item.Existe, 'id': item.Id, })
    lista_servicios_basicos_json = json.dumps(lista_servicios_basicos_datos)

    lista_riesgos_datos=[]
    for item in lista_general:
        if item.IdInfraestructura.Tipo == "6":
            lista_riesgos_datos.append ( {'existe': item.Existe, 'id': item.Id, })
    lista_riesgos_json = json.dumps(lista_riesgos_datos)

    try:
        rs=  RiesgosInspLot.objects.get(IdInspeccionLote=id)
    except RiesgosInspLot.DoesNotExist:
        rs=""
    
    try:
        cm=  ComentariosObseInsLot.objects.get(IdInspeccionLote=id)
    except ComentariosObseInsLot.DoesNotExist:
        cm=""

    try:
        vs=  ViasAcceInsLot.objects.get(IdInspeccionLote=id)
    except ViasAcceInsLot.DoesNotExist:
        vs=""
    
    try:
        ft=  FactibilidadInsLot.objects.get(IdInspeccionLote=id)
    except FactibilidadInsLot.DoesNotExist:
        ft=""
        
    try:
        dp=  DescripcionProyInsLot.objects.get(IdInspeccionLote=id)
    except DescripcionProyInsLot.DoesNotExist:
        dp=""
    
    try:
        rps=  ResponsabilidadSoliInsLot.objects.get(IdInspeccionLote=id)
    except ResponsabilidadSoliInsLot.DoesNotExist:
        rps=""
      
    return render(request, "InspeccionLoteApp/editarInspeccionl.html", {"ipl":ipl,"s":s,"do":do,
            "listad":listad, "listat":listat,"listac":listac,"listacn":listacn,"listase":listase,
            "lista_construcciones_json":lista_construcciones_json,
            "lista_infraestructura_json":lista_infraestructura_json,
            "lista_saneamiento_json":lista_saneamiento_json,
            "lista_servicios_basicos_json":lista_servicios_basicos_json,
            "lista_riesgos_json":lista_riesgos_json,"rs":rs,"cm":cm,"vs":vs,"ft":ft,"dp":dp,"rps":rps}) 



def modificarIL(request): 
    
    if request.is_ajax and request.method == "POST":
            dtig =json.loads(request.POST.get('valoresif'))
            print(dtig)
            for objif in dtig:
                ids=objif['ids']
                idIL=objif['idIL']
                fechal=objif['fechal']
                hora=objif['horal']
                telp=objif['telp']
                tels=objif['tels']
                terceraed=objif['terceraed']
                adultos=objif['adultos']
                ninos=objif['ninos']
                personadis=objif['personadis']
                propietarioinm=objif['propietarioinm']
                latitud=objif['latitud']
                longitud=objif['longitud']
                inmueble=objif['inmueble']
                exotrav=objif['exotrav']
                terrenoagric=objif['terrenoagric']
                anchocv=objif['anchocv']
                largocv=objif['largocv']
                areacv=objif['areacv']
                anchoaf=objif['anchoaf']
                largoaf=objif['largoaf']
                areaaf=objif['areaaf']
                print(ids)

                idsol= Solicitud.objects.get(Id=ids)
                idsol.Id=ids

                inspeccionl=InspeccionLote.objects.update_or_create(Id=idIL,
                defaults={ 'Fecha':fechal,'Hora':hora,'TelefonoPrim':telp,'TelefonoSegu':tels,'TerceraEdad':terceraed,
                          'Adultos':adultos,'Ninos':ninos,'PersonaDisc':personadis,'PropietarioTerr':propietarioinm,
                          'Latitud':latitud,'Longitud':longitud,'Inmueble':inmueble,'ExisteOtraViv':exotrav,
                          'TerrenoAgri':terrenoagric,'AnchoConsViv':anchocv,'LargoConsViv':largocv,'AreaConsViv':areacv,
                          'AnchoAmplFut':anchoaf,'LargoAmplFut':largoaf,'AreaAmplFut':areaaf,'IdSolicitud':idsol,})
                
                registroBit(request, "Se actualizó formulario Inspeccion de Lote " + idsol.IdPerfil.Dui, "Actualización") 
   

               # print(ids)
               # print(fechal)


    #inicia Construccones
    
            data =json.loads( request.POST.get('valores'))
            print(data)
            for obj in data:
                idc=obj['id']
                valor=obj['valor']
                idif= Infraestructura.objects.get(Id=idc)
                idif.Id=idc
                
                print(idc)
                print(valor)

                inspeccionlcisr = InspeccionLoteConInfSanSerRie.objects.update_or_create(IdInfraestructura=idif,IdInspeccionLote=idIL,
                                  defaults={'Existe':valor,})

    # fin

    #inicia infraestructura
    
            dataif =json.loads(request.POST.get('valorestbif'))
            print(dataif)
            for obj in dataif:
                idci=obj['idi']
                valori=obj['valori']
                idifi= Infraestructura.objects.get(Id=idci)
                idifi.Id=idci
                
                print(idci)
                print(valori)

                inspeccionlcisrif = InspeccionLoteConInfSanSerRie.objects.update_or_create(IdInfraestructura=idifi,IdInspeccionLote=idIL,
                                    defaults={'Existe':valori,})      
    # fin

      #inicia saneamiento
    
            datasa =json.loads(request.POST.get('valorestbsa'))
            print(datasa)
            for obj in datasa:
                idcs=obj['idi']
                valors=obj['valori']
                idisa= Infraestructura.objects.get(Id=idcs)
                idisa.Id=idcs
                
                print(idcs)
                print(valors)

                inspeccionlcisrsa = InspeccionLoteConInfSanSerRie.objects.update_or_create(IdInfraestructura=idisa,IdInspeccionLote=idIL,
                                    defaults={'Existe':valors,})       
    # fin

    
     #inicia servicios basicos
    
            datasb =json.loads(request.POST.get('valorestbsb'))
            print(datasb)
            for obj in datasb:
                idcsb=obj['idb']
                valorsb=obj['valorb']
                idisb= Infraestructura.objects.get(Id=idcsb)
                idisb.Id=idcsb
                
                print(idcsb)
                print(valorsb)

                inspeccionlcisrsb = InspeccionLoteConInfSanSerRie.objects.update_or_create(IdInfraestructura=idisb,IdInspeccionLote=idIL,
                                    defaults={'Existe':valorsb, })         
    # fin

    
      #inicia riesgos
    
            datar =json.loads(request.POST.get('valorestbr'))
            print(datar)
            for obj in datar:
                idcr=obj['idr']
                valorr=obj['valorr']
                idir= Infraestructura.objects.get(Id=idcr)
                idir.Id=idcr
                
                print(idcr)
                print(valorr)

                inspeccionlcisrr = InspeccionLoteConInfSanSerRie.objects.update_or_create(IdInfraestructura=idir,IdInspeccionLote=idIL,
                                   defaults={'Existe':valorr,})         
    # fin

    #inicia distancia riesgos
            dtdr =json.loads(request.POST.get('valorestbdr'))
            print(dtdr)
            for objif in dtdr:
                distanciatl=objif['distanciatl']
                distanciarc=objif['distanciarc']
                distancialc=objif['distancialc']
                distanciata=objif['distanciata']

            riesgosipl = RiesgosInspLot.objects.update_or_create(IdInspeccionLote=idIL,
                      defaults={'DistanciaTalu':distanciatl,'DistanciaRiosCer':distanciarc,'DistanciaLadeCer':distancialc,'DistanciaTorrAnt':distanciata, })  

    #
    #inicia comentarios y observaciones
            dtco =json.loads(request.POST.get('valoresco'))
            print(dtco)
            for obj in dtco:
                comentariosil=obj['comentariosil']
                observacionesil=obj['observacionesil']
                print(comentariosil)

            comentariosObsipl = ComentariosObseInsLot.objects.update_or_create(IdInspeccionLote=idIL,
                              defaults={'Comentarios':comentariosil,'Observaciones':observacionesil, })

    #

    
     #inicia vias de acceso
            dtv =json.loads(request.POST.get('valoresv'))
            print(dtv)
            for obj in dtv:
                tipovia=obj['tipovia']

            viasAccesoipl = ViasAcceInsLot.objects.update_or_create(IdInspeccionLote=idIL,
                           defaults={'TipoVias':tipovia, })

    #
     #inicia factibilidades tecnicas
            dttf =json.loads(request.POST.get('valoresft'))
            print(dttf)
            for obj in dttf:
                factp=obj['factp']
                print(factp)

            factibilidadipl = FactibilidadInsLot.objects.update_or_create(IdInspeccionLote=idIL,
                              defaults={ 'Detalle':factp, }) 

    #
     #inicia descripción del proyecto
            dtdp =json.loads(request.POST.get('valoresdp'))
            print(dtdp)
            for obj in dtdp:
                modelov=obj['modelov']
                solucions=obj['solucions']
                obrasa=obj['obrasa']
                obst=obj['obst']
                descripciona=obj['descripciona']
                print(descripciona)

            descripcionProyectoipl = DescripcionProyInsLot.objects.update_or_create(IdInspeccionLote=idIL,
                defaults={'ModeloViviCon':modelov,'SolucionSaniPro':solucions,'ObrasAdicCon':obrasa,
                'ObservacionesTecn':obst, 'ActividadRespFia':descripciona, })

    #
      #inicia responsabilidades del solicitante
            dtrs =json.loads(request.POST.get('valoresrs'))
            print(dtrs)
            for obj in dtrs:
                mojonesl=obj['mojonesl']
                linderosl=obj['linderosl']
                resguardom=obj['resguardom']
                auxiliarc=obj['auxiliarc']
                aguap=obj['aguap']
                energiae=obj['energiae']
                print(energiae)

            responSolicitanteipl = ResponsabilidadSoliInsLot.objects.update_or_create(IdInspeccionLote=idIL,
                defaults={'MojonesLote':mojonesl,'LinderosLote':linderosl,'ResguardoMate':resguardom,
                          'AuxiliaresCons':auxiliarc, 'AguaPota':aguap,'EnergiaElec':energiae , })
    #
    return redirect('administrarPerfil', id=idsol.IdPerfil.Id)  # id de perfil 
  


############  Primera inspeccion

def pinspeccionl(request, id, n): # id de la tabla inspeccion
    try:
        inspeccionl=InspeccionLote.objects.get(Id=id)
    except InspeccionLote.DoesNotExist:
        inspeccionl=""
    try:
        do= DatosObra.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""       
    try:
        DPipl = DescripcionProyInsLot.objects.get(IdInspeccionLote=id)
    except DescripcionProyInsLot.DoesNotExist:
        DPipl=""
    try:
        pdg= PresupuestoViviDatGen.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
    except PresupuestoViviDatGen.DoesNotExist:
        pdg=""
    return render(request,"InspeccionLoteApp/pinspeccionl.html", {"ipl":inspeccionl,"do":do,"dpi":DPipl,"pdg":pdg, "n":n})

def registrarPIL(request):
    idil=request.POST['idi']
    try:
        ninspeccion=request.POST['ninspeccion']
    except :
        ninspeccion=""
    try:
        fecha=request.POST['pfecha']
    except :
        fecha=""
    try:
        esquema=request.FILES['archivoesq']
    except :
        esquema=""
    try:
        ubicacion=request.FILES['archivoubic']
    except :
        ubicacion=""
    try:
        reportef=request.FILES.getlist('archivorepf')
    except :
        reportef=""

    idipl= InspeccionLote.objects.get(Id=idil)
    idipl.Id=idil 

    pil= PrimeraInspLot.objects.create(NumeroInsp=ninspeccion,Fecha=fecha,Esquema=esquema,Ubicacion=ubicacion,IdInspeccionLote=idipl)

    # Obtener el ID de la instancia de pInspeccion
    pilid= PrimeraInspLot.objects.get(Id=pil.Id)
    pilid.Id = pil.Id

    for i in range(len(reportef)): #verifica el numero de imagenes que llegan
        if (reportef[i] != ""):
            print(reportef[i])
            print('llego')
            im =ImagenPrimInsLot.objects.create(ReporteFoto=reportef[i],IdPrimeraInspLot=pilid)
    registroBit(request, "Se registro formulario "+ pilid.NumeroInsp + " Inspeccion de Lote " + idipl.IdSolicitud.IdPerfil.Dui, "Registro")
    
    return redirect('administrarPerfil', id=pil.IdInspeccionLote.IdSolicitud.IdPerfil.Id)  # id de perfil 

def listaPIL(request,id): 
    listapI=PrimeraInspLot.objects.filter(IdInspeccionLote__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "InspeccionLoteApp/listapil.html", {"listapi":listapI})

def editarPIL(request, id): # id de la tabla PrimeraInspLot
    try:
        pil=PrimeraInspLot.objects.get(Id=id)
    except PrimeraInspLot.DoesNotExist:
        pil=""
    try:
        inspeccionl=InspeccionLote.objects.get(Id=pil.IdInspeccionLote.Id)
    except InspeccionLote.DoesNotExist:
        inspeccionl=""
    try:
        do= DatosObra.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""       
    try:
        DPipl = DescripcionProyInsLot.objects.get(IdInspeccionLote=inspeccionl.Id)
    except DescripcionProyInsLot.DoesNotExist:
        DPipl=""
    try:
        pdg= PresupuestoViviDatGen.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
    except PresupuestoViviDatGen.DoesNotExist:
        pdg=""

    try:
        imgpil= ImagenPrimInsLot.objects.filter(IdPrimeraInspLot=id)
    except ImagenPrimInsLot.DoesNotExist:
        imgpil=""

        
    return render(request,"InspeccionLoteApp/editarPinspeccionl.html", {"pil":pil,"ipl":inspeccionl,"do":do,"dpi":DPipl,"pdg":pdg, "imgpil":imgpil})


def modificarPIL(request):
    idpil=request.POST['idpi']
    try:
        ninspeccion=request.POST['ninspeccion']
    except :
        ninspeccion=""
    try:
        fecha=request.POST['pfecha']
    except :
        fecha=""
        
    datoesq=request.POST['desquema']
    
    try:
        esquemam=request.FILES['archivoesq']
    except :
        esquemam=""

    datoubi=request.POST['dubicacion']    

    try:
        ubicacionm=request.FILES['archivoubic']
    except :
        ubicacionm=""
    idimgp =request.POST.getlist('idimg')
    try:
        reportef=request.FILES.getlist('archivorepf')
    except :
        reportef=""

    mpil= PrimeraInspLot.objects.get(Id=idpil)
    mpil.NumeroInsp=ninspeccion
    mpil.Fecha=fecha

    if datoesq == "" :
        mpil.Esquema=esquemam

    if datoesq != "" and esquemam !="":
        mpil.Esquema=esquemam

    if datoubi == "" :
        mpil.Ubicacion=ubicacionm

    if datoubi != "" and ubicacionm !="":
        mpil.Ubicacion=ubicacionm

    mpil.save()

        
    # Iterar a través de reportef y crear objetos en la base de datos
    for i in range(len(reportef)):
        if i < len(idimgp) and idimgp[i] != "":
            # Si hay un valor válido en idimgp, actualizar el objeto existente
            pInspeccion_obj = ImagenPrimInsLot.objects.get(Id=idimgp[i])
            mim = ImagenPrimInsLot.objects.update_or_create(Id=pInspeccion_obj.Id, IdPrimeraInspLot=mpil, defaults={'ReporteFoto': reportef[i], 'IdPrimeraInspLot': mpil})
        elif reportef[i] != "":
            # Si idimgp está vacío o no hay un valor válido en idimgp, crear un nuevo objeto
            mim = ImagenPrimInsLot.objects.create(IdPrimeraInspLot=mpil, ReporteFoto=reportef[i])


    mensaje="Datos Actualizados"
    registroBit(request, "Se actualizo formulario "+ mpil.NumeroInsp +" Inspeccion de Lote " + mpil.IdInspeccionLote.IdSolicitud.IdPerfil.Dui, "Actualizacion")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=mpil.IdInspeccionLote.IdSolicitud.IdPerfil.Id)  # id de perfil 
