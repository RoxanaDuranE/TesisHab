from django.urls import path
from SolicitudInscripcionSApp import views
from Reportes import views as viewsnat

urlpatterns = [
path('',views.solicitudI, name="solicitud"),
path('registrarDs/',views.registrarDs), 
path('listaIS/<id>', views.listaIs, name="listaIS"),
path('listaIS/editarSIS/<id>', views.editarSIS, name="editarSIS"),
path('modificarSIS/', views.modificarSIS),

path('listaIS/seguro/<id>', viewsnat.seguro, name="seguro"),

]