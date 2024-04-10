from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imp
import json
import smtplib
#from inspect import _empty
#from queue import Empty
from telnetlib import LOGOUT
from typing import Any
from urllib import request
import uuid
from django import http
from django.db.models import Q
from django.template.loader import render_to_string
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View
#from django.contrib.auth.forms import UserCreationForm

#from django.contrib.auth import get_user_model
from ConfiguracionApp.models import *
from Tesis import settings
from TesisApp.models import Bitacora
from TesisApp.models import Usuario
#from django.core.files.storage import FileSystemStorage
import pytz
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect, JsonResponse
from TesisApp.forms import FormularioLogin #,FormularioUsuario

from ClienteApp.models import *
from ConfiguracionApp.models import Ocupacion, Salario
from datetime import date, datetime
from DireccionApp.models import *
from TesisApp.reset import ChangePasswordForm, ResetPasswordForm

# Create your views here.
def home(request):
    return render(request, "TesisApp/base.html")
def registroUsuario(request):
    listaragencia=Agencia.objects.all()
    return render(request, "TesisApp/registroUsuario.html",{"Agencia":listaragencia})
def iniciosession(request):
    

    return render(request, "TesisApp/iniciosession.html")

def admin():
    ag=None
    try:
        ag=Agencia.objects.all()
    except:
        ag=None
    print(ag)
    if not ag:
        print("usuario")
        agen=Agencia.objects.create(Nombre="Oficina Nacional", Direccion="Cl. Jorge Domínguez, Col. General Arce #H-4 San Salvador, El Salvador", Telefono="2510-6420", TelefonoDos="0000-0000", Departamento="San Salvador", Municipio="San Salvador Centro", Distrito="San Salvador", Estado=5)
        print("hola")
        agen=Agencia.objects.get(Estado=5)
        cont= make_password("Habitat$2023")
        usu=Usuario.objects.create(username="admin", nombre="Administrador",apellido="Admin", cargo=1, email="admin@gmial.com", password=cont, agencia=agen)
    
    

def insertar(request):
    
    nombre=request.POST['nombre']
    apellido=request.POST['apellido']
    correo=request.POST['correo']
    contra=request.POST['contra']
    id=request.POST['agencia']
    print(id)
    cargo=request.POST['cargo']
    agencia=Agencia.objects.get(Id=id)
    agencia.Id=id
    test_str=correo
    username=test_str.split('@')[0]
    cont= make_password(contra)
    usuario=Usuario.objects.create(username=username, nombre=nombre,apellido=apellido, cargo=cargo, email=correo, password=cont, agencia=agencia)
    
    mensaje="Usuario registrado"
    #registroBit(request, Actividad=mensaje, Nivel="Registro")
    messages.success(request, mensaje)
    return redirect('/')

########Empleado
def activarEmpleado(request):
    ######
    return redirect('/')
def listaEmpleados(request, id): 
    cargo_letras = {
        1: 'Administrador',
        2: 'Jefe de agencia',
        3: 'Cliente',
        4: 'Oficial de credito',
        5: 'Tecnico de construccion',
        6: 'Comite de credito',
        # Añade más mapeos según sea necesario
    }

    listUsu=Usuario.objects.filter(estado=0,agencia=id).exclude(Q(cargo=1) | Q(cargo=2) | Q(cargo=3))
    for usuario in listUsu:
       usuario.cargo = cargo_letras.get(usuario.cargo, 'Desconocido')
    return render(request, "TesisApp/listaEmpl.html", {"usuario":listUsu})

def empleadoActi(request, id):

    #fecha_actual = timezone.now().date()
    #print(fecha_actual)
   
    estad=0
    # cambia el estado del salario a inactivo
    emp= Usuario.objects.get(iduser=id, estado=0)
    emp.estado=1
    emp.save()
    

    mensaje="Empleado activado" 
    registroBit(request, Actividad=mensaje + emp.nombre +" "+ emp.apellido, Nivel="Activacion")
    messages.success(request, mensaje)
    return redirect('listaEmpleados', request.user.iduser)


def listaEmpleadosAdmin(request): #lista filtrada por agencias
    listaAg=Agencia.objects.all()
    return render(request, "ClienteApp/listaClientesAdmin.html", {"agencia":listaAg})
#######################################


class Login(FormView):
    template_name='TesisApp/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('home')
   
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs): 
        if request.user.is_authenticated:
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            admin()
            return super(Login,self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        usuar=Usuario.objects.get(username=self.request.POST['username'])
        print(usuar.agencia.Nombre)
        print(usuar.cargo)
        print(form.get_user())
        login(self.request,form.get_user())
        registroBit(self.request, Actividad="Inicio sesion", Nivel="Login")
        return super(Login,self).form_valid(form)
    
def logoutUsuario(request):
    registroBit(request, Actividad="Cierre de sesion", Nivel="Logout")
    logout(request)
    
    return HttpResponseRedirect('/accounts/login/')

def registroBit(request, Actividad, Nivel):
    usua=request.user.iduser
    fechah=datetime.now()
    fecha=fechah.strftime('%Y-%m-%d %H:%M:%S')
    print("fecha: ", fecha)
    usu=Usuario.objects.get(iduser=usua)
    bit=Bitacora.objects.create(FechaHora=fecha, Actividad=Actividad, Nivel=Nivel, IdUsuario=usu)

def listaB(request):
    usua=request.user.iduser
    bit=Bitacora.objects.filter(IdUsuario=usua).order_by('-FechaHora')
    return render(request, "TesisApp/listarBitacora.html",{"bitacora":bit})
    
def listaBitC(request):
    bit=Bitacora.objects.all()
    
def listaBita(request):
    usua=request.user.iduser
    bit=Bitacora.objects.filter(IdUsuario=usua)

def fechas(request):
    
    fini=request.GET['ini']
    ffin=request.GET['fin']
    fini=fini+' 00:'+'00:'+'00'
    ffin=ffin+' 23:'+'59:'+'59'
    lista_bit=[]
    
    print("entro")
    if request.is_ajax():
        try:
            bit=Bitacora.objects.filter(FechaHora__gte=fini, FechaHora__lte=ffin)
            #muni=Distrito.objects.filter(muni=id)
            for item in bit:
                lista_bit.append({"id":item.Id, "actividad":item.Actividad, "fecha":item.FechaHora, "tipo":item.Nivel, "usu":item.IdUsuario})
        except Exception:
            None
            print("pasoo"+str(fini))
        serialized_data = json.dumps(lista_bit,default=str)
        #serialized_data = serialize("safe",[lista_muni])
        return HttpResponse(serialized_data, content_type="application/json")
    
class ResetPasswordView(FormView):
    form_class=ResetPasswordForm
    template_name='TesisApp/resetpwd.html'
    success_url=reverse_lazy('/')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def send_email_reset_pwd(self, user): #Enviar correo
        data={}
        try:
            URL=settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer=smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            print(mailServer.ehlo())
            mailServer.starttls()
            print(mailServer.ehlo())
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print('conectado...')

            #email_to= 'duranroxa.10@gmail.com'
            email_to=user.email
            #Construimos el mensaje
            mensaje= MIMEMultipart()
            mensaje['From']= settings.EMAIL_HOST_USER
            mensaje['To']= email_to
            mensaje['Subject']= "Cambiar contraseña"

            content= render_to_string('TesisApp/send_email.html', {
                'user': user,
                'link_resetpwd':'http://{}/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))
            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
            
            print('Correo enviado correctamente')
            #messages.success(request, "Correo enviado correctamente")
        except Exception as e:
            #data['error']=str(e)
            print(e)
            #messages.error(request, str(e))
        return data

    def post(self, request,  *args, **kwargs):
        data={}
        try:
            form=ResetPasswordForm(request.POST) #self.get_form()
            if form.is_valid():
                user= form.get_user()
                #print(self.request.META['HTTP_HOST'])
                data= self.send_email_reset_pwd(user)
                messages.success(request, "Correo enviado correctamente")
            else:
                mensaje=form.errors
                messages.error(request, "Usuario invalido")
                #data['error']=form.errors
                #messages.error(request, data['error'])
                return redirect(reverse_lazy('reset_password'))
            print("Hola entro")
            print(request.POST)
            #return ResetPasswordView(request)
                
        except Exception as e:
            data['error']=str(e)
            JsonResponse(data, safe=False)
            messages.error(request, data['error'])
        return HttpResponseRedirect('/')
        
    def form_valid(self, form):
        pass
        return HttpResponseRedirect(self.success_url)
        #return super().form_valid(form)
        #super(Login,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reseteo de Contraseña"
        return context
            

class ChangePasswordView(FormView):
    form_class=ChangePasswordForm
    template_name='TesisApp/changepwd.html'
    success_url=reverse_lazy('/')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        token= self.kwargs['token']
        if Usuario.objects.filter(token=token).exists():
            print(self.kwargs['token'])
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')
    
    def post(self, request,  *args, **kwargs):
        data={}
        try:
           form= ChangePasswordForm(request.POST)
           if form.is_valid():
               user = Usuario.objects.get(token=self.kwargs['token'])
               user.set_password(request.POST['password'])
               user.token=uuid.uuid4()
               user.save()
               mensaje="Contraseña modificada"
               messages.success(request, mensaje)
               
           else:
               mensaje=form.errors
               messages.error(request, "Contraseña invalida")
               return redirect(reverse_lazy('change_password'))
               #data['error'] = form.errors
        except Exception as e:
            data['error']=str(e)
            JsonResponse(data, safe=False)
            messages.error(request, "Error: Las contraseñas deben ser validas")
            return redirect(reverse_lazy('change_password', kwargs={'token': self.kwargs['token']}))
        return HttpResponseRedirect('/')
           # messages.error(request, str(e))
            #data['error']=str(e)
        #return JsonResponse(data, safe=False)
        
    def form_valid(self, form):
        pass
        return HttpResponseRedirect(self.success_url)
        #return super().form_valid(form)
        #super(Login,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reseteo de Contraseña"
        return context
        

        

