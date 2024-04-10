import json
from django.contrib import messages
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import TemplateView
from PresupuestoVApp.models import *
from ConfiguracionApp.models import *
from ListaChequeoApp.models import ListaCheq
from TesisApp.views import registroBit

# Create your views here.

def presupuestov(request, id):
    sol= PresupuestoViviDatGen.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= PresupuestoViviDatGen.objects.get(IdSolicitud=id)
    
        return redirect('editarPV', id=solv.Id)   
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
            d=  Detalle.objects.get(IdSolicitud=id)
        except Detalle.DoesNotExist:
            d=""
        
        try:
            listam=Materiales.objects.filter(Estado="activo")
        except Materiales.DoesNotExist:
            listam=""

    
        return render(request,"PresupuestoVApp/presupuesto.html", {"materiales":listam, "s":s, "do":do, "d":d})

# carga los datos del material seleccionado en los inputs
def get(request):
    id=request.GET['idmaterial']
    if request.is_ajax():
        material=Materiales.objects.get(Id=id)
        serialized_data = serialize("json",[material])
        return HttpResponse(serialized_data, content_type="application/json")
    else:
       listam=Materiales.objects.filter(Estado="activo")
       return render(request,"PresupuestoVApp/presupuesto.html", {"materiales":listam})

def registrarPV(request): 
    
 if request.is_ajax and request.method == "POST":
    dtig =json.loads(request.POST.get('valoresig'))
    print(dtig)
    for objif in dtig:
        ids=objif['ids']
        fecha=objif['fecha']
        tiempoconstruccion =objif['tiempoc']
        modelo =objif['modelo']
        dimensionviv =objif['dimension']
        cantidadvivienda =objif['cantv']
        costototalv =objif['costotv']
        
    
        print(fecha)
        print( modelo)
        print(dimensionviv)
        print( costototalv)
    

        idsol= Solicitud.objects.get(Id=ids)
        idsol.Id=ids 

        presupuestodg= PresupuestoViviDatGen.objects.create(Fecha=fecha,TiempoCons=tiempoconstruccion,Modelo=modelo,DimensionVivi=dimensionviv,CantidadVivi=cantidadvivienda,CostoTotaViv=costototalv,IdSolicitud=idsol ) #
    

        idpdg= PresupuestoViviDatGen.objects.all().last() #obtengo el ultimo registro de los datos generales de presupuesto
        
        ###### para tabla de materiales
        
        datamt =json.loads( request.POST.get('valorestmt'))
        print(datamt)  
        for obj in datamt:
                idmp=obj['idm'] # id del material
                cantidad=obj['cantidad']
                preciouni=obj['preciouni']
                subtotal=obj['subtotal']
                
                idm= Materiales.objects.get(Id=idmp)
                idm.id=idmp
                
                #ma=obj['idm']
                print(cantidad)
                print(preciouni)
                print(subtotal)
            
                PreMate = PresupuestoViviMat.objects.filter(IdMateriales=idm,IdPresupuestoViviDatGen=idpdg ).exists()
                print(PreMate)
                #PresupuestoMateriales()
                if PreMate== True:
                    presupuestoMateriales=PresupuestoViviMat.objects.get(IdMateriales=idm,IdPresupuestoViviDatGen=idpdg )
                
                    print(presupuestoMateriales.Cantidad)
                    presupuestoMateriales.Cantidad=presupuestoMateriales.Cantidad+cantidad
                    presupuestoMateriales.PrecioUnit=presupuestoMateriales.PrecioUnit+preciouni
                    presupuestoMateriales.SubTota=presupuestoMateriales.SubTota+subtotal
                    presupuestoMateriales.save()
                else:
                    presupuestoMateriales= PresupuestoViviMat.objects.create(Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal,IdMateriales=idm,IdPresupuestoViviDatGen=idpdg)
  
  ###  para tabla mano de obra
        datamo =json.loads( request.POST.get('valorestmo'))
        print(datamo)  
        for obj in datamo:
                descripcion=obj['descripc'] # id del material
                unidad=obj['unidad']
                preciouni=obj['preciouni']
                cantidad=obj['cantidad']
                subtotal=obj['subtotal']
                
                print(descripcion)
                print(cantidad)
                print(preciouni)
                print(subtotal)
            
                PreMo = PresupuestoViviManObr.objects.filter(IdPresupuestoViviDatGen=idpdg,Descripcion=descripcion, Unidad=unidad).exists()
                print(PreMo)

                if PreMo== True:
                    presupuestoManoObra=PresupuestoViviManObr.objects.get(IdPresupuestoViviDatGen=idpdg )
                
                    presupuestoManoObra.Cantidad=presupuestoManoObra.Cantidad+cantidad
                    presupuestoManoObra.PrecioUnit=float(presupuestoManoObra.PrecioUnit)+preciouni
                    presupuestoManoObra.SubTota=float(presupuestoManoObra.SubTota)+subtotal
                    presupuestoManoObra.save()
                else:
                    presupuestoManoObra= PresupuestoViviManObr.objects.create(Descripcion=descripcion,Unidad=unidad,Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal,IdPresupuestoViviDatGen=idpdg)

   
        ### para otras especificaciones
        dtesp =json.loads(request.POST.get('valoresesp'))
        print(dtesp)
        for obje in dtesp:
            materiales=obje['material']
            manoobra=obje['manoob']
            transporte=obje['transporte']
            solucionsanit=obje['solucions']
            kitemerg=obje['kitemg']
            herramientas=obje['herramienta']
            totalcostosd=obje['totalcd']

            if(manoobra=="" ):
                manoobra = 0.00  
            if(transporte=="" ):
                transporte = 0.00  
            if(solucionsanit=="" ):
                solucionsanit = 0.00  
            if(kitemerg=="" ):
                kitemerg = 0.00  
            if(herramientas=="" ):
                herramientas = 0.00   


            print(materiales)
            print( manoobra)
            print(transporte)
            print(totalcostosd)

            
            presupvt= PresupuestoViviTot.objects.create(Materiales=materiales,ManoObra=manoobra,Transporte=transporte,SolucionSani=solucionsanit,KitEmer=kitemerg,Herramientas=herramientas,TotalCostDir=totalcostosd,IdPresupuestoViviDatGen=idpdg ) 

    
    #####################################################
    # para guardar en la lista de chequeo 
    lchequo= ListaCheq.objects.get(IdSolicitud=idsol)
    lchequo.PresupuestoCons ="Si"
    lchequo.save()

    mensaje="Datos guardados"
    registroBit(request, "Se registro formulario Presupuesto de Vivienda " + idsol.IdPerfil.Dui, "Registro")
    messages.success(request, mensaje)
    #return JsonResponse(data=response_json, status=200)
    return redirect('administrarPerfil', id=presupuestodg.IdSolicitud.IdPerfil.Id)  # id de perfil 
 
#mensaje="Datos guardados"
    #return JsonResponse(data=response_json, status=200)
    #return HttpResponse(response_json)
    #return redirect('/SolicitudesApp/listaSoli/presupuesto/1'+)

def listaPV(request,id): 
    listapm=PresupuestoViviTot.objects.filter(IdPresupuestoViviDatGen__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "PresupuestoVApp/listaPV.html", {"listap":listapm})


def editarPV(request, id):# id presupuesto dg
    lista_materiales_json = []
    lista_mano_obra_json = []

    try:
        pvdg=  PresupuestoViviDatGen.objects.get(Id=id)
    except PresupuestoViviDatGen.DoesNotExist:
        pvdg=""
    try:
        s=  Solicitud.objects.get(Id=pvdg.IdSolicitud.Id)
    except Solicitud.DoesNotExist:
        s=""

    try:
        do= DatosObra.objects.get(IdSolicitud=pvdg.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
    
    try:
        d=  Detalle.objects.get(IdSolicitud=pvdg.IdSolicitud.Id)
    except Detalle.DoesNotExist:
        d=""
    
    try:
        listam=Materiales.objects.filter(Estado="activo")
    except Materiales.DoesNotExist:
        listam=""
    try:
        pvt=  PresupuestoViviTot.objects.get(IdPresupuestoViviDatGen=id)
    except PresupuestoViviTot.DoesNotExist:
        pvt=""

    try:
        lista_materiales= PresupuestoViviMat.objects.filter(IdPresupuestoViviDatGen=pvdg.Id)
        datos=[]
        for item in lista_materiales:
            datos.append ( {'id': item.Id, 'precio':item.PrecioUnit,'cantida': item.Cantidad,'total':item.SubTota,
            "nombre":item.IdMateriales.Nombre,"descripcion":item.IdMateriales.Descripcion,"unidad":item.IdMateriales.Unidad,"idm":item.IdMateriales.Id })
        lista_materiales_json = json.dumps(datos,default=str)
    except PresupuestoViviMat.DoesNotExist:
        lista_materiales=""

    try:
        lista_mano_obra= PresupuestoViviManObr.objects.filter(IdPresupuestoViviDatGen=pvdg.Id)
        datos=[]
        for item in lista_mano_obra:
            datos.append({
                "id":item.Id,
                "descripcion":item.Descripcion,
                "unidad":item.Unidad,
                "preciouni":item.PrecioUnit,
                "cantidad":item.Cantidad,
                "total":item.SubTota,
            })
            lista_mano_obra_json = json.dumps(datos, default=str)
    except PresupuestoViviManObr.DoesNotExist:
        lista_mano_obra=""
        lista_mano_obra_json=""

    
    return render(request,"PresupuestoVApp/editarPresupuesto.html", {"materiales":listam,"pvdg":pvdg,
                             "s":s, "do":do, "d":d,"pvt":pvt, "listMateriales":lista_materiales_json,
                             "lista_mano_obra_json":lista_mano_obra_json,})

def actualizar_presupuestoV(request):
    if request.is_ajax and request.method == "POST":
        dtig =json.loads(request.POST.get('valoresig'))
        for objif in dtig:
            ids=objif['ids']
            fecha=objif['fecha']
            tiempoconstruccion =objif['tiempoc']
            modelo =objif['modelo']
            dimensionviv =objif['dimension']
            cantidadvivienda =objif['cantv']
            costototalv =objif['costotv']                   
            presupuesto = objif['idPresupuesto']  
            
            idsol= Solicitud.objects.get(Id=ids)
            idsol.Id=ids 
            presupuesto = PresupuestoViviDatGen.objects.get(Id=presupuesto, IdSolicitud=idsol.Id)

            presupuestodg= PresupuestoViviDatGen.objects.update_or_create(IdSolicitud=idsol, Id=presupuesto.Id ,
            defaults={
                "Fecha":fecha,
                "TiempoCons":tiempoconstruccion,
                "Modelo":modelo,
                "DimensionVivi":dimensionviv,
                "CantidadVivi":cantidadvivienda,
                "CostoTotaViv":costototalv,
                "IdSolicitud":idsol }) #
        
            idpdg= presupuesto #obtengo el ultimo registro de los datos generales de presupuesto
            
            ###### para tabla de materiales
            
            datamt =json.loads( request.POST.get('valorestmt'))
            lista_original = PresupuestoViviMat.objects.filter(
                IdPresupuestoViviDatGen=presupuesto.Id)
            lista_actual = []  # el id que no este aqui se eliminara
            for obj in datamt:
                    idmp=obj['idm'] # id del material
                    cantidad=obj['cantidad']
                    preciouni=obj['preciouni']
                    subtotal=obj['subtotal']
                    
                    idm= Materiales.objects.get(Id=idmp)
                    idm.Id=idmp
                    lista_actual.append(idmp) 
                    PreMate = PresupuestoViviMat.objects.update_or_create(IdMateriales=idm, IdPresupuestoViviDatGen=presupuesto.Id,
                        defaults={
                            "PrecioUnit":preciouni,
                            "Cantidad":cantidad,
                            "SubTota":subtotal,
                            "IdMateriales":idm,
                            "IdPresupuestoViviDatGen":idpdg,
                        })
            # ciclo para eliminar  material
            for item in lista_original:
                if ((item.IdMateriales.Id in lista_actual) == False):
                    PreMate = PresupuestoViviMat.objects.get(
                        IdMateriales=item.IdMateriales, IdPresupuestoViviDatGen=presupuesto.Id)
                    PreMate.delete()
        
    ###  para tabla mano de obra
            datamo = json.loads( request.POST.get('valorestmo'))
            lista_original = PresupuestoViviManObr.objects.filter(
                IdPresupuestoViviDatGen=presupuesto.Id)
            lista_actual = []
            for obj in datamo:
                    id =obj['id']
                    descripcion=obj['descripc'] 
                    unidad=obj['unidad']
                    preciouni=obj['preciouni']
                    cantidad=obj['cantidad']
                    subtotal=obj['subtotal']
                    
                    try: 
                        mano_obra = PresupuestoViviManObr.objects.update_or_create( Id=id, IdPresupuestoViviDatGen=presupuesto.Id,
                                defaults={
                                "Descripcion":descripcion, 
                                "Unidad":unidad, 
                                "PrecioUnit":preciouni, 
                                "Cantidad":cantidad, 
                                "SubTota":subtotal, 
                                "IdPresupuestoViviDatGen":presupuesto, 
                                })  
                        lista_actual.append(int(id))
                    except Exception:
                        presupuestoManoObra= PresupuestoViviManObr.objects.create(Descripcion=descripcion,
                                Unidad=unidad,
                                Cantidad=cantidad, 
                                PrecioUnit=preciouni, 
                                SubTota=subtotal,
                                IdPresupuestoViviDatGen=idpdg)     
                        lista_actual.append(presupuestoManoObra.Id)
                                
            # ciclo para eliminar mano de obra
            for item in lista_original:
                if ((item.Id in lista_actual) == False):
                    PreMate = PresupuestoViviManObr.objects.get(
                        Id=item.Id, IdPresupuestoViviDatGenp=presupuesto.Id)
                    PreMate.delete()
            ### para otras especificaciones
            dtesp = json.loads(request.POST.get('valoresesp'))
            
            for obje in dtesp:
                materiales=obje['material']
                manoobra=obje['manoob']
                transporte=obje['transporte']
                solucionsanit=obje['solucions']
                kitemerg=obje['kitemg']
                herramientas=obje['herramienta']
                totalcostosd=obje['totalcd']

                if(manoobra=="" ):
                    manoobra = 0.00  
                if(transporte=="" ):
                    transporte = 0.00  
                if(solucionsanit=="" ):
                    solucionsanit = 0.00  
                if(kitemerg=="" ):
                    kitemerg = 0.00  
                if(herramientas=="" ):
                    herramientas = 0.00  
                     
                presupvt= PresupuestoViviTot.objects.update_or_create(IdPresupuestoViviDatGen=presupuesto.Id,
                    defaults={
                        "Materiales":materiales,
                        "ManoObra":manoobra,
                        "Transporte":transporte,
                        "SolucionSani":solucionsanit,
                        "KitEmer":kitemerg,
                        "Herramientas":herramientas,
                        "TotalCostDir":totalcostosd,
                        "IdPresupuestoViviDatGen":idpdg} ) 

        
        
    mensaje="Datos actualizados"
    registroBit(request, "Se actualizó Presupuesto de Vivienda " + idsol.IdPerfil.Dui, "Actualización")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=idsol.IdPerfil.Id)  # id de perfil ")
    

# para presupuesto de obras adicionales
def presupuestovoa(request, id):
    try:
        listam=Materiales.objects.filter(Estado="activo")
    except Materiales.DoesNotExist:
        listam=""
    try:
        pdg=  PresupuestoViviDatGen.objects.get(Id=id)
    except PresupuestoViviDatGen.DoesNotExist:
        pdg=""
    
    try:
        do= DatosObra.objects.get(IdSolicitud=pdg.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
    return render(request,"PresupuestoVApp/presupuestoobra.html", {"materiales":listam,"pdg":pdg,"do":do})


# carga los datos del material seleccionado en los inputs
def obtenermt(request):
    id=request.GET['idmaterial']
    if request.is_ajax():
        material=Materiales.objects.get(Id=id)
        serialized_data = serialize("json",[material])
        return HttpResponse(serialized_data, content_type="application/json")
    else:
       listam=Materiales.objects.filter(Estado="activo")
       return render(request,"PresupuestoVApp/presupuestoobra.html", {"materiales":listam})
    
def registrarPVObra(request): 
    
 if request.is_ajax and request.method == "POST":
    dtig =json.loads(request.POST.get('valoresig'))
    print(dtig)
    for objif in dtig:
        idp=objif['idpvo']
        fecha=objif['fechaob']
        tipoobra =objif['tipoobra']
        costoobra =objif['costooba']
        solucionsa =objif['solucionsa']
        totalobraa =objif['costott']
    
        print(fecha)
        print(tipoobra)
        print( totalobraa)
    

        idpv= PresupuestoViviDatGen.objects.get(Id=idp)
        idpv.Id=idp

        presupuestodg= PresupuestoViviDatGenObr.objects.create(Fecha=fecha,TipoObra=tipoobra,CostoObra=costoobra,SolucionSan=solucionsa,TotalObraAdi=totalobraa,IdPresupuestoViviDatGen=idpv ) #
    
        idpdg= PresupuestoViviDatGenObr.objects.all().last() #obtengo el ultimo registro de los datos generales de presupuesto
        
        ###### para tabla de materiales
        
        datamt =json.loads( request.POST.get('valorestmt'))
        print(datamt)  
        for obj in datamt:
                idmp=obj['idm'] # id del material
                cantidad=obj['cantidad']
                preciouni=obj['preciouni']
                subtotal=obj['subtotal']
                
                idm= Materiales.objects.get(Id=idmp)
                idm.Id=idmp
                
                #ma=obj['idm']
                print(cantidad)
                print(preciouni)
                print(subtotal)
            
                PreMateO = PresupuestoViviMatObr.objects.filter(IdMateriales=idm,IdPresupuestoViviDatGenObr=idpdg ).exists()
                print(PreMateO)
                #PresupuestoMateriales()
                if PreMateO== True:
                    presupuestoMateriales=PresupuestoViviMatObr.objects.get(IdMateriales=idm,IdPresupuestoViviDatGenObr=idpdg )
                
                    print(presupuestoMaterialeso.Cantidad)
                    presupuestoMaterialeso.Cantidad=presupuestoMaterialeso.Cantidad+cantidad
                    presupuestoMaterialeso.PrecioUnit=presupuestoMaterialeso.PrecioUnit+preciouni
                    presupuestoMaterialeso.SubTota=presupuestoMaterialeso.SubTota+subtotal
                    presupuestoMaterialeso.save()
                else:
                    presupuestoMaterialeso= PresupuestoViviMatObr.objects.create(Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal,IdMateriales=idm,IdPresupuestoViviDatGenObr=idpdg)
  
  ###  para tabla mano de obra
        datamo =json.loads( request.POST.get('valorestmo'))
        print(datamo)  
        for obj in datamo:
                descripcion=obj['descripc'] # id del material
                unidad=obj['unidad']
                preciouni=obj['preciouni']
                cantidad=obj['cantidad']
                subtotal=obj['subtotal']
                
                print(descripcion)
                print(cantidad)
                print(preciouni)
                print(subtotal)
            
                PreMoo = PresupuestoViviManObrObr.objects.filter(IdPresupuestoViviDatGenObr=idpdg,Descripcion=descripcion,Unidad=unidad).exists()
                print(PreMoo)

                if PreMoo== True:
                    presupuestoManoObrao=PresupuestoViviManObrObr.objects.get(IdPresupuestoViviDatGenObr=idpdg )
                
                    presupuestoManoObrao.Cantidad=presupuestoManoObrao.Cantidad+cantidad
                    presupuestoManoObrao.PrecioUnit=presupuestoManoObrao.PrecioUnit+preciouni
                    presupuestoManoObrao.SubTota=presupuestoManoObrao.SubTota+subtotal
                    presupuestoManoObrao.save()
                else:
                    presupuestoManoObrao= PresupuestoViviManObrObr.objects.create(Descripcion=descripcion,Unidad=unidad,Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal,IdPresupuestoViviDatGenObr=idpdg)
    
    mensaje="Datos guardados"
    registroBit(request, "Se registro Presupuesto Obras adicionales " + presupuestodg.IdPresupuestoViviDatGen.IdSolicitud.IdPerfil.Dui, "Registro")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=presupuestodg.IdPresupuestoViviDatGen.IdSolicitud.IdPerfil.Id)  # id de perfil  
 
def listaPVO(request,id): 
    listapo=PresupuestoViviDatGenObr.objects.filter(IdPresupuestoViviDatGen__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "PresupuestoVApp/listaPVO.html", {"listapo":listapo})

def editarPVO(request, id):# id Presupuestovdgobra
    lista_materiales_json = []
    lista_mano_obra_json = []

    try:
        pvdgo=  PresupuestoViviDatGenObr.objects.get(Id=id)
    except PresupuestoViviDatGenObr.DoesNotExist:
        pvdgo=""

    try:
        pdg=  PresupuestoViviDatGen.objects.get(Id=pvdgo.IdPresupuestoViviDatGen.Id)
    except PresupuestoViviDatGen.DoesNotExist:
        pdg=""
    
    try:
        do= DatosObra.objects.get(IdSolicitud=pdg.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do=""
  
    try:
        listam=Materiales.objects.filter(Estado="activo")
    except Materiales.DoesNotExist:
        listam=""

    try:
        lista_materiales= PresupuestoViviMatObr.objects.filter(IdPresupuestoViviDatGenObr=pvdgo.Id)
        datos=[]
        for item in lista_materiales:
            datos.append ( {'id': item.Id, 'precio':item.PrecioUnit,'cantida': item.Cantidad,'total':item.SubTota,
            "nombre":item.IdMateriales.Nombre,"descripcion":item.IdMateriales.Descripcion,"unidad":item.IdMateriales.Unidad,"idm":item.IdMateriales.Id })
        lista_materiales_json = json.dumps(datos,default=str)
    except PresupuestoViviMatObr.DoesNotExist:
        lista_materiales=""

    try:
        lista_mano_obra= PresupuestoViviManObrObr.objects.filter(IdPresupuestoViviDatGenObr=pvdgo.Id)
        datos=[]
        for item in lista_mano_obra:
            datos.append({
                "id":item.Id,
                "descripcion":item.Descripcion,
                "unidad":item.Unidad,
                "preciouni":item.PrecioUnit,
                "cantidad":item.Cantidad,
                "total":item.SubTota,
            })
            lista_mano_obra_json = json.dumps(datos, default=str)
    except PresupuestoViviManObrObr.DoesNotExist:
        lista_mano_obra=""
        lista_mano_obra_json=""

    
    return render(request,"PresupuestoVApp/editarPresupuestoObra.html", {"materiales":listam,"pvdgo":pvdgo,
                             "pdg":pdg, "do":do, "listMateriales":lista_materiales_json,
                             "lista_mano_obra_json":lista_mano_obra_json,})


def modificarPVO(request):
    if request.is_ajax and request.method == "POST":
        dtig =json.loads(request.POST.get('valoresig'))
        for objif in dtig:
            idp=objif['idpv']
            fecha=objif['fechaob']
            tipoobra =objif['tipoobra']
            costoobra =objif['costooba']
            solucionsa =objif['solucionsa']
            totalobraa =objif['costott']
            presupuesto = objif['idPresupuesto']  

            idpv= PresupuestoViviDatGen.objects.get(Id=idp)
            idpv.Id=idp
            idsol= Solicitud.objects.get(Id=idpv.IdSolicitud.Id)
            
            presupuesto = PresupuestoViviDatGenObr.objects.get(Id=presupuesto, IdPresupuestoViviDatGen=idpv.Id)

            presupuestodg= PresupuestoViviDatGenObr.objects.update_or_create(IdPresupuestoViviDatGen=idpv, Id=presupuesto.Id ,
            defaults={
                "Fecha":fecha,
                "TipoObra":tipoobra,
                "CostoObra":costoobra,
                "SolucionSan":solucionsa,
                "TotalObraAdi":totalobraa,
                "IdPresupuestoViviDatGen":idpv }) #
        
            idpdg= presupuesto #obtengo el ultimo registro de los datos generales de presupuesto
            
            ###### para tabla de materiales
            
            datamt =json.loads( request.POST.get('valorestmt'))
            lista_original = PresupuestoViviMatObr.objects.filter(
                IdPresupuestoViviDatGenObr=presupuesto.Id)
            lista_actual = []  # el id que no este aqui se eliminara
            for obj in datamt:
                    idmp=obj['idm'] # id del material
                    cantidad=obj['cantidad']
                    preciouni=obj['preciouni']
                    subtotal=obj['subtotal']
                    
                    idm= Materiales.objects.get(Id=idmp)
                    idm.Id=idmp
                    lista_actual.append(idmp) 
                    PreMate = PresupuestoViviMatObr.objects.update_or_create(IdMateriales=idm, IdPresupuestoViviDatGenObr=presupuesto.Id,
                        defaults={
                            "PrecioUnit":preciouni,
                            "Cantidad":cantidad,
                            "SubTota":subtotal,
                            "IdMateriales":idm,
                            "IdPresupuestoViviDatGenObr":idpdg,
                        })
            # ciclo para eliminar  material
            for item in lista_original:
                if ((item.IdMateriales.Id in lista_actual) == False):
                    PreMate = PresupuestoViviMatObr.objects.get(
                        IdMateriales=item.IdMateriales, IdPresupuestoViviDatGenObr=presupuesto.Id)
                    PreMate.delete()
        
    ###  para tabla mano de obra
            datamo = json.loads( request.POST.get('valorestmo'))
            lista_original = PresupuestoViviManObrObr.objects.filter(
                IdPresupuestoViviDatGenObr=presupuesto.Id)
            lista_actual = []
            for obj in datamo:
                    id =obj['id']
                    descripcion=obj['descripc'] 
                    unidad=obj['unidad']
                    preciouni=obj['preciouni']
                    cantidad=obj['cantidad']
                    subtotal=obj['subtotal']
                    
                    try: 
                        mano_obra = PresupuestoViviManObrObr.objects.update_or_create( Id=id, IdPresupuestoViviDatGenObr=presupuesto.Id,
                                defaults={
                                "Descripcion":descripcion, 
                                "Unidad":unidad, 
                                "PrecioUnit":preciouni, 
                                "Cantidad":cantidad, 
                                "SubTota":subtotal, 
                                "IdPresupuestoViviDatGenObr":presupuesto, 
                                })  
                        lista_actual.append(int(id))
                    except Exception:
                        presupuestoManoObra= PresupuestoViviManObrObr.objects.create(Descripcion=descripcion,
                                Unidad=unidad,
                                Cantidad=cantidad, 
                                PrecioUnit=preciouni, 
                                SubTota=subtotal,
                                IdPresupuestoViviDatGenObr=idpdg)  
                        lista_actual.append(presupuestoManoObra.Id)           
            # ciclo para eliminar mano de obra
            for item in lista_original:
                if ((item.Id in lista_actual) == False):
                    PreMate = PresupuestoViviManObrObr.objects.get(
                        Id=item.Id, IdPresupuestoViviDatGenObr=presupuesto.Id)
                    PreMate.delete()

            
        
    mensaje="Datos actualizados"
    registroBit(request, "Se actualizó Presupuesto de Vivienda Obras adicionales " + idsol.IdPerfil.Dui, "Actualización")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=idsol.IdPerfil.Id)  # id de perfil ")
 
