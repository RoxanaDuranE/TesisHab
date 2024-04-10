from django.urls import path
from EvaluacionIvEFApp import views
from NaturalApp import views as viewsN
from Reportes import views as viewsnat

urlpatterns = [
    
    path('evaluacionf/',views.evaluacionf, name="evaluacionf"),  
    path('registrarEvaluacion/',views.registrarEvaluacion), 
    path('listaEvaluacion/<id>', views.listaEvaluacion, name="listaIvE"),
    path('listaEvaluacion/editarEvaluacion/<id>', views.editarEvaluacion),
    path('listaEvaluacion/darBajaF/<id>/<idp>', views.darBajaF),
    path('modificarEvaluacion/', views.modificarEvaluacion),

    #para solicitud natural   
    path('listaEvaluacion/solicitudNatu/<idCliente>',viewsN.registrarSolicitudNatu, name="solicitudNatu"),
    # para reporte
    path('listaEvaluacion/evaluacionIvEF/<id>', viewsnat.evaluacionF, name="evaluacionIvEF"),

    #para el administrador
    path('listaEvaluacionAdmin/', views.listaEvaluacionAdmin, name="listaIvEAdmin"),
    path('agencEF/',views.agencEF),
    path('listaEvaluacionAdmin/editarEvaluacion/<id>', views.editarEvaluacion),
    # para reporte
    path('listaEvaluacionAdmin/evaluacionIvEF/<id>', viewsnat.evaluacionF, name="evaluacionIvEF"),
  
]