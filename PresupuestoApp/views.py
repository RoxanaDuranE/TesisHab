import json
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import TemplateView
from PresupuestoApp.models import *
from ListaChequeoApp.models import ListaCheq
from TesisApp.views import registroBit


# Create your views here.


def presupuesto(request, id):
    sol= PresupuestoDatoGen.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True:
        solv= PresupuestoDatoGen.objects.get(IdSolicitud=id)
    
        return redirect('modPresupuesto', id=solv.Id)   
    else:
        try:
            s = Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s = ""
        try:
            do = DatosObra.objects.get(IdSolicitud=id)
        except DatosObra.DoesNotExist:
            do = ""
        
        try:
            listam = Materiales.objects.filter(Estado="activo")
        except Materiales.DoesNotExist:
            listam = ""

        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam, "s": s, "do": do})

# carga los datos del matrial seleccionado en los inputs


def get(request):
    id = request.GET['idmaterial']
    if request.is_ajax():
        material = Materiales.objects.get(Id=id)
        serialized_data = serialize("json", [material])
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})


def registrarP(request):
    # bandera= request.POST['passGN']  # guarda datos de
    # if(bandera == '1'):

    if request.is_ajax and request.method == "POST":
        dtig = json.loads(request.POST.get('valoresig'))
        print(dtig)
        for objif in dtig:
            ids = objif['ids']
            fecha = objif['fecha']
            mejorarea = objif['mejora']
            diasestimadosc = objif['diases']

            print(fecha)
            print(mejorarea)
            print(diasestimadosc)

            idsol = Solicitud.objects.get(Id=ids)
            idsol.Id = ids

            presupuestodg = PresupuestoDatoGen.objects.create(Fecha=fecha, MejoraReal=mejorarea, DiasEstiCon=diasestimadosc, IdSolicitud=idsol)
            
            # obtengo el ultimo registro de los datos generales de presupuesto
            idpdg = PresupuestoDatoGen.objects.all().last()

            # para tabla de materiales
            datamt = json.loads(request.POST.get('valorestmt'))
            print(datamt)
            for obj in datamt:
                idmp = obj['idm']  # id del material
                cantidad = obj['cantidad']
                preciouni = obj['preciouni']
                subtotal = obj['subtotal']

                idm = Materiales.objects.get(Id=idmp)
                idm.Id = idmp

                # ma=obj['idm']
                print(cantidad)
                print(preciouni)
                print(subtotal)

                PreMate = PresupuestoMate.objects.filter(
                    IdMateriales=idm, IdPresupuestoDatoGen=idpdg).exists()
                print(PreMate)
                # PresupuestoMateriales()
                if PreMate == True:
                    presupuestoMateriales = PresupuestoMate.objects.get(
                        IdMateriales=idm, IdPresupuestoDatoGen=idpdg)

                    print(presupuestoMateriales.Cantidad)
                    presupuestoMateriales.Cantidad = presupuestoMateriales.Cantidad+cantidad
                    presupuestoMateriales.PrecioUnit = presupuestoMateriales.PrecioUnit+preciouni
                    presupuestoMateriales.SubTota = presupuestoMateriales.SubTota+subtotal
                    presupuestoMateriales.save()
                else:
                    presupuestoMateriales = PresupuestoMate.objects.create(
                        Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal, IdMateriales=idm, IdPresupuestoDatoGen=idpdg)

  # para tabla mano de obra
            datamo = json.loads(request.POST.get('valorestmo'))
            print(datamo)
            for obj in datamo:
                descripcion = obj['descripc']  # id del material
                unidad = obj['unidad']
                preciouni = obj['preciouni']
                cantidad = obj['cantidad']
                subtotal = obj['subtotal']

                print(descripcion)
                print(cantidad)
                print(preciouni)
                print(subtotal)

                PreMo = PresupuestoManoObr.objects.filter(IdPresupuestoDatoGen=idpdg,Descripcion=descripcion, Unidad=unidad).exists()
                print(PreMo)

                if PreMo == True:
                    presupuestoManoObra = PresupuestoManoObr.objects.get(
                        IdPresupuestoDatoGen=idpdg)

                    presupuestoManoObra.Cantidad = presupuestoManoObra.Cantidad+cantidad
                    presupuestoManoObra.PrecioUnit = presupuestoManoObra.PrecioUnit+preciouni
                    presupuestoManoObra.SubTota = presupuestoManoObra.SubTota+subtotal
                    presupuestoManoObra.save()
                else:
                    presupuestoManoObra = PresupuestoManoObr.objects.create(
                        Descripcion=descripcion, Unidad=unidad, Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal, IdPresupuestoDatoGen=idpdg)

        # para tabla otros
            dataot = json.loads(request.POST.get('valorestot'))
            print(dataot)
            for obj in dataot:
                descripcion = obj['descripc']  # id del material
                unidad = obj['unidad']
                preciouni = obj['preciouni']
                cantidad = obj['cantidad']
                subtotal = obj['subtotal']

                print(descripcion)
                print(cantidad)
                print(preciouni)
                print(subtotal)

                PreOtr = PresupuestoOtro.objects.filter(IdPresupuestoDatoGen=idpdg,Descripcion=descripcion, Unidad=unidad).exists()

                if PreOtr == True:
                    presupuestoOtros = PresupuestoOtro.objects.get(IdPresupuestoDatoGen=idpdg)

                #    print(presupuestoMateriales.cantidad)
                    presupuestoOtros.Cantidad = presupuestoOtros.Cantidad+cantidad
                    presupuestoOtros.PrecioUnit = presupuestoOtros.PrecioUnit+preciouni
                    presupuestoOtros.SubTota = presupuestoOtros.SubTota+subtotal
                    presupuestoOtros.save()
                else:
                    presupuestoOtros = PresupuestoOtro.objects.create(
                        Descripcion=descripcion, Unidad=unidad, Cantidad=cantidad, PrecioUnit=preciouni, SubTota=subtotal, IdPresupuestoDatoGen=idpdg)

            # para otras especificaciones
            dtesp = json.loads(request.POST.get('valoresesp'))
            print(dtesp)
            for obje in dtesp:
                subtotal = obje['subtotal']
                asistenciatecn = obje['asistenciatc']
                comisionporot = obje['comisionot']
                consultabcredoto = obje['consultabc']
                cansaldopend = obje['cancelarsp']
                pcuota = obje['primerac']
                total = obje['total']
                notas = obje['notas']

                if(subtotal=="" ):
                    subtotal = 0.00  
                if(asistenciatecn=="" ):
                    asistenciatecn = 0.00  
                if(comisionporot=="" ):
                    comisionporot = 0.00  
                if(consultabcredoto=="" ):
                    consultabcredoto = 0.00  
                if(cansaldopend=="" ):
                    cansaldopend = 0.00  
                if(pcuota=="" ):
                    pcuota = 0.00  
                if(total=="" ):
                    total = 0.00  

                print(comisionporot)
                print(pcuota)
                print(notas)

                presup = Presupuesto.objects.create(SubTota=subtotal, AsistenciaTecn=asistenciatecn, ComisionPorOto=comisionporot,
                                                    ConsultaBuroCre=consultabcredoto, CancelarSaldPen=cansaldopend, PrimeraCuot=pcuota, Total=total, Notas=notas, IdPresupuestoDatoGen=idpdg)

        #####################################################
        # para guardar en la lista de chequeo 
        lchequo= ListaCheq.objects.get(IdSolicitud=idsol)
        lchequo.PresupuestoCons ="Si"
        lchequo.save()

        registroBit(request, "Se registro formulario de Presupuesto Mejora " + presupuestodg.IdSolicitud.IdPerfil.Dui, "Registro")
        # Suponiendo que quieres redirigir a una nueva página y devolver un mensaje JSON.
        response_data = {'message': 'Datos guardados correctamente.'}
        return JsonResponse(response_data)

        # Redirigir a una nueva página (modifica la URL según tu configuración)
        # redireccion = reverse('administrarPerfil', kwargs={'id': presupuestodg.ids.perfil.id})
        # return HttpResponseRedirect(redireccion)


       # mensaje = "Datos guardados"
       # messages.success(request, mensaje)
        #return redirect('administrarPerfil', id=presupuestodg.ids.perfil.id)  # id de perfil 


def modificarPresupuesto(request, id):
    lista_materiales_json = []
    lista_mano_obra_json = []
    lista_otros_json = []
    try:
        presupuesto_datos_generales = PresupuestoDatoGen.objects.get(Id=id)
    except PresupuestoDatoGen.DoesNotExist:
        presupuesto_datos_generales = ""

    try:
        pre = Presupuesto.objects.get(IdPresupuestoDatoGen=presupuesto_datos_generales.Id)
    except:
        pre = ""

    try:
        s = Solicitud.objects.get(Id=presupuesto_datos_generales.IdSolicitud.Id)
    except Solicitud.DoesNotExist:
        s = ""
    try:
        do = DatosObra.objects.get(IdSolicitud=presupuesto_datos_generales.IdSolicitud.Id)
    except DatosObra.DoesNotExist:
        do = ""
    try:
        listam = Materiales.objects.filter(Estado="activo")
    except Materiales.DoesNotExist:
        listam = ""

    try:
        lista_materiales = PresupuestoMate.objects.filter(IdPresupuestoDatoGen=presupuesto_datos_generales.Id)
        datos = []
        for item in lista_materiales:
            datos.append({'id': item.Id, 'precio': item.PrecioUnit, 'cantida': item.Cantidad, 'total': item.SubTota,
                          "nombre": item.IdMateriales.Nombre, "descripcion": item.IdMateriales.Descripcion, "unidad": item.IdMateriales.Unidad, "idm": item.IdMateriales.Id})
        lista_materiales_json = json.dumps(datos, default=str)

    except PresupuestoMate.DoesNotExist:
        None

    try:
        lista_mano_obra = PresupuestoManoObr.objects.filter(
            IdPresupuestoDatoGen=presupuesto_datos_generales.Id)
        datos = []
        for item in lista_mano_obra:
            datos.append({
                "id": item.Id,
                "descripcion": item.Descripcion,
                "unidad": item.Unidad,
                "preciouni": item.PrecioUnit,
                "cantidad": item.Cantidad,
                "total": item.SubTota,
            })
            lista_mano_obra_json = json.dumps(datos, default=str)

    except PresupuestoManoObr.DoesNotExist:
        lista_mano_obra = ""
        lista_mano_obra_json = []

    try:
        lista_otros = PresupuestoOtro.objects.filter(
            IdPresupuestoDatoGen=presupuesto_datos_generales.Id)
        datos = []
        for item in lista_otros:
            datos.append({
                "id": item.Id,
                "descripcion": item.Descripcion,
                "unidad": item.Unidad,
                "preciouni": item.PrecioUnit,
                "cantidad": item.Cantidad,
                "total": item.SubTota,
            })
            lista_otros_json = json.dumps(datos, default=str)

    except PresupuestoOtro.DoesNotExist:
        lista_otros = ""

    return render(request, "PresupuestoApp/modificaPresupuesto.html", {"materiales": listam, "s": s, "do": do,
                                                                       "datosGenerales": presupuesto_datos_generales, "pre": pre,
                                                                       "listMateriales": lista_materiales_json,
                                                                       "lista_mano_obra_json": lista_mano_obra_json,
                                                                       "lista_otros_json": lista_otros_json
                                                                       })


def actualizarPresupuesto(request):
    if request.is_ajax and request.method == "POST":
        dtig = json.loads(request.POST.get('valoresig'))
        for objif in dtig:
            ids = objif['ids']
            idPresupuestoMejora = objif['idPresupuestoMejora']
            fecha = objif['fecha']
            mejorarea = objif['mejora']
            diasestimadosc = objif['diases']
            idsol = Solicitud.objects.get(Id=ids)
            idsol.Id = ids

            presupuestodg = PresupuestoDatoGen.objects.update_or_create(IdSolicitud=idsol, Id=idPresupuestoMejora,
                                                                   defaults={
                                                                       "Fecha": fecha,
                                                                       "MejoraReal": mejorarea,
                                                                       "DiasEstiCon": diasestimadosc,
                                                                       "IdSolicitud": idsol,
                                                                   })
            # obtengo el ultimo registro de los datos generales de presupuesto
            idpdg = PresupuestoDatoGen.objects.get(Id=idPresupuestoMejora)

        # para tabla de materiales
            datamt = json.loads(request.POST.get('valorestmt'))
            lista_original = PresupuestoMate.objects.filter(
                IdPresupuestoDatoGen=idPresupuestoMejora)
            lista_actual = []  # el id que no este aqui se eliminara

            for obj in datamt:
                idmp = obj['idm']  # id del material
                cantidad = obj['cantidad']
                preciouni = obj['preciouni']
                subtotal = obj['subtotal']
                idm = Materiales.objects.get(Id=idmp)
                idm.Id = idmp
                lista_actual.append(idmp)
                PreMate = PresupuestoMate.objects.update_or_create(IdMateriales=idm, IdPresupuestoDatoGen=idPresupuestoMejora,
                                                                         defaults={
                                                                             "PrecioUnit": preciouni,
                                                                             "Cantidad": cantidad,
                                                                             "SubTota": subtotal,
                                                                             "IdMateriales": idm,
                                                                             "IdPresupuestoDatoGen": idpdg,
                                                                         })
        # ciclo para eliminar  material
            for item in lista_original:
                if ((item.IdMateriales.Id in lista_actual) == False):
                    PreMate = PresupuestoMate.objects.get(
                        IdMateriales=item.IdMateriales, IdPresupuestoDatoGen=idPresupuestoMejora)
                    PreMate.delete()

  # para tabla mano de obra
            datamo = json.loads(request.POST.get('valorestmo'))
            lista_original = PresupuestoManoObr.objects.filter(
                IdPresupuestoDatoGen=idPresupuestoMejora)
            lista_actual = []  # el id que no este aqui se eliminara
            for obj in datamo:
                id = obj['id']
                descripcion = obj['descripc']  # id del material
                unidad = obj['unidad']
                preciouni = obj['preciouni']
                cantidad = obj['cantidad']
                subtotal = obj['subtotal']

                try:

                    PreMo = PresupuestoManoObr.objects.update_or_create(Id=id, IdPresupuestoDatoGen=idPresupuestoMejora,
                                                                         defaults={
                                                                             "Descripcion": descripcion,
                                                                             "Cantidad": cantidad,
                                                                             "SubTota": subtotal,
                                                                             "Unidad": unidad,
                                                                             "PrecioUnit": preciouni,
                                                                             "IdPresupuestoDatoGen": idpdg,
                                                                         })
                    lista_actual.append(int(id))
                except Exception:
                    presupuestoManoObra = PresupuestoManoObr.objects.create(
                        Descripcion=descripcion,
                        Unidad=unidad,
                        Cantidad=cantidad,
                        PrecioUnit=preciouni,
                        SubTota=subtotal,
                        IdPresupuestoDatoGen=idpdg)
                    lista_actual.append(presupuestoManoObra.Id)
            # ciclo para eliminar  mano obra            
            for item in lista_original:
                if ((item.Id in lista_actual) == False):
                    PreMate = PresupuestoManoObr.objects.get(
                        Id=item.Id, IdPresupuestoDatoGen=idPresupuestoMejora)
                    PreMate.delete()

        # para tabla otros
            dataot = json.loads(request.POST.get('valorestot'))
            lista_original = PresupuestoOtro.objects.filter(
                IdPresupuestoDatoGen=idPresupuestoMejora)
            lista_actual = []  # el id que no este aqui se eliminara
            for obj in dataot:
                id = obj['id']
                descripcion = obj['descripc']  # id del material
                unidad = obj['unidad']
                preciouni = obj['preciouni']
                cantidad = obj['cantidad']
                subtotal = obj['subtotal']

                PreOtr = PresupuestoOtro.objects.filter(IdPresupuestoDatoGen=idpdg).exists()
                try:
                    PreOtr = PresupuestoOtro.objects.update_or_create(Id=id, IdPresupuestoDatoGen=idPresupuestoMejora,
                                                                       defaults={
                                                                           "Descripcion": descripcion,
                                                                           "Cantidad": cantidad,
                                                                           "SubTota": subtotal,
                                                                           "Unidad": unidad,
                                                                           "PrecioUnit": preciouni,
                                                                           "IdPresupuestoDatoGen": idpdg,
                                                                       })
                    lista_actual.append(int(id))
                except Exception:
                    PreOtr = PresupuestoOtro.objects.create(
                        Descripcion=descripcion,
                        Unidad=unidad,
                        Cantidad=cantidad,
                        PrecioUnit=preciouni,
                        SubTota=subtotal,
                        IdPresupuestoDatoGen=idpdg)
                    lista_actual.append( PreOtr.Id)
                    
            # ciclo para eliminar  material
            for item in lista_original:
                if ((item.Id in lista_actual) == False):
                    PreMate = PresupuestoOtro.objects.get(
                        Id=item.Id, IdPresupuestoDatoGen=idPresupuestoMejora)
                    PreMate.delete()

        # para otras especificaciones
            dtesp = json.loads(request.POST.get('valoresesp'))
            for obje in dtesp:
                subtotal = obje['subtotal']
                asistenciatecn = obje['asistenciatc']
                comisionporot = obje['comisionot']
                consultabcredoto = obje['consultabc']
                cansaldopend = obje['cancelarsp']
                pcuota = obje['primerac']
                total = obje['total']
                notas = obje['notas']

                if(subtotal=="" ):
                    subtotal = 0.00  
                if(asistenciatecn=="" ):
                    asistenciatecn = 0.00  
                if(comisionporot=="" ):
                    comisionporot = 0.00  
                if(consultabcredoto=="" ):
                    consultabcredoto = 0.00  
                if(cansaldopend=="" ):
                    cansaldopend = 0.00  
                if(pcuota=="" ):
                    pcuota = 0.00  
                if(total=="" ):
                    total = 0.00  
                    
                print(notas)
                presup = Presupuesto.objects.update_or_create(IdPresupuestoDatoGen=idPresupuestoMejora,
                    defaults={
                    "SubTota":subtotal,
                    "AsistenciaTecn":asistenciatecn,
                    "ComisionPorOto":comisionporot,
                    "ConsultaBuroCre":consultabcredoto,
                    "CancelarSaldPen":cansaldopend,
                    "PrimeraCuot":pcuota, 
                    "Total":total,
                    "Notas":notas, 
                    "IdPresupuestoDatoGen":idpdg
                    })

    mensaje = "Datos actualizados"
    registroBit(request, "Se actualizo formulario Presupuesto Mejora " + idsol.IdPerfil.Dui, "Actualizacion")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=idsol.IdPerfil.Id)  # id de perfil ")


def listaPM(request,id):
    listapm = Presupuesto.objects.filter(IdPresupuestoDatoGen__IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "PresupuestoApp/listaPM.html", {"listap": listapm})
