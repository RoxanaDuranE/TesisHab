from django.urls import path
from NaturalApp import views
from ConozcaClienteApp import views as viewscca
from SolicitudInscripcionSApp import views as viewssia
from DeclaracionJurClienteApp import views as viewsdjca
from SolicitudesApp import views as viewsS
from Reportes import views as viewsnat
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
     path('solicitudNatural/', views.registrarSolicitudNatu, name='solicitudNatural'),
     path('registrarDatosN/', views.registroSolicitudN),
     path('listarSN/',views.listarSN, name="listarSN"),  
     path('listarSNC',views.listarSNC, name="listarSNC"),
     path('listarSNCA/<id>', views.listarSNCA, name="listarSNCA"),
     path('listarSN/editarSolicitudN/<idSolicitud>',views.editarSolicitudN),
     path('modDatosNatural/', views.modSoliNatural),

     # para los reportes de formulario de comite de credito y hoja de pre-aprobacion
    path('listaRFN/<id>', views.listaRF, name="listaRFN"),
    # para reporte formulario de comite de credito
    path('listaRFN/formularioCN/<id>', viewsnat.formComiteCN, name="formularioCN"),
    # para reporte hoja de pre-aprobacion
    path('listaRFN/hojaPN/<id>', viewsnat.hojaPreAprobacionN, name="hojaPN"),

     # para los reportes de formulario de comite de credito y hoja de pre-aprobacion Admin
    path('listaRFNAdmin/', views.listaRFAdmin, name="listaRFNAdmin"),
    path('agencRFA/',views.agencRFA),
    # para reporte formulario de comite de credito
    path('listaRFNAdmin/formularioCN/<id>', viewsnat.formComiteCN, name="formularioCN"),
    # para reporte hoja de pre-aprobacion
    path('listaRFNAdmin/hojaPN/<id>', viewsnat.hojaPreAprobacionN, name="hojaPN"),
     
     
     # reporte solicitud   
    path('listarSNC/soliPer/<ids>', login_required(viewsnat.SolicitudPe), name="soliPer"),
        
     # para canozca a su cliente
    path('listarSNC/ccliente/<id>', login_required(viewscca.ccliente)),

     # para Solicitud de incripcion al seguro
    path('listarSNC/solicitudI/<id>', login_required(viewssia.solicitudI)),

     # para Declaración Jurada cliente
    path('listarSNC/declaracionjc/<id>', login_required(viewsdjca.declaracionjc)),

     # para  solicitudes pendientes de aprobacion
    path('listaSolicitudesPA/<id>', views.listaSolicitudesPA, name="listaSolicitudesPAN"),
    # reporte de solicitudes pendientes de aprobacion
    path('listaSolicitudesPA/solP/<id>', viewsnat.solicPA, name="solP"), 
    path('listaSolicitudesPA/evaluarSol/<id>', viewsS.evaluarSol),
    #path('registrarEvaluacion/', views.registrarEvaluacion),

    # para  solicitudes pendientes de aprobacion Administrador
    path('listaSolicitudesPAAdmin/', views.listaSolicitudesPAAdmin, name="listaSolicitudesPANAdmin"),
    path('agencPAA/',views.agencPAA),
    # reporte de solicitudes pendientes de aprobacion
    path('listaSolicitudesPAAdmin/solP/<id>', viewsnat.solicPA, name="solP"), 
    path('listaSolicitudesPAAdmin/evaluarSol/<id>', viewsS.evaluarSol),
    #path('registrarEvaluacion/', views.registrarEvaluacion),

    # para  solicitudes aprobadas
    path('listaSolicitudesApr/<id>', views.listaSolicitudesApr, name="listaSolicitudesAN"),
    # reporte de solicitudes aprobadas
    path('listaSolicitudesApr/formularioCN/<id>', viewsnat.formComiteCN, name="formularioCN"),
    path('listaSolicitudesApr/evaluarSolApr/<id>', viewsS.evaluarSolApr),

    # para  solicitudes aprobadas admin
    path('listaSolicitudesAprAdmin/', views.listaSolicitudesAprAdmin, name="listaSolicitudesANAdmin"),
    path('agencAA/',views.agencAA),
    # reporte de solicitudes aprobadas
    path('listaSolicitudesAprAdmin/formularioCN/<id>', viewsnat.formComiteCN, name="formularioCN"),
    path('listaSolicitudesAprAdmin/evaluarSolApr/<id>', viewsS.evaluarSolApr),

    # para  solicitudes observadas
    path('listaSolicitudesObs/<id>', views.listaSolicitudesObs, name="listaSolicitudesObsN"),
    # reporte de solicitudes observadas
    path('listaSolicitudesObs/solObs/<id>', viewsnat.solicObs, name="solObs"), 
    path('listaSolicitudesObs/evaluarSolObs/<id>', viewsS.evaluarSolObs),
    path('modificarEvaluacion/', viewsS.modificarEvaluacion),

    # para  solicitudes observadas Admin
    path('listaSolicitudesObsAdmin/', views.listaSolicitudesObsAdmin, name="listaSolicitudesObsNAdmin"),
    path('agencOA/',views.agencOA),
    # reporte de solicitudes observadas
    path('listaSolicitudesObsAdmin/solObs/<id>', viewsnat.solicObs, name="solObs"), 
    path('listaSolicitudesObsAdmin/evaluarSolObs/<id>', viewsS.evaluarSolObs),
    path('modificarEvaluacion/', viewsS.modificarEvaluacion),

    # para  solicitudes denegadas
    path('listaSolicitudesDen/<id>', views.listaSolicitudesDen, name="listaSolicitudesDenN"),
    # reporte de solicitudes denegadas
    path('listaSolicitudesDen/solDen/<id>', viewsnat.solicDen, name="solDen"), 
    path('listaSolicitudesDen/evaluarSolDen/<id>', viewsS.evaluarSolDen),

    # para  solicitudes denegadas Admin
    path('listaSolicitudesDenAdmin/', views.listaSolicitudesDenAdmin, name="listaSolicitudesDenNAdmin"),
    path('agencDA/',views.agencDA),
    # reporte de solicitudes denegadas
    path('listaSolicitudesDenAdmin/solDen/<id>', viewsnat.solicDen, name="solDen"), 
    path('listaSolicitudesDenAdmin/evaluarSolDen/<id>', viewsS.evaluarSolDen),

    path('obtenerRangoNat/' ,views.obtenerRangoNat, name='obtenerRangoNat'),
     

]