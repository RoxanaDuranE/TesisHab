import json
from cProfile import label
from cgitb import html
from email import message
from pyexpat import model
from time import strftime, strptime
from django.contrib.auth.hashers import make_password, check_password
from django.core.serializers import serialize
from django.shortcuts import render,redirect, HttpResponse
from ClienteApp.models import *
from ConozcaClienteApp.models import ClienteDatoGen
from ConfiguracionApp.models import *
from DeclaracionJurClienteApp.models import DeclaracionJuraCli
from ListaChequeoApp.models import ListaCheq
from PresupuestoApp.models import PresupuestoDatoGen
from SolicitudInscripcionSApp.models import SolicitudInscSeg
from PresupuestoVApp.models import PresupuestoViviDatGen,PresupuestoViviDatGenObr
from InspeccionLoteApp.models import InspeccionLote, PrimeraInspLot
from InspeccionMejViviendaApp.models import InspeccionMejo, PrimeraInspMej
from datetime import date, datetime
from HistorialApp.models import RegistroHist

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
#from UsuarioApp.serializers import UsuarioSerializers
#from rest_framework.parsers import JSONParser
from SolicitudesApp.models import DatosPersFia, Solicitud as sol, Detalle
from EvaluacionMicroApp.models import *
from EvaluacionIvEFApp.models import EgresosFami
from django.http.response import JsonResponse
from django.contrib import messages
from DireccionApp.models import *
from TesisApp.models import *
from django.db.models import Q

from TesisApp.views import registroBit

def perfil(request):
    try:
        distrito = Distrito.objects.filter(Estado=2).exists()
    except Distrito.DoesNotExist:
        distrito =""
        
    if distrito == True:
        pass  
    else:
        mensaje="Debe Asignar Distritos"
        messages.error(request, mensaje)
   
    try:
        salario = Salario.objects.filter(Estado="activo")
    except Salario.DoesNotExist:
        mensaje="Debe Registrar Salarios"
        messages.error(request, mensaje)

    try:
        listao=Ocupacion.objects.filter(Estado="activo")
    except Ocupacion.DoesNotExist:
        listao=""

    try:
        listarDepto=Departamento.objects.all()
    except Departamento.DoesNotExist:
        listarDepto=""   
    
    try:
        lper = Perfil.objects.all()
    except Perfil.DoesNotExist:
        lper=""

     # Convertir la lista a JSON
    lper_json = json.dumps(list(lper.values()), default=str)  

    return render(request,"ClienteApp/perfil.html", {"ocupaciones":listao,"Departamento":listarDepto, "lper_json": lper_json})

def perfilc(request):
    try:
        distrito = Distrito.objects.filter(Estado=2).exists()
    except Distrito.DoesNotExist:
        distrito =""
        
    if distrito == True:
        pass  
    else:
        mensaje="Debe Asignar Distritos"
        messages.error(request, mensaje)
   
    try:
        salario = Salario.objects.filter(Estado="activo")
    except Salario.DoesNotExist:
        mensaje="Debe Registrar Salarios"
        messages.error(request, mensaje)

    try:
        listao=Ocupacion.objects.filter(Estado="activo")
    except Ocupacion.DoesNotExist:
        listao=""

    try:
        listarDepto=Departamento.objects.all()
    except Departamento.DoesNotExist:
        listarDepto=""   
    
    try:
        lper = Perfil.objects.all()
    except Perfil.DoesNotExist:
        lper=""

     # Convertir la lista a JSON
    lper_json = json.dumps(list(lper.values()), default=str)  
    return render(request,"ClienteApp/perfilc.html", {"ocupaciones":listao,"Departamento":listarDepto, "lper_json": lper_json})

def registrarPerfil(request): 
  
    nombres=request.POST['nombres']
    apellidos=request.POST['apellidos']
    dui=request.POST['dui']
    telefono=request.POST['telefono']
    nacionalidad=request.POST['nacionalidad']
    fecha=request.POST['fecha']
    ocu =request.POST['ocupacion']
    salario=request.POST['salario']
    distrito=request.POST['distrito']
    direccion=request.POST['direccion']
    correo =request.POST['correo']
    contrasena=request.POST['contrasena']
    rcontrasena=request.POST['rcontrasena']
    estadosoli=1

    fe= datetime.strptime(fecha, '%Y-%m-%d')
    anio= fe.year
    mes =fe.month
    dia= fe.day

    anioa= date.today().year
    mesa= date.today().month
    diaa= date.today().day

    ed= anioa - anio

    edad= ed

    if anio >= anioa:
        mensaje="ingrese un año valido"
        messages.warning(request, mensaje)
        return redirect('/ClienteApp/')
    elif mes >= mesa  and dia > diaa:
        edad= ed-1
    else:
        edad= ed

    sal=float(salario)
    ls=Salario.objects.filter(Estado="activo")
    des=""
    for sala in ls:
        if sal>= sala.SalarioMini and sal<=sala.SalarioMaxi:
            min= sala.SalarioMini
            max=sala.SalarioMaxi
            des=sala.TipoSala
            break
        else:
            des=""
    print(des)
    try:
        vDist=Distrito.objects.filter(Id=distrito,Estado=2).exists()
    except Distrito.DoesNotExist:
        vDist =""
    

    if vDist == True:
        pass  
    else:
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)

    idocu=Ocupacion.objects.get(Id=ocu)
    idocu.Id=ocu
    
    muni=Distrito.objects.get(Id=distrito)
    muni_zona=muni.Id

   
    #########agreagado para guardar a que zona pertenece el cliente
    try:
        zona=Zona.objects.get(IdDistrito=muni_zona)
    except Zona.DoesNotExist:
        zona=""
    if zona == "":
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)       
    else:
        zona.IdDistrito=muni
        zo=zona.IdZonaAgen.IdAgencia
    #print(zo)
    #############################

    du=Perfil.objects.filter(Dui=dui).exists()
    if du == True:
        mensaje="Usted ya esta registrado"
        messages.warning(request, mensaje)
        return redirect( '/')

    elif des=="" :
        observacion="Salario fuera de los rangos establecidos"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que no cumple los requisitos de salario"
        messages.error(request, mensaje)
        return redirect('perfil')
    elif nacionalidad!="salvadoreño" :
        observacion="Nacionalidad no aceptada"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que la nacionalidad no es aceptada"
        messages.error(request, mensaje)
        return redirect('perfil')
    elif edad< 18 or edad > 65:
        observacion="Edad fuera del rango establecido"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que la edad no es aceptada"
        messages.error(request, mensaje)
        return redirect('perfil')
    elif zona == "":
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)  
        return redirect('perfil')
    else:
        esta="activo"
        cont = make_password(contrasena)
        rcont = make_password(rcontrasena)
        test_str=correo
        username=test_str.split('@')[0]
        perfil=Perfil.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,FechaNaci=fecha,Edad=edad,IdOcupacion=idocu,Salario=sal,IdDistrito=muni,Direccion=direccion,Correo=correo,Contrasena=cont,ContrasenaVeri=rcont,Estado=esta,IdAgencia=zo,EstadoSoli=estadosoli)
        registroBit(request, "Registro de perfil" + nombres + " " + apellidos + " DUI " + dui, "Registro")
        ####### Registrar cliente para que pueda iniciar sesion
        per=Perfil.objects.get(Dui=dui)
        login=Usuario.objects.create(username=username, nombre=nombres,apellido=apellidos, cargo=3, email=correo, password=cont, agencia=zo, estado=1, perfil=per)
        mensaje="Datos guardados"
        messages.success(request, mensaje)
    usua=request.user.iduser
    usu=Usuario.objects.get(iduser=usua)
    if usu.cargo==1 or usu.cargo==6:
        return redirect('listaClientesAdmin')
    else:
        return redirect('listaClientes', usu.agencia.Id)
        
    
def registrarPerfilc(request): 
  
    nombres=request.POST['nombres']
    apellidos=request.POST['apellidos']
    dui=request.POST['dui']
    telefono=request.POST['telefono']
    nacionalidad=request.POST['nacionalidad']
    fecha=request.POST['fecha']
    ocu =request.POST['ocupacion']
    salario=request.POST['salario']
    distrito=request.POST['distrito']
    direccion=request.POST['direccion']
    correo =request.POST['correo']
    contrasena=request.POST['contrasena']
    rcontrasena=request.POST['rcontrasena']
    estadosoli=1

    fe= datetime.strptime(fecha, '%Y-%m-%d')
    anio= fe.year
    mes =fe.month
    dia= fe.day

    anioa= date.today().year
    mesa= date.today().month
    diaa= date.today().day

    ed= anioa - anio

    edad= ed

    if anio >= anioa:
        mensaje="ingrese un año valido"
        messages.warning(request, mensaje)
        return redirect('/ClienteApp/')
    elif mes >= mesa  and dia > diaa:
        edad= ed-1
    else:
        edad= ed

    sal=float(salario)
    ls=Salario.objects.filter(Estado="activo")
    des=""
    for sala in ls:
        if sal == sala.SalarioMini or (sala.SalarioMini < sal < sala.SalarioMaxi) or sal == sala.SalarioMaxi:
            min= sala.SalarioMini
            max=sala.SalarioMaxi
            des=sala.TipoSala
            break
        else:
            des=""
    print(des)
    try:
        vDist=Distrito.objects.filter(Id=distrito,Estado=2).exists()
    except Distrito.DoesNotExist:
        vDist =""
    

    if vDist == True:
        pass  
    else:
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)

    idocu=Ocupacion.objects.get(Id=ocu)
    idocu.Id=ocu
    
    muni=Distrito.objects.get(Id=distrito)
    muni_zona=muni.Id

   
    #########agreagado para guardar a que zona pertenece el cliente
    try:
        zona=Zona.objects.get(IdDistrito=muni_zona)
    except Zona.DoesNotExist:
        zona=""
    if zona == "":
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)       
    else:
        zona.IdDistrito=muni
        zo=zona.IdZonaAgen.IdAgencia
    #print(zo)
    #############################

    du=Perfil.objects.filter(Dui=dui).exists()
    if du == True:
        mensaje="Usted ya esta registrado"
        messages.warning(request, mensaje)
        return redirect( '/')

    elif des=="" :
        observacion="Salario fuera de los rangos establecidos"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que no cumple los requisitos de salario"
        messages.error(request, mensaje)
        return redirect('perfilc')
    elif nacionalidad!="salvadoreño" :
        observacion="Nacionalidad no aceptada"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que la nacionalidad no es aceptada"
        messages.error(request, mensaje)
        return redirect('perfilc')
    elif edad< 18 or edad > 65:
        observacion="Edad fuera del rango establecido"
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal,Direccion=direccion,IdAgencia=zo,Observaciones=observacion)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada ya que la edad no es aceptada"
        messages.error(request, mensaje)
        return redirect('perfilc')
    elif zona == "":
        mensaje="Debe Asignar el Distritos"
        messages.error(request, mensaje)  
        return redirect('perfilc')
    else:
        esta="activo"
        cont = make_password(contrasena)
        rcont = make_password(rcontrasena)
        test_str=correo
        username=test_str.split('@')[0]
        perfil=Perfil.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,FechaNaci=fecha,Edad=edad,IdOcupacion=idocu,Salario=sal,IdDistrito=muni,Direccion=direccion,Correo=correo,Contrasena=cont,ContrasenaVeri=rcont,Estado=esta,IdAgencia=zo,EstadoSoli=estadosoli)
        #registroBit(request, "Registro de perfil" + nombres + " " + apellidos + " DUI " + dui, "Registro")
        ####### Registrar cliente para que pueda iniciar sesion
        per=Perfil.objects.get(Dui=dui)
        login=Usuario.objects.create(username=username, nombre=nombres,apellido=apellidos, cargo=3, email=correo, password=cont, agencia=zo, estado=1, perfil=per.Id)
        mensaje="Datos guardados"
        messages.success(request, mensaje)
        
        return redirect('perfilc')   


def eliminar(request, id):
    es="inactivo"
    
    per=sol.objects.filter(IdPerfil=id).exists()
    
    if(per!=True):
        perfil=  Perfil.objects.get(Id=id)
   # perfil.delete()
   
        perfil.Estado=es
        perfil.save()
        mensaje="Perfil eliminado"
        messages.success(request, mensaje)
    else:
        mensaje="El perfil tiene solicitud en proceso"
        messages.error(request, mensaje)
    
    return redirect('/ClienteApp/listaperfil')

def editarPerfil(request, id):
    perfil = Perfil.objects.get(Id=id)    
    ocupaciones = Ocupacion.objects.all()
    listarDepto=Departamento.objects.all()
    listarMuni=Municipio.objects.filter(IdDepartamento=perfil.IdDistrito.IdMunicipio.IdDepartamento.Id)
    listarDist=Distrito.objects.filter(IdMunicipio=perfil.IdDistrito.IdMunicipio.Id)
    # nombres 
    Deptop=Departamento.objects.get(Id=perfil.IdDistrito.IdMunicipio.IdDepartamento.Id)
    Munip=Municipio.objects.get(Id=perfil.IdDistrito.IdMunicipio.Id)
    Distp=Distrito.objects.get(Id=perfil.IdDistrito.Id)

    try:
        lper = Perfil.objects.all()
    except Perfil.DoesNotExist:
        lper=""

     # Convertir la lista a JSON
    lper_json = json.dumps(list(lper.values()), default=str)  

    return render(request, "ClienteApp/editarperfil.html", {"perfil":perfil,"ocupaciones":ocupaciones,"Departamento":listarDepto,"Municipios":listarMuni,"Distritos":listarDist,"Deptop":Deptop,"Munip":Munip,"Distp":Distp, "lper_json": lper_json})


def modificarPerfil(request):
    idp=request.POST['idp']
    nombres=request.POST['nombres']
    apellidos=request.POST['apellidos']
    dui=request.POST['dui']
    telefono=request.POST['telefono']
    nacionalidad=request.POST['nacionalidad']
    fecha=request.POST['fecha']
    ocu =request.POST['ocupacion']
    salario=request.POST['salario']
    distrito=request.POST['distrito']
    direccion=request.POST['direccion']
    correo =request.POST['correo']

    fe= datetime.strptime(fecha, '%Y-%m-%d')
    anio= fe.year
    mes =fe.month
    dia= fe.day

    anioa= date.today().year
    mesa= date.today().month
    diaa= date.today().day

    ed= anioa - anio

    edad= ed

    if anio >= anioa:
        mensaje="ingrese un año valido"
        messages.warning(request, mensaje)
        return redirect('/ClienteApp/')
    elif mes >= mesa  and dia > diaa:
        edad= ed-1
    else:
        edad= ed

    
    sal=float(salario)
    ls=Salario.objects.filter(Estado="activo")
    des=""
    for sala in ls:
        if sal> sala.SalarioMini and sal<sala.SalarioMaxi:
            min= sala.SalarioMini
            max=sala.SalarioMaxi
            des=sala.TipoSala   
            print(des)
            break
        else:
            des=""
            print(des)
    
    idocu=Ocupacion.objects.get(Id=ocu)
    idocu.Id=ocu
    
    muni=Distrito.objects.get(Id=distrito)
    muni_zona=muni.Id

    #########agreagado para guardar a que zona pertenece el cliente
    zona=Zona.objects.get(IdDistrito=muni_zona)
    zona.IdDistrito=muni
    zo=zona.IdZonaAgen.IdAgencia
    #############################
    
    if des=="" or nacionalidad!="salvadoreño" or edad< 18 or edad > 65:
        print(nacionalidad)
        print(edad)
       
        perfilna=PerfilNoApl.objects.create(Nombres=nombres,Apellidos=apellidos,Dui=dui,Telefono=telefono,Nacionalidad=nacionalidad,Fecha=fecha,Edad=edad,Salario=sal)
        mensaje="Lo sentimos, su solicitud no puede ser aceptada"
        messages.error(request, mensaje)
        return redirect('/ClienteApp/listaperfil/')
    else:
        test_str=correo
        username=test_str.split('@')[0]

        usuario = Perfil.objects.get(Id=idp)
        usuario.Nombres=nombres
        usuario.Apellidos=apellidos
        usuario.Telefono=telefono
        usuario.FechaNaci=fecha
        usuario.Edad=edad
        usuario.IdOcupacion=idocu 
        usuario.Salario=salario
        usuario.IdDistrito=muni 
        usuario.Direccion=direccion
        usuario.Correo=correo
        usuario.IdAgencia=zo
        usuario.save()

    mensaje="Datos de usuario actualizado "
    registroBit(request, Actividad=mensaje + usuario.Nombres +" "+ usuario.Apellidos, Nivel="Actualizacion")
    messages.success(request, mensaje)
    return redirect('administrarPerfil', id=usuario.Id)  # id de perfil 

def municipios(request):
    id=request.GET['departamento']
    depto=Departamento.objects.get(Id=id)
    depto.Id=id
    de=depto.Id
    muni=Municipio.objects.filter(IdDepartamento=depto)
    return render(request,"ClienteApp/municipio.html", {"Muni":muni})

def distri(request):    
    idmuni=request.GET['municipio']
    idmuni=Municipio.objects.get(Id=idmuni)
    destri=Distrito.objects.filter(IdMunicipio=idmuni)
    #print(' paso '+str(destri))
    return render(request,"ClienteApp/distrito.html", {"MuniDistrito":destri})

def municipio(request):
    id=request.GET['departamento']
    depto=Departamento.objects.get(Id=id)
    muni=Municipio.objects.filter(IdDepartamento=depto.Id)

    return render(request,"ClienteApp/municipio.html", { "muni":muni})

#### Listado de perfil por agencia
def listaPerfil(request): 
    listper=Perfil.objects.filter(Estado="activo")
    return render(request, "ClienteApp/listaperfil.html", {"perfil":listper})


def solicitudmMicroempresa(request, id):
    perfil = Perfil.objects.get(Id=id)
    return render(request, "ClienteApp/solicitud.html", {"Perfil":perfil})



#########################################################
def listaClienets(request, id): 
    listper=Perfil.objects.filter(Estado="activo",IdAgencia=id)
    return render(request, "ClienteApp/listaClientes.html", {"perfil":listper})

def listaClientesAdmin(request): #lista filtrada por agencias
    listaAg=Agencia.objects.all()
    return render(request, "ClienteApp/listaClientesAdmin.html", {"agencia":listaAg})

def agenc(request):
    id=request.GET['id']
    lista_agenciaC=[]
    clien=""
    if request.is_ajax():
        try:
            clien=Perfil.objects.filter(IdAgencia=id,Estado="activo")
            for item in clien:
                lista_agenciaC.append({"id":item.Id,"dui":item.Dui, "nombre":item.Nombres, "apellido":item.Apellidos,"telefono":item.Telefono, "agencia":item.IdAgencia.Nombre})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")

def administrarPerfil(request, id):
    perfil = Perfil.objects.get(Id=id)    
    ocupaciones = Ocupacion.objects.all()
   
    return render(request, "ClienteApp/administracionPerfil.html", {"perfil":perfil,"ocupaciones":ocupaciones})

def consulta_evaliacion_micro(request):    
    id = request.GET['idCliente']  
    listaId=[]
    
    if request.is_ajax():        
        try:            
            balance = BalanceSituMic.objects.get(Estado="1",IdPerfil=id)           
            egresos= EgresoFlujMic.objects.get(IdBalanceSituMic=balance)
            listaId.append(egresos.Id)             
        except Exception:           
            listaId.append("-0") 

        try:
            solicitud=sol.objects.filter(Q(IdPerfil=id) & (Q(EstadoSoli=1)  | Q(EstadoSoli=2) | Q(EstadoSoli=3)  | Q(EstadoSoli=4) | ( Q(EstadoSoli=5))) ).latest('Fecha') #obtengo la ultima solicitud por fecha 
            listaId.append(solicitud.Id)
        except Exception:
           listaId.append("-0") 
        try:
            conosca_cliente=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id ,CalidadActu="Cliente")
            listaId.append(conosca_cliente.Id)
        except Exception:
           listaId.append("-0") 
        try:
            declaracion=DeclaracionJuraCli.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(declaracion.Id)
        except Exception:
           listaId.append("-0") 
        try:
            seguro=SolicitudInscSeg.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(seguro.Id)
        except Exception:
           listaId.append("-0") 
        try:
            if(solicitud.TipoObra!="vivienda"):
                try:
                    inspeccion_mejora=InspeccionMejo.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(inspeccion_mejora.Id)
                except Exception:
                    listaId.append("-0") 
                try:
                    presupuesto=PresupuestoDatoGen.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(presupuesto.Id)
                    print(str(presupuesto.Id))
                except Exception:
                    listaId.append("-0") 
                try:
                    primeraInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="PRIMERA")
                    listaId.append(primeraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    segundaInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="SEGUNDA")
                    listaId.append(segundaInspeccion.Id) 
                except Exception:
                    listaId.append("-0")
                try:
                    terceraInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="TERCERA")
                    listaId.append(terceraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                
            else:
                try:
                    inspeccion_lote=InspeccionLote.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(inspeccion_lote.Id)   
                except Exception:
                    listaId.append("-0")  
                try:               
                    presupuesto=PresupuestoViviDatGen.objects.get(IdSolicitud=solicitud.Id)                      
                    listaId.append(presupuesto.Id)
                except Exception:
                    listaId.append("-0")             
                try:
                    primeraInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="PRIMERA")
                    listaId.append(primeraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    segundaInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="SEGUNDA")
                    listaId.append(segundaInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    terceraInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="TERCERA")
                    listaId.append(terceraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                
        except Exception:
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0")
        try:            
            lista_chequeo=ListaCheq.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(lista_chequeo.Id)
        except Exception:
           listaId.append("-0") 

        try:
            dicom=RegistroHist.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(dicom.Id)
        except Exception:
           listaId.append("-0") 

        try:
            presupuesto_obras_adicionales=PresupuestoViviDatGenObr.objects.get(IdPresupuestoViviDatGen = presupuesto.Id)
            listaId.append(presupuesto_obras_adicionales.Id)
        except Exception:
           listaId.append("-0")

        try:
            datos_fiador = DatosPersFia.objects.get(IdSolicitud=solicitud.Id )
            if(datos_fiador.Tipo == "codeudor"):
                try:
                    conosca_cliente_fiador=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id, CalidadActu="Fiador")
                    listaId.append(conosca_cliente_fiador.Id)
                except Exception:
                    listaId.append("-0")
            else:
                listaId.append("-1") 
        except Exception:
           listaId.append("-1") 
        
        listaId.append("-1") 

        print("micro  "+str(listaId)+" p= "+id)
        serialized_data = json.dumps(listaId, default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})

def consulta_evaliacion_natural(request):    
    id = request.GET['idCliente']  
    listaId=[]
    
    if request.is_ajax():        
        try:            
            egresosf = EgresosFami.objects.get(Estado="1",IdPerfil=id)   
            listaId.append(egresosf.Id)             
        except Exception:           
            listaId.append("-0") 

        try:
            solicitud=sol.objects.filter(Q(IdPerfil=id) & (Q(EstadoSoli=1)  | Q(EstadoSoli=2) | Q(EstadoSoli=3)  | Q(EstadoSoli=4) | ( Q(EstadoSoli=5))) ).latest('Fecha') #obtengo la ultima solicitud por fecha 
            listaId.append(solicitud.Id)
        except Exception:
           listaId.append("-0") 
        try:
            conosca_cliente=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id, CalidadActu="Cliente")
            listaId.append(conosca_cliente.Id)
        except Exception:
           listaId.append("-0") 
        try:
            declaracion=DeclaracionJuraCli.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(declaracion.Id)
        except Exception:
           listaId.append("-0") 
        try:
            seguro=SolicitudInscSeg.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(seguro.Id)
        except Exception:
           listaId.append("-0") 
        try:
            if(solicitud.TipoObra!="vivienda"):
                try:
                    inspeccion_mejora=InspeccionMejo.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(inspeccion_mejora.Id)
                except Exception:
                    listaId.append("-0") 
                try:
                    presupuesto=PresupuestoDatoGen.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(presupuesto.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    primeraInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="PRIMERA")
                    listaId.append(primeraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    segundaInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="SEGUNDA")
                    listaId.append(segundaInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    terceraInspeccion = PrimeraInspMej.objects.get(IdInspeccionMejo = inspeccion_mejora, NumeroInsp="TERCERA")
                    listaId.append(terceraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                 
            else:
                try:
                    inspeccion_lote=InspeccionLote.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(inspeccion_lote.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    presupuesto=PresupuestoViviDatGen.objects.get(IdSolicitud=solicitud.Id)
                    listaId.append(presupuesto.Id)
                except Exception:
                    listaId.append("-0")    
                try:
                    primeraInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="PRIMERA")
                    listaId.append(primeraInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    segundaInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="SEGUNDA")
                    listaId.append(segundaInspeccion.Id)
                except Exception:
                    listaId.append("-0")
                try:
                    terceraInspeccion = PrimeraInspLot.objects.get(IdInspeccionLote = inspeccion_lote, NumeroInsp="TERCERA")
                    listaId.append(terceraInspeccion.Id) 
                except Exception:
                    listaId.append("-0")

        except Exception:
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0") 
           listaId.append("-0")
        try:
            lista_chequeo=ListaCheq.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(lista_chequeo.Id)
        except Exception:
           listaId.append("-0") 

        try:
            dicom=RegistroHist.objects.get(IdSolicitud=solicitud.Id)
            listaId.append(dicom.Id)
        except Exception:
           listaId.append("-0") 
        
        try:
            presupuesto_obras_adicionales=PresupuestoViviDatGenObr.objects.get(IdPresupuestoViviDatGen = presupuesto.Id)
            listaId.append(presupuesto_obras_adicionales.Id)
        except Exception:
           listaId.append("-0")
        try:
            datos_fiador = DatosPersFia.objects.get(IdSolicitud=solicitud.Id)
            if(datos_fiador.Tipo == "codeudor"):
                try:
                        conosca_cliente_fiador=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id, CalidadActu="Fiador")
                        listaId.append(conosca_cliente_fiador.Id)
                except Exception:
                        listaId.append("-0")
            else:
              listaId.append("-1")   
        except Exception:
           listaId.append("-1") 

        print("nat  "+str(listaId)+" p= "+id)
        serialized_data = json.dumps(listaId, default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})

def consulta_tipo_solicitud(request):    
    id = request.GET['idCliente']
    cliente = Perfil.objects.get(Id=id)
    solicitud = "-0"
    if request.is_ajax():  
        try:
            if(cliente.EstadoSoli==2):
                solicitud=sol()
                solicitud.Tipo="micro"
                print("micro")
            if(cliente.EstadoSoli==3):
                solicitud=sol()
                solicitud.Tipo="natural" 
                print("natural")
            if(cliente.EstadoSoli >3):                        
                solicitud = sol.objects.filter(Q(IdPerfil=id) & (Q(EstadoSoli=1) | Q(EstadoSoli=2) | Q(EstadoSoli=3) | Q(EstadoSoli=4)| ( Q(EstadoSoli=5)) | Q(EstadoSoli=6)) ).latest('Fecha') #obtengo la ultima solicitud por fecha    
                solicitud.Id=solicitud.Id    
            serialized_data =  serialize("json", [ solicitud])
        except Exception: 
            serialized_data = json.dumps(solicitud, default=str)
       
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})

def obtener_historial(request):
    
    id = request.GET['idCliente']
    historial = []
    try:
        lista_solicitudes = sol.objects.filter(Q(IdPerfil=id) & Q(Q(EstadoSoli=4) | Q(EstadoSoli=6) | Q(EstadoSoli=7) | ( Q(EstadoSoli=5)) ) )##agregar 6 y 7
        datos = []
        for item in lista_solicitudes:

            try:
                monto=Detalle.objects.get(IdSolicitud=item.Id).Monto
            except Exception:
                monto=0.00

            datos.append({'id': item.Id, 'monto': monto, 'fecha': item.Fecha, 'estado': item.EstadoSoli, 'tipo': item.Tipo, 
                          'tipoObra': item.TipoObra, 'numero': item.Numero})
        historial = json.dumps(datos, default=str)
        print(historial)
        if(historial=="[]"):
            historial="-0"
    except Exception:
        historial = "-0"

    serialized_data = json.dumps(historial, default=str)
    return HttpResponse(serialized_data, content_type="application/json")

def completar_solicitud(request):
    id_cliente = request.GET['idCliente']
    completa = 'si'
    
    try:
        solicitud = sol.objects.filter(Q(IdPerfil=id_cliente) & ( Q(EstadoSoli=2)) ).latest('Fecha') #obtengo la ultima solicitud por fecha    
        if(solicitud.Tipo=="micro"):
            try:            
                balance = BalanceSituMic.objects.get(Estado="1",IdPerfil=id_cliente)           
                egresos= EgresoFlujMic.objects.get(IdBalanceSituMic=balance)
                            
            except Exception:           
                completa = completa+"evaluacion,&10;"
        else:
            try:            
                egresosf = EgresosFami.objects.get(Estado="1",IdPerfil=id_cliente)   
                       
            except Exception:           
                ompleta = completa+"evaluacion,&10;"
      
        try:
            conosca_cliente=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id, CalidadActu="Cliente")
        except Exception:
           completa = completa+"Conozca a su cliente,&10;"
        try:
            datos_fiador = DatosPersFia.objects.get(IdSolicitud=solicitud.Id)
            if(datos_fiador.Tipo == "codeudor"):
                try:
                        conosca_cliente_fiador=ClienteDatoGen.objects.get(IdSolicitud=solicitud.Id, CalidadActu="Fiador")
                        
                except Exception:
                         completa = completa+"Conozca a su cliente-fiador,&10;"
            
        except Exception:
           completa = completa
        try:
            declaracion=DeclaracionJuraCli.objects.get(IdSolicitud=solicitud.Id)      
        except Exception:
            completa = completa+"Declaracion jurada,&10;"

        try:
            seguro=SolicitudInscSeg.objects.get(IdSolicitud=solicitud.Id)        
        except Exception:
           completa = completa+"Inscripcion de seguro,&10;"
        
        if(solicitud.TipoObra!="vivienda"):
                try:
                    inspeccion_mejora=InspeccionMejo.objects.get(IdSolicitud=solicitud.Id)
                except Exception:
                    completa = completa+"Inspeccion mejora,&10;"

                try:
                    presupuesto=PresupuestoDatoGen.objects.get(IdSolicitud=solicitud.Id)                  
                except Exception:
                    completa = completa+"Presupuesto,&10;"
        else:                        
                try:
                   inspeccion_lote=InspeccionLote.objects.get(IdSolicitud=solicitud.Id)                   
                except Exception:
                    completa = completa+"Inspeccion vivienda,&10;"
              
                try:
                    presupuesto=PresupuestoViviDatGen.objects.get(IdSolicitud=solicitud.Id)
                except Exception:
                    completa = completa+"Presupuesto,&10;"
        
        try:
            lista_chrequeo=ListaCheq.objects.get(IdSolicitud=solicitud.Id, Estado="completo")           
        except Exception:
           completa = completa+"Lista de Chequeo,&10;"

        try:
            dicom=RegistroHist.objects.get(IdSolicitud=solicitud.Id)      
        except Exception:
           completa = completa+"DICOM,&10;"

        if (solicitud.EstadoSoli == 3):
            completa = "Completada"
        print(completa)
    except Exception:
        completa="-0"
    print(completa)
   
    serialized_data = json.dumps(completa, default=str)
    return HttpResponse(serialized_data, content_type="application/json")

def consultar_documentos(id):
    completa = "si"

    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="fotocdui")
    except Exception:
        completa="DUI"  
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="aguaDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="luzDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="constanciaEmpDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="duifDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="aguafDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="luzfDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="constEmpDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="referenciasCreDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="referenciasCrefDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="certificacionEstracDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="fotocopiaEscritDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = DocumentosClie.objects.get(IdSolicitud=id, NombreDocu="informeDICOMDoc")
    except Exception:
        completa="DUI" 
    try:        
        doc = ListaCheq.objects.get(IdSolicitud=id, Estado="completo")
    except Exception:
        completa="Lista chequeo incompleta" 


    return completa  

def completar_solicitud_base(request):
    id = request.GET['idCliente']
    bandera="si"
    try:
        perfil = Perfil.objects.get(Id= id)
        perfil.EstadoSoli=11
        perfil.save()

        #solicitud = sol.objects.filter(Q(IdPerfil=id) & (Q(EstadoSoli=4) | Q(EstadoSoli=6) | Q(EstadoSoli=3)) ).latest('Fecha') 
        solicitud = sol.objects.filter(Q(IdPerfil=id) & ( Q(EstadoSoli=2) | ( Q(EstadoSoli=5))) ).latest('Fecha') #obtengo la ultima solicitud por fecha  
        solicitud.EstadoSoli=3
        solicitud.save()
    except Exception: 
     bandera="-0"
    
    serialized_data = json.dumps(bandera, default=str)
    return HttpResponse(serialized_data, content_type="application/json")

def denegar_solicitud(request):
    id = request.GET['idSoli']
    bandera="si"
    try:       
        
        solicitud = sol.objects.get(Id = id) #obtengo la ultima solicitud por fecha  
        solicitud.EstadoSoli=6
        solicitud.Observaciones="La solicitud no se completo en el plazo de 30 dias"
        solicitud.save()

        perfil = Perfil.objects.get(Id= solicitud.IdPerfil.Id)
        perfil.EstadoSoli=1
        perfil.save()

        if(solicitud.Tipo == "micro"):                       
            balance = BalanceSituMic.objects.get(Estado="1",IdPerfil=perfil.Id)           
            balance.Estado=2
            balance.save()    
                
        else:
            egresosf = EgresosFami.objects.get(Estado="1",IdPerfil=perfil.Id)   
            egresosf.Estado=2
            egresosf.save()

    except Exception: 
        bandera="-0"
    
    serialized_data = json.dumps(bandera, default=str)
    return HttpResponse(serialized_data, content_type="application/json")

def Registrar_documento(request):    
    id = request.GET['idCliente']
    fecha = request.GET['fecha']
    if 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
    else:
        archivo = None 

    nombreD = request.GET['nombreD']
    ids = request.GET['ids']

    idsoli=sol.objects.get(Id=ids, IdPerfil=id)
    print(str(idsoli))
    print(nombreD)
    bandera= "paso"

    if request.is_ajax():     
        
        try:  
            documento, creado = DocumentosClie.objects.update_or_create(NombreDocu=nombreD,IdSolicitud=idsoli, defaults={
                "Fecha":fecha,
                "Archivo":archivo,
                "NombreDocu":nombreD,
                "IdSolicitud":idsoli
            }) 
            print(documento)
            print(creado)
            if creado:
                
                registroBit(request, Actividad="Se guardo archivo "+nombreD, Nivel="Registro")
            else:
                registroBit(request, Actividad="Se guardo archivo "+nombreD, Nivel="Actualizacion")
            ##############################
            # para guardar en la lista de chequeo  
            
            try:
                doc=DocumentosClie.objects.filter(IdSolicitud=idsoli)  
            except:
                doc=''
            #refe= DatosPersonalesF.objects.get(idSolicitud=idsoli, tipo='codeudor').exists()
            try:
                codeudor =  DatosPersFia.objects.get(IdSolicitud=idsoli, Tipo='codeudor')
                # Tu código para manejar el caso en que el codeudor existe
                codeudor=True
            except DatosPersFia.DoesNotExist:
                codeudor=False
            #print(codeudor)
            duic=0
            rec=0
            ref=0
            print("refe"+ str(codeudor))
            for d in doc: 
                             
                if d.NombreDocu == "duiDoc":
                    print(d.NombreDocu + ' refe' + str(codeudor)) 
                    duic=1
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.FotocopiaDui ="Si"
                    lchequo.save()
                if d.NombreDocu == "nitDoc" and duic==1:
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.FotocopiaDui ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "aguaDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.RecibosAgua ="Si"
                    lchequo.save()
                    
                if d.NombreDocu == "luzDoc" :
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.RecibosLuz ="Si"
                    lchequo.save()

                if d.NombreDocu == "telDoc" :
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.RecibosTele ="Si"
                    lchequo.save()

                if d.NombreDocu == "referenciasCreDoc" :
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.ReferenciaCred ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "constanciaEmpDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.ConstanciaEmpl ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "tacoIsssDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.TacoIsss ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "analisisEcNDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.AnalisisEcon ="Si"
                    lchequo.save()

                if d.NombreDocu == "balanceDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.Balance ="Si"
                    lchequo.save()
                                
                if d.NombreDocu == "balanceResDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.BalanceResu ="Si"
                    lchequo.save()

                if codeudor==True:#Documentos fiador
                    if d.NombreDocu == "duifDoc" :
                        duif=1
                        lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                        lchequo.CopiaDuiFia ="Si"
                        lchequo.save()
                    if d.NombreDocu == "nitfDoc" and duif==1:
                        lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                        lchequo.CopiaDuiFia ="Si"
                        lchequo.save()

                    if d.NombreDocu == "aguafDoc":                      
                        lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                        lchequo.RecibosAguaFia ="Si"
                        lchequo.save()

                    if d.NombreDocu == "luzfDoc":
                        lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                        lchequo.RecibosLuzFia ="Si"
                        lchequo.save()
     
                    if d.NombreDocu == "constEmpDoc" or d.NombreDocu == "analisisEcNDoc":
                        lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                        lchequo.ConstanciaEmplFia ="Si"
                        lchequo.save()


                if d.NombreDocu == "referenciasCrefDoc" :
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.ReferenciaCredFia ="Si"
                    lchequo.save()

                
                if d.NombreDocu == "inspeccionTecDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.InspeccionTecn ="Si"
                    lchequo.save()

                if d.NombreDocu == "presupuestoConsDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.PresupuestoCons ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "certificacionEstracDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.CertificadoExtr ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "carenciaBienDoc" :
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.CarenciaBien ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "fotocopiaEscritDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.FotocopiaEscr ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "declaracionSalDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.DeclaracionSalu ="Si"
                    lchequo.save()

                if d.NombreDocu == "informeDICOMDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.InformeDico ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "documentosSopDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.DocumentoSopoIng ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "documentosRemDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.DocumentoReme ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "cancelacionPresDoc" or d.NombreDocu == "estadoCuenDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.CancelacionesPresEst ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "finiquitosDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.Finiquitos ="Si"
                    lchequo.save()

                if d.NombreDocu == "hojaAprobCredDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.HojaAproCre ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "cartaElabMutDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.CartaElabMut ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "reciboPagPrimDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.ReciboPagoPri ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "ordenDesIrrevDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.OrdenDeseIrr ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "permisoConsDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.PermisoCons ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "cartaEntrCostDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.CartaEntrCosdes ="Si"
                    lchequo.save()
                
                if d.NombreDocu == "fotocopiaMutHipDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.FotocopiaMutu ="Si"
                    lchequo.save()

                if d.NombreDocu == "gestionesCobrDoc":
                    lchequo= ListaCheq.objects.get(IdSolicitud=idsoli)
                    lchequo.GestionCobr ="Si"
                    lchequo.save()

            clistaCq= ListaCheq.objects.get(IdSolicitud=idsoli)
            if clistaCq.SolicitudCred=="Si" and  clistaCq.FotocopiaDui=="Si" and  clistaCq.RecibosAgua=="Si" and  clistaCq.RecibosLuz=="Si"  and clistaCq.ConstanciaEmpl=="Si" or clistaCq.AnalisisEcon=="Si"  or  clistaCq.Balance=="Si" or  clistaCq.BalanceResu=="Si" and  clistaCq.CopiaDuiFia=="Si" and  clistaCq.RecibosAguaFia=="Si" and  clistaCq.RecibosLuzFia=="Si" and  clistaCq.ConstanciaEmplFia=="Si" and  clistaCq.ReferenciaCredFia=="Si" and  clistaCq.InspeccionTecn=="Si" and  clistaCq.PresupuestoCons=="Si" and  clistaCq.CertificadoExtr=="Si" and  clistaCq.FotocopiaEscr=="Si" and  clistaCq.DeclaracionSalu=="Si" and  clistaCq.InformeDico=="Si" :
                clistaCq.Estado="completo"
                clistaCq.save()

                    
            serialized_data = json.dumps(bandera, default=str)
        except Exception:           
            bandera = "-0"
            serialized_data = json.dumps(bandera, default=str)
        print(bandera)  
        return HttpResponse(serialized_data, content_type="application/json")
    else:
        listam = Materiales.objects.filter(Estado="activo")
        return render(request, "PresupuestoApp/presupuesto.html", {"materiales": listam})
    

#########################################################
# Listado de perfil que no aplican
def listaPerfilNA(request, id): 
    listper=PerfilNoApl.objects.filter(IdAgencia=id)
    return render(request, "ClienteApp/listaperfilNA.html", {"perfil":listper})

def listaPerfilNAAdmin(request): 
    listaAg=Agencia.objects.all()
    return render(request, "ClienteApp/listaperfilNAAdmin.html", {"agencia":listaAg})

def agencNA(request):
    id=request.GET['id']
    lista_agenciaC=[]
    clien=""
    if request.is_ajax():
        try:
            clien=PerfilNoApl.objects.filter(IdAgencia=id)
            for item in clien:
                lista_agenciaC.append({"id":item.Id,"dui":item.Dui, "nombre":item.Nombres, "apellido":item.Apellidos,"telefono":item.Telefono, "agencia":item.IdAgencia.Nombre,"observaciones":item.Observaciones})
        except Exception:
            None
        serialized_data = json.dumps(lista_agenciaC,default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    
   