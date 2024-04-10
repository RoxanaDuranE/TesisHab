from django.urls import path
from ListaChequeoApp import views
from Reportes import views as viewsnat

urlpatterns = [

    path('listaPC/', views.listaPC, name="listaPC"),
    path('listaPC/listaChequeov/<id>',views.listaChequeov, name="listaChequeov"),
    path('listaC/', views.listaC, name="listaC"),
    path('listaC/editarCheq/<id>',views.editarCheq, name='editarCheq'),
    # para reporte lista de chequeo
    path('listaC/listaCheq/<id>', viewsnat.listaC, name="listaCheq"),
    
]