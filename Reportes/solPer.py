from fpdf import FPDF
from datetime import date
import locale
from ClienteApp.models import *
from django.http import FileResponse
from SolicitudesApp.models import *
from ClienteApp.models import Perfil
from django.db.models import Q


class solicitudPer(FPDF):
    
    def soliPer(request, ids):
        

        locale.setlocale(locale.LC_TIME, '')
        fecha=date.today()
        
        print(fecha)
        try:
            sol=Solicitud.objects.get(Id=ids)
        except Solicitud.DoesNotExist: 
            sol=""
          
        try:
            do=DatosObra.objects.get(IdSolicitud=sol.Id)
        except DatosObra.DoesNotExist: 
            do=""

        try:
            gf=GrupoFami.objects.filter(IdSolicitud=sol.Id)            
        except GrupoFami.DoesNotExist: 
            gf=""  

        try:
            dps=DatosPers.objects.get(IdSolicitud=sol.Id)
        except DatosPers.DoesNotExist: 
            dps=""

        try:
            dpf=DatosPersFia.objects.get(Q(IdSolicitud=ids) & Q(Q(Tipo ="conyuge") | Q(Tipo="codeudor")))
        except DatosPersFia.DoesNotExist: 
            dpf=""
        
        try:
            ds=Domicilio.objects.get(IdSolicitud=ids, Tipo="Solicitante")        
        except Domicilio.DoesNotExist: 
            ds=""
        
        try:
            df=Domicilio.objects.get(Q(IdSolicitud=ids) & Q(Q(Tipo ="conyuge") | Q(Tipo="codeudor")))       
        except Domicilio.DoesNotExist: 
            df=""
       
        try:            
            det=Detalle.objects.get(IdSolicitud=sol.Id)                   
        except Detalle.DoesNotExist: 
            det=""

        try:            
            ec=ExperienciaCred.objects.filter(IdSolicitud=sol.Id)                    
        except ExperienciaCred.DoesNotExist: 
            ec=""

        try:           
            rp=Referencias.objects.filter(IdSolicitud=sol.Id)                   
        except Referencias.DoesNotExist: 
            rp=""

        try:           
            com=Comentarios.objects.get(IdSolicitud=sol.Id)                    
        except Comentarios.DoesNotExist: 
            com=""

        try:
            med=Medio.objects.get(IdSolicitud=sol.Id)
        except Medio.DoesNotExist:
            med=""

 
        
        r=74
        g=96
        b=45
        aux=[0, 1, 2, 3]
        aux2=[0, 1, 2]    
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=5, y=2, w=35, h=25)#, link=url)
        

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(r,g,b)
        pdf.text(x=80, y=20, txt='SOLICITUD DE CREDITO.')
        pdf.text(x=30, y=25, txt='Para familias con ingresos provenientes de empleos y/o remesas familiares')
            
        pdf.set_font('Arial', '', 10)
        pdf.set_y(30)
        pdf.set_left_margin(10)
        pdf.cell(w=20,h=5,txt='Fecha:', border=0, align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=20,h=5,txt=fecha.strftime("%d/%m/%Y") or '', border='B', align='C', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=20,h=5,txt='Agencia:', border=0, align='R', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=50,h=5,txt=sol.IdPerfil.IdAgencia.Nombre if hasattr(sol, 'IdPerfil') else '', border='B', align='C', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=20,h=5,txt='Comunidad:', border=0, align='R', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=50,h=5,txt=sol.Comunidad if hasattr(sol, 'Comunidad') else '', border='B', align='C', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=20,h=5,txt='Municipio:', border=0, align='R', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=50,h=5,txt=sol.IdPerfil.IdDistrito.Distrito if hasattr(sol, 'IdPerfil') else '', border='B', align='C', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=15,h=5,txt='Area: ', border=0, align='R', fill=False)
        if sol.Area =="Urbana":
            pdf.cell(w=15,h=5,txt='Urbana:', border=0, align='C', fill=False)
            pdf.set_text_color(0,0,0)
            pdf.cell(w=5,h=5,txt='X', border=1, align='C', fill=False)
            pdf.set_text_color(r,g,b)
            pdf.cell(w=15,h=5,txt='Rural:', border=0, align='C', fill=False)
            pdf.multi_cell(w=5,h=5,txt='', border=1, align='C', fill=False)
        elif sol.Area == 'Rural':
            pdf.cell(w=15,h=5,txt='Urbana:', border=0, align='C', fill=False)
            pdf.cell(w=5,h=5,txt='', border=1, align='C', fill=False)
            pdf.cell(w=15,h=5,txt='Rural:', border=0, align='C', fill=False)
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(w=5,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.set_text_color(r,g,b)
            pdf.cell(w=15,h=5,txt='Urbana:', border=0, align='C', fill=False)
            pdf.cell(w=5,h=5,txt='', border=1, align='C', fill=False)
            pdf.cell(w=15,h=5,txt='Rural:', border=0, align='C', fill=False)
            pdf.multi_cell(w=5,h=5,txt='', border=1, align='C', fill=False)
        
        #pdf.cell(w=0,h=5,txt='', border='B',  align='L', ln=1, fill=0)

        pdf.set_font('Arial', '', 10)
        pdf.set_y(40)
        pdf.set_left_margin(10)
        pdf.set_fill_color(r,g,b)
        #pdf.add_page
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='', border='B',  align='L', ln=1, fill=0)
        pdf.cell(w=50,h=5,txt='Identificacion', border=1, align='C', fill=True)
        pdf.cell(w=80,h=5,txt='Solicitante', border=1, align='C', fill=True)
        pdf.multi_cell(w=0,h=5,txt='Conyuge  Codeudor', border=1,  align='C', fill=True)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Nombres', border=1, align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=sol.IdPerfil.Nombres if hasattr(sol, 'IdPerfil') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.NombreFiad if hasattr(dpf, 'NombreFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Apellidos', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=sol.IdPerfil.Apellidos if hasattr(sol, 'IdPerfil') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.ApellidoFiad if hasattr(dpf, 'ApellidoFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='DUI', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=sol.IdPerfil.Dui if hasattr(sol, 'IdPerfil') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.DuiFiad if hasattr(dpf, 'DuiFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Lugar y Fecha de Expedicion', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=(dps.LugarDuiCli  if hasattr(dps, 'LugarDuiCli') else '') +' '+(dps.FechaDuiCli.strftime("%d/%m/%Y") if hasattr(dps, 'FechaDuiCli') else '') , border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=(dpf.LugarDuiFia  if hasattr(dpf, 'LugarDuiFia') else '') +' '+ (dpf.FechaDuiFia.strftime("%d/%m/%Y") if hasattr(dpf, 'FechaDuiFia') else '' ), border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Lugar y Fecha de Nacimiento', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=(dps.LugarNaciCli if hasattr(dps, 'LugarNaciCli') else '')  +' '+(sol.IdPerfil.FechaNaci.strftime("%d/%m/%Y") if hasattr(sol, 'IdPerfil') else '') , border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=(dpf.LugarNaciFia  if hasattr(dpf, 'LugarNaciFia') else '') +' '+(dpf.FechaNaciFia.strftime("%d/%m/%Y")  if hasattr(dpf, 'FechaNaciFia') else ''), border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Edad', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=str(sol.IdPerfil.Edad) if hasattr(sol, 'IdPerfil') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=str(dpf.EdadFiad) if hasattr(dpf, 'EdadFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='NIT', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt='---------', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='---------', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Estado Civil', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=dps.EstadoCiviCli if hasattr(dps, 'EstadoCiviCli') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.EstadoCiviFiad if hasattr(dpf, 'EstadoCiviFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Genero', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=dps.GeneroClie if hasattr(dps, 'GeneroClie') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.GeneroFiad if hasattr(dpf, 'GeneroFiad') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Profesión u Oficio', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=sol.IdPerfil.IdOcupacion.Nombre if hasattr(sol, 'IdPerfil') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=dpf.ProfecionFiad if hasattr(dpf, 'ProfecionFiad') else '', border=1,  align='L', fill=0)
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Grupo Familiar', border=1, ln=1, align='C', fill=1)
        pdf.cell(w=60,h=5,txt='Nombre', border=1,  align='C', fill=1)
        pdf.cell(w=20,h=5,txt='Edad', border=1,  align='C', fill=1)
        pdf.cell(w=20,h=5,txt='Salario', border=1,  align='C', fill=1)
        pdf.cell(w=40,h=5,txt='Lugar de Trabajo', border=1,  align='C', fill=1)
        pdf.multi_cell(w=0,h=5,txt='Parentesco', border=1,  align='C', fill=1)
        pdf.set_text_color(0,0,0)
        if gf!='' and len(gf)>0:
            for i in gf:
                pdf.cell(w=60,h=5,txt=i.Nombre or '', border=1,  align='L', fill=0)
                pdf.cell(w=20,h=5,txt=str(i.Edad) or '', border=1,  align='L', fill=0)
                pdf.cell(w=20,h=5,txt=str(i.Salario) or '', border=1,  align='L', fill=0)
                pdf.cell(w=40,h=5,txt=i.Trabajo or '', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt=i.Parentesco or '', border=1,  align='L', fill=0)
        else:
            
            for i in aux:
                pdf.cell(w=60,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=20,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=20,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=40,h=5,txt='', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt='', border=1,  align='L', fill=0)
            
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Domicilio y Lugar de Trabajo', border=1, ln=1, align='C', fill=1)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Direccion actual del domicilio', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.Direccion if hasattr(ds, 'Direccion') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.Direccion if hasattr(df, 'Direccion') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Punto de refencia', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.Referencia if hasattr(ds, 'Referencia') else '', border=0,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.Referencia if hasattr(df, 'Referencia') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Telefóno', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.Telefono if hasattr(ds, 'Telefono') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.Telefono if hasattr(df, 'Telefono') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Reside desde', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.ResideDesd if hasattr(ds, 'ResideDesd') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.ResideDesd if hasattr(df, 'ResideDesd') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Condicion de la vivienda', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.CondicionVivi if hasattr(ds, 'CondicionVivi') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.CondicionVivi if hasattr(df, 'CondicionVivi') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Lugar de trabajo o negocio', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.LugarTrab if hasattr(ds, 'LugarTrab') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.LugarTrab if hasattr(df, 'LugarTrab') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Jefe inmediato', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.JefeInme if hasattr(ds, 'JefeInme') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.JefeInme if hasattr(df, 'JefeInme') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Tiempo de empleo', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=str(ds.TiempoEmprTieFun) if hasattr(ds, 'TiempoEmprTieFun') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=str(df.TiempoEmprTieFun) if hasattr(df, 'TiempoEmprTieFun') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Salario', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=str(ds.SalarioIngr) if hasattr(ds, 'SalarioIngr') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=str(df.SalarioIngr) if hasattr(df, 'SalarioIngr') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Dirección del trabajo', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.DireccionTrabMic if hasattr(ds, 'DireccionTrabMic') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.DireccionTrabMic if hasattr(df, 'DireccionTrabMic') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='Telefono del trabajo', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=ds.TelefonoTrabMic if hasattr(ds, 'TelefonoTrabMic') else '', border=1,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt=df.TelefonoTrabMic if hasattr(df, 'TelefonoTrabMic') else '', border=1,  align='L', fill=0)
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Datos de la obra a realizar', border=1, ln=1, align='C', fill=1)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Destino del credito o producto', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=do.IdAlternativa.Alternativa if hasattr(do, 'IdAlternativa') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Nombre del dueño de la propiedad', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=do.Dueno if hasattr(do, 'Dueno') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Parentesco con el solicitante', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=do.Parentesco if hasattr(do, 'Parentesco') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Direccion exacta de donde se construira', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Detalle de la obra a realizar', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=(do.IdModeloVivi.TipoVivi if hasattr(do, 'IdModeloVivi') else '')+', '+(do.DetalleAdic if hasattr(do, 'DetalleAdic') else ''), border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Presupuesto de obra', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=str(do.Presupuesto) if hasattr(do, 'Presupuesto') else '', border=1,  align='L', fill=0)
        pdf.add_page()
        #pdf.cell(w=0,h=20,txt='', border=0,  align='L', ln=1, fill=0)
        ##########
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Detalle de la solicitud', border=1, ln=1, align='C', fill=1)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Monto a solicitar', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=str(det.Monto) if hasattr(det, 'Monto') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Plazo solicitado', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=det.Plazo if hasattr(det, 'Plazo') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Cuota proyectada', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=str(det.Cuota) if hasattr(det, 'Cuota') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=10,txt='Forma de pago', border=1,  align='L', fill=0)
        pdf.set_xy(80, 30)
        if det.FormaPago=='Ventanilla':
            pdf.cell(w=30,h=10,txt='Ventanilla', border=0,  align='L', fill=0)
            pdf.set_xy(105, 32)
            pdf.cell(w=5,h=5,txt='X', border=1,  align='L', fill=0)
            pdf.set_xy(140, 30)
            pdf.cell(w=20,h=10,txt='OPI', border=0,  align='L', fill=0)
            pdf.set_xy(150, 32)
            pdf.cell(w=5,h=5,txt='', border=1,  align='L', fill=0)
            pdf.set_xy(170, 30)
            pdf.multi_cell(w=0, h=10, border='R')
        else:
            pdf.cell(w=30,h=10,txt='Ventanilla', border=0,  align='L', fill=0)
            pdf.set_xy(105, 32)
            pdf.cell(w=5,h=5,txt='', border=1,  align='L', fill=0)
            pdf.set_xy(140, 30)
            pdf.cell(w=20,h=10,txt='OPI', border=0,  align='L', fill=0)
            pdf.set_xy(150, 32)
            pdf.cell(w=5,h=5,txt='X', border=1,  align='L', fill=0)
            pdf.set_xy(170, 30)
            pdf.multi_cell(w=0, h=10, border='R')
        pdf.set_text_color(0,0,0)
        #pdf.multi_cell(w=0,h=10,txt=str(det.formaPago), border=1,  align='L', fill=0)
        pdf.set_xy(10, 40)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=70,h=5,txt='Fecha que solicita pagar', border=1,  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=str(det.FechaPago) if hasattr(det, 'FechaPago') else '', border=1,  align='L', fill=0)
        ########
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Experiencia crediticia', border=1, ln=1, align='C', fill=1)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=10,txt='Lugar', border=1,  align='C', fill=0,)
        pdf.cell(w=30,h=10,txt='Monto', border=1,  align='C', fill=0)
        pdf.multi_cell(w=30,h=5,txt='Fecha de otorgamiento', border=1,  align='C', fill=0)
        pdf.set_xy(120, 55)
        pdf.cell(w=30,h=10,txt='Estado', border=1,  align='C', fill=0)
        pdf.multi_cell(w=0,h=10,txt='Cuota que pagaba', border=1,  align='C', fill=0)
        pdf.set_text_color(0,0,0)
        
        if ec!='' and len(ec)>0:
            for i in ec:
                pdf.cell(w=50,h=5,txt=i.Lugar or '', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt=str(i.Monto) or '', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt=i.FechaOtor.strftime("%d/%m/%Y") or '', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt=i.Estado or '', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt=str(i.Cuota) or '', border=1,  align='L', fill=0)
        else:        
            for i in aux2:
                pdf.cell(w=50,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=30,h=5,txt='', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt='', border=1,  align='L', fill=0)
        ################       
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='Referencia personales y familiares', border=1, ln=1, align='C', fill=1)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=60,h=5,txt='Nombre completo', border=1,  align='C', fill=0,)
        pdf.cell(w=40,h=5,txt='Parentesco', border=1,  align='C', fill=0)
        pdf.cell(w=60,h=5,txt='Domicilio completo', border=1,  align='C', fill=0)
        pdf.multi_cell(w=0,h=5,txt='Teléfono', border=1,  align='C', fill=0)
        pdf.set_text_color(0,0,0)
        
        if rp!='' and len(rp)>0:
            for i in rp:
                pdf.cell(w=60,h=5,txt=i.Nombre or '', border=1,  align='L', fill=0)
                pdf.cell(w=40,h=5,txt=i.Parentesco or '', border=1,  align='L', fill=0)
                pdf.cell(w=60,h=5,txt=i.Domicilio or '', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt=i.Telefono or '', border=1,  align='L', fill=0)
        else:
            
            for i in aux2:
                pdf.cell(w=60,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=40,h=5,txt='', border=1,  align='L', fill=0)
                pdf.cell(w=60,h=5,txt='', border=1,  align='L', fill=0)
                pdf.multi_cell(w=0,h=5,txt='', border=1,  align='L', fill=0)
            
        ############
        
        pdf.cell(w=0,h=5,txt='', border='TB',  align='L', ln=1, fill=0)
        pdf.set_text_color(255,255,255)
        pdf.multi_cell(w=0,h=5,txt='Comentario sobre la necesidad de la vivienda o mejoramiento de vivienda', border=1, align='C', fill=1)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=15, txt=com.ComentarioNeceVivMej if hasattr(com, 'ComentarioNeceVivMej') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(255,255,255)
        pdf.multi_cell(w=0,h=5,txt='Comentario sobre la evaluación y estabilidad de los ingresos (Capacidad de pago, actividad productiva, referencias crediticias y alternativas de pago por pérdida de fuente de ingreso actual)', border=1, align='C', fill=1)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=20,txt=com.ComentarioEvalEst if hasattr(com, 'ComentarioEvalEst') else '', border=1,  align='L', fill=0)
        pdf.set_text_color(255,255,255)
        pdf.multi_cell(w=0,h=5,txt='Comentario sobre la garantía ofrecida', border=1, align='C', fill=1)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=25,txt=com.ComentarioGaraOfr if hasattr(com, 'ComentarioGaraOfr') else '', border=1,  align='L', fill=0)
        ########
        pdf.ln(3)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=5,txt='Medio por el cual se infomo del servicio crediticio de HPHES', border=0,  align='C', fill=0,)
        pdf.ln(5)
        pdf.cell(w=30,h=5,txt='Redes Sociales', border=0,  align='L', fill=0,)
        if med.RedesSoci=='Redes sociales':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=20,h=5,txt='PVV', border=0,  align='C', fill=0)
        if med.Pvv=='PVV':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=40,h=5,txt='Referenciado', border=0,  align='C', fill=0)
        if med.Referenciado=='Referenciado':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=40,h=5,txt='Perofoneo', border=0,  align='C', fill=0)
        if med.Perifoneo=='Perifoneo':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=20,h=5,txt='Radio', border=0,  align='C', fill=0)
        if med.Radio=='Radio':
            pdf.multi_cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.multi_cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=35,h=5,txt='Feria de Vivienda', border=0,  align='L', fill=0)
        if med.FeriaVivi=='Feria de Vivienda':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=50,h=5,txt='Campaña de Promocion', border=0,  align='C', fill=0)
        if med.CampanaProm=='Campaña de Promoción':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=20,h=5,txt='Otros', border=0,  align='C', fill=0)
        if med.Otros=='Otros':
            pdf.cell(w=5,h=5,txt='X', border=1,  align='C', fill=0)
        else:
            pdf.cell(w=5,h=5,txt='', border=1,  align='C', fill=0)
        pdf.cell(w=25,h=5,txt='Especifique:', border=0,  align='C', fill=0)
        pdf.multi_cell(w=0,h=5,txt=med.Especifique if hasattr(med, 'Especifique') else '', border='B',  align='C', fill=0)
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 9.5)
        pdf.multi_cell(w=0,h=5,txt='Declaro que toda la informacion contenida en en la solicitud es verdadera y autorizo a la Asociacion HPH El Salvador para que realice las investigaciones respectivas.', border=0,  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='La recepcion de la presente solicitud no significa compromiso alguno de La Asociacion con el solicitante.', border=0,  align='L', fill=0)
        
        
        pdf.line(30, 265, 90, 265)
        pdf.text(x=45, y=270, txt='Firma Solicitante ')
        pdf.line(120, 265, 180, 265)
        pdf.text(x=135, y=270, txt='Firma Codeudor ')
        
        pdf.output('solicitudPersonal.pdf', 'F')
        return FileResponse(open('solicitudPersonal.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
        #return redirect("listaSolicitud")
