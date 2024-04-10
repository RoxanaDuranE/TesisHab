import json
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from DireccionApp.models import *
from django.contrib import messages
from django.http import JsonResponse

from TesisApp.views import registroBit
# Create your views here.
def depto(request):
    return render(request, "DireccionApp/depto.html")
def registrarDepto(request):
    nombre_depto=request.POST['nombre_depto'].upper()
    consulta=Departamento.objects.filter(NombreDepa=nombre_depto).exists()
 
    if consulta==True :
        mensaje="El departamento ya existe"
        messages.warning(request, mensaje)
        return redirect('/DireccionApp/listarDepto')
    else:
        depto= Departamento.objects.create(NombreDepa=nombre_depto)
        mensaje="Se ha guardado el departamento"
        registroBit(request, "Se registro departamento " + nombre_depto, "Registro")
        messages.success(request, mensaje)
        return redirect('depto')
    
#####listar depto
def listarDepto(request):
    listardepto=Departamento.objects.all()
    return render(request,"DireccionApp/listarDepto.html", {"departamento":listardepto})

### modificar depto
def modiDepto(request, id):
    departamento = Departamento.objects.get(Id=id)
    return render(request, "DireccionApp/modiDepto.html", {"Departamento":departamento})


def editDepto(request):
    id=request.POST['id']
    nombre_depto=request.POST['nombre_depto'].upper()

    depto = Departamento.objects.get(Id=id)
    depto.NombreDepa =nombre_depto
    depto.save()

    mensaje="Departamento actualizado"
    registroBit(request, "Se actualizó Departamento " + nombre_depto, "Actualización")
    messages.success(request, mensaje)
    return redirect('/DireccionApp/listarDepto')

#### para  municipios
def muni(request):
    listarde=Departamento.objects.all()
    return render(request,"DireccionApp/muni.html",{"Departamento":listarde})


def registrarMuni(request):
    nombre_muni=request.POST['nombre_muni'].upper()
    id_depto=request.POST["id_depto"]   

    depto=Departamento.objects.get(Id=id_depto)
    depto.Id=id_depto
    estado=1

    mmu=Municipio.objects.filter(NombreMuni=nombre_muni).exists()
    
    if mmu == True:
            mensaje="El municipio ya existe"
            messages.warning(request, mensaje)
    else:
            muni= Municipio.objects.create(NombreMuni=nombre_muni, IdDepartamento=depto, Estado=estado)
            
            mensaje="Se ha guardado el municipio"
            registroBit(request, "Se registro municipio" + nombre_muni, "Registro")
            messages.success(request, mensaje)
    return redirect('muni')

def mu(request):
    id=request.GET['id']
    lista_muni=[]
    muni=""
    if request.is_ajax():
        try:
            muni=Municipio.objects.filter(IdDepartamento=id)
            for item in muni:
                lista_muni.append({"id":item.Id, "nombre":item.NombreMuni})
        except Exception:
            None
        print("pasoo"+str(muni))
        serialized_data = json.dumps(lista_muni,default=str)
        #serialized_data = serialize("safe",[lista_muni])
        return HttpResponse(serialized_data, content_type="application/json")


    muni=Municipio.objects.filter(IdDepartamento=id)
    print(str(muni))
    #return render(request,"DireccionApp/mu.html", {"Muni":muni})

def listarMuni(request):
    listarmuni=Departamento.objects.all()
    return render(request,"DireccionApp/listarMuni.html", {"Departamento":listarmuni})

def modiMuni(request, idmuni):
    muni = Municipio.objects.get(Id=idmuni)
    listarde=Departamento.objects.all()
    return render(request, "DireccionApp/modiMuni.html", {"Muni":muni,"Departamento":listarde})

def editMuni(request):
    id=request.POST['id']
    nombre_muni=request.POST['nombre_muni'].upper()

    mmu=Municipio.objects.filter(NombreMuni=nombre_muni).exists()
    
    if mmu == True:
            mensaje="El municipio ya existe"
            messages.warning(request, mensaje)
    else:
            depto = Municipio.objects.get(Id=id)
            depto.NombreMuni =nombre_muni
            depto.save()

            mensaje="Municipio actualizado"
            registroBit(request, "Se actualizó municipio " + nombre_muni, "Actualización")
            messages.success(request, mensaje)
    return redirect('/DireccionApp/listarMuni')

def distrito(request):
    listarde=Departamento.objects.all()
    return render(request,"DireccionApp/distrito.html",{"Departamento":listarde})

def municipio(request):
    id=request.GET['departamento']
    depto=Departamento.objects.get(Id=id)
    depto.Id=id
    de=depto.Id
    muni=Municipio.objects.filter(IdDepartamento=depto)
    return render(request,"DireccionApp/municipio.html", {"Muni":muni})

def registrarDistri(request):
    distri=request.POST['nombre_muni'].upper()
    id=request.POST["municipio"]

    muni=Municipio.objects.get(Id=id)
    muni.Id=id
    estado=1

    mdis=Distrito.objects.filter(Distrito=distri,IdMunicipio=id).exists()
    
    if mdis == True:
            mensaje="El distrito ya existe"
            messages.warning(request, mensaje)
    else:
            muni= Distrito.objects.create(Distrito=distri, IdMunicipio=muni, Estado=estado)
            mensaje="Se ha guardado el Distrito"
            registroBit(request, "Se registro Distrito " + distri, "Registro")
            messages.success(request, mensaje)
    return redirect('distrito')

def listarDistrito(request):
    listardepto=Departamento.objects.all()
    listarmuni=Municipio.objects.all()
    ran_json = json.dumps(list(listarmuni.values()))  # Convertir la lista a JSON
    return render(request,"DireccionApp/listarDistrito.html", {"Departamento":listardepto, "ran_json": ran_json, "Muni":listarmuni})

def mun(request):
    id=request.GET['id']
    lista_distri=[]
    muni=""
    print(id)
    if request.is_ajax():
        try:
            muni=Distrito.objects.filter(IdMunicipio=id)
            for item in muni:
                lista_distri.append({"id":item.Id, "nombre":item.Distrito})
        except Exception:
            None
        print("pasoo"+str(muni))
        serialized_data = json.dumps(lista_distri,default=str)
        #serialized_data = serialize("safe",[lista_muni])
        return HttpResponse(serialized_data, content_type="application/json")

def modiDistri(request, iddistri):
    distri=Distrito.objects.get(Id=iddistri)
    idD=distri.IdMunicipio.IdDepartamento.Id
    #print(idD)
    muni = Municipio.objects.filter(IdDepartamento=idD)
    listarde=Departamento.objects.all()
    ran_json = json.dumps(list(muni.values()))
    return render(request, "DireccionApp/distritoedit.html", {"Muni":muni,"Departamento":listarde, "ran_json": ran_json, "distrito":distri})


    
def munic(request): # tenia muni
    id=request.GET['id']
    lista_muni=[]
    muni=""
    print(id)
    if request.is_ajax():
        try:
            muni=Municipio.objects.filter(IdDepartamento=id)
            for item in muni:
                lista_muni.append({"id":item.Id, "nombre":item.NombreMuni})
        except Exception:
            None
        print("pasoo"+str(muni))
        serialized_data = json.dumps(lista_muni,default=str)
        return HttpResponse(serialized_data, content_type="application/json")
    

def editDistri(request):
    id=request.POST['id']
    muni=request.POST['municipio']
    nombre_distri=request.POST['nombre_muni'].upper()

    depto = Municipio.objects.get(Id=muni)

    mdis=Distrito.objects.filter(Distrito=nombre_distri,IdMunicipio=muni).exists()
    
    if mdis == True:
            mensaje="El distrito ya existe"
            messages.warning(request, mensaje)
    else:
            distri=Distrito.objects.get(Id=id)
            distri.Distrito=nombre_distri
            distri.IdMunicipio=depto
            distri.save()

            print(id)
            mensaje="Distrito actualizado"
            registroBit(request, "Se actualizó Distrito " + distri.Distrito, "Actualización")
            messages.success(request, mensaje)
    return redirect('/DireccionApp/listarDistrito')