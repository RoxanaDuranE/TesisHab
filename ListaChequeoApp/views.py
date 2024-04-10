from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from ClienteApp.models import *
from ListaChequeoApp.models import *
from InspeccionMejViviendaApp.models import *
from InspeccionLoteApp.models import *
from PresupuestoApp.models import *
from PresupuestoVApp.models import *
from SolicitudInscripcionSApp.models import *

# Create your views here.
# para lista de chequeo
def listaPC(request): 
    listper=Perfil.objects.filter(Estado="activo")
    listSoli = Solicitud.objects.filter(Estado="Completado")
    return render(request, "ListaChequeoApp/listaPC.html", {"sol":listSoli})

def listaChequeov(request, id): # id d solicitud
    sol= ListaCheq.objects.filter(IdSolicitud=id).exists() # comprueba si en la tabla existe el registro de la solicitud
    
    if sol == True:
        try:
            idlist = ListaCheq.objects.get(IdSolicitud=id)  
        except ListaCheq.DoesNotExist:
            idlist= " " 
        return redirect('editarCheq', id=idlist.Id)

    elif sol == False:
        try:
            solic = Solicitud.objects.get(Id=id)  
        except Solicitud.DoesNotExist:
            solic= " "   
        return render(request,"ListaChequeoApp/listaChequeo.html", {"soli":solic})



# para lista de chequeo
def listaC(request): 
    listac=ListaCheq.objects.all()
    return render(request, "ListaChequeoApp/listaC.html", {"listac":listac})


def editarCheq(request, id):
    try:
        lc=  ListaCheq.objects.get(Id=id)
    except ListaCheq.DoesNotExist:
        lc=""   

    return render(request,"ListaChequeoApp/editarListaChequeo.html", {"lc":lc})

