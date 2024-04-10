from fpdf import FPDF
from datetime import date
import locale
from ClienteApp.models import *

from django.http import FileResponse
from SolicitudesApp.models import *
from django.db.models import Q
from DeclaracionJurClienteApp.models import *



class Declaracion(FPDF):
    
    def declaJur(request,id,idp):

        locale.setlocale(locale.LC_TIME, '')
        fecha=date.today()
        
        print(fecha)
        try:
            dj=DeclaracionJuraCli.objects.get(Id=id)
        except DeclaracionJuraCli.DoesNotExist:
            dj=''
        idsl=dj.IdSolicitud.Id
        try:
            sol=Solicitud.objects.get(Id=idsl)
        except Solicitud.DoesNotExist: 
            sol=''
        try:
            d=  Detalle.objects.get(IdSolicitud=idsl)
        except Detalle.DoesNotExist:
            d=""

        try:
            per=Perfil.objects.get(Id=idp)
        except Perfil.DoesNotExist:
            per=''

        try:
            djnm=  DeclaracionJiroNeg.objects.get(IdDeclaracionJuraCli=id)
        except DeclaracionJiroNeg.DoesNotExist:
            djnm=""

        try:
            dja=  DeclaracionActiEco.objects.get(IdDeclaracionJuraCli=id)
        except DeclaracionActiEco.DoesNotExist:
            dja=""
        
        
        r=0
        g=102
        b=153
        aux=[0, 1, 2, 3]
        aux2=[0, 1, 2]    
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        pdf.set_draw_color(r,g,b)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=8, y=5, w=40, h=30)#, link=url)  
        
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=0, h=30, txt='', border='TRL')
        pdf.text(x=80, y=20, txt='ASOCIACIÓN HPH EL SALVADOR.')
        pdf.text(x=80, y=25, txt='DECLARACIÓN JURADA CLIENTES')
        pdf.set_font('Arial', 'B', 10)
        pdf.set_xy(40,25)
        pdf.multi_cell(w=165,h=5,txt='(Según Acuerdo No.85, Instructivo de la Unidad de Investigacion Financiera para la prevencion de lavado de Dinero y de activos en las instituciones de Intermediación Financiera).', border=0, align='C', fill=False)    
        pdf.set_font('Arial', '', 10)
        pdf.set_y(40)
        pdf.set_left_margin(10)
        pdf.cell(w=10,h=5,txt='Yo:', border='L', align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=120,h=5,txt=(per.Nombres if hasattr(per, 'Nombres') else '') +' '+ (per.Apellidos if hasattr(per, 'Apellidos') else ''), border='B', align='L', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=5,txt='actuando en mi calidad personal y/o de ', border='R', align='L', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=125,h=4,txt='(Nombre de la Persona Natural o Representante Legal)', border='L', align='C', fill=False)
        pdf.multi_cell(w=0,h=4,txt='', border='R', align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=40,h=5,txt='Representante Legal de:', border='L', align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=150,h=5,txt='', border='B', align='L', fill=False)
        pdf.multi_cell(w=0,h=5,txt='', border='R', align='L', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=180,h=4,txt='(Nombre de la Persona o de la Empresa que Representa)', border='L', align='C', fill=False)
        pdf.multi_cell(w=0,h=4,txt='', border='R', align='C', fill=False)
        pdf.cell(w=0,h=2,txt='', border='RL',  align='L', ln=1, fill=0)
        pdf.set_font('Arial', '', 10)
        pdf.set_y(57)
        pdf.set_left_margin(10)
        pdf.set_fill_color(r,g,b)
        pdf.cell(w=0,h=4,txt='', border='RLB',  align='L', ln=1, fill=0)
        pdf.multi_cell(w=110,h=5,txt='DOCUMENTO(S) DE IDENTIFICACION DE PERSONA NATURAL O APODERADO LEGAL', border=1, align='C', fill=False)
        pdf.set_xy(120,61)
        pdf.multi_cell(w=0,h=5,txt='DOCUMENTO(s) DE IDENTIFICACION DE LA PERSONA REPRESENTADA', border=1,  align='C', fill=False)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=30,h=5,txt='Nombre:', border='TL', align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=80,h=5,txt=(per.Nombres if hasattr(per, 'Nombres') else '') +' '+ (per.Apellidos if hasattr(per, 'Apellidos') else ''), border='TR', align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=5,txt='No. NIT:', border='TLR',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=110,h=5,txt='', border='LRB',  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='', border='BLR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=25,h=10,txt='DUI NÚMERO:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=25,h=10,txt=per.Dui if hasattr(per, 'Dui') else '', border='RTB',  align='L', fill=0)
        #pdf.cell(w=80,h=5,txt='per.apellidos', border=1,  align='L', fill=0)
       
           # pdf.multi_cell(w=0, h=10, border='R')
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=40,h=10,txt='No. de Registro Fiscal:', border='TLB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=10,txt="", border='TRB',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=35,h=5,txt='NIT NÚMERO:', border='TBL',  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='TIPO DE OPERACIÓN:', border='TBL',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=dj.IdTipoOper.Nombre if hasattr(dj, 'IdTipoOper') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=20,h=5,txt='Crédito N°', border='TL',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=40,h=5,txt=dj.NumeroCred if hasattr(dj, 'NumeroCred') else '', border='TB',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=15,h=5,txt='Monto $', border='T',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=60,h=5,txt=str(d.Monto) if hasattr(d, 'Monto') else '', border='TB',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=15,h=5,txt='Plazo', border='T',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=30,h=5,txt=dj.Plazo if hasattr(dj, 'Plazo') else '', border='TB',  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(w=0,h=4,txt='(Espacio Reservado para Asociacion HPH El Salvador)', border='RL',  align='C', fill=0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=2,border='LR')
        pdf.multi_cell(w=0,h=5,txt='Declaro bajo Juramento que:', border='LR',  align='L', fill=0)
        pdf.multi_cell(w=0,h=5,txt='a) Los fondos que utilizaré para cancelar el crédito, que este día me otorga Asociación HPH El Salvador procedera de:', border='BLR',  align='L', fill=0)
        pdf.multi_cell(w=50,h=5,txt='ACTIVIDAD ECONÓMICA (PARA PERSONA NATURAL)', border='BLT',  align='L', fill=0)
        pdf.set_xy(60, 122)
        pdf.multi_cell(w=50,h=10,border='RTB')
        pdf.set_xy(110, 122)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=10,txt='GIRO DEL NEGOCIO AL QUE SE DEDICA', border='LTBR',  align='L', fill=0)
      
        pdf.set_text_color(r,g,b)
        pdf.cell(w=25,h=5,txt='-Empleado en:', border='TLB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=75,h=5,txt=dja.EmpleadoEn if hasattr(dja, 'EmpleadoEn') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=25,h=5,txt='-Empresa de: ', border='TLB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt= djnm.Empresa if hasattr(djnm, 'Empresa') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        #pdf.cell(w=50,h=5,txt='', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=50,h=5,txt='-Profesional Independiente en:', border='TLB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=50,h=5,txt=dja.ProfecionalInde if hasattr(dja, 'ProfecionalInde') else '', border='TBR',  align='L', fill=0)
        #pdf.multi_cell(w=0,h=5,txt='', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=25,h=5,txt='-Industria de:', border='TLB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt= djnm.IndustriaDe if hasattr(djnm, 'IndustriaDe') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        #pdf.multi_cell(w=0,h=5,txt='', border=1,  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=30,h=5,txt='-Conocimiento en:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=dja.ConocimientosEn if hasattr(dja, 'ConocimientosEn') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=25,h=5,txt='-Comercio de:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt= djnm.ComercioDe if hasattr(djnm, 'ComercioDe') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=30,h=5,txt='-Empresario en:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=70,h=5,txt=dja.EmpresarioEn if hasattr(dja, 'EmpresarioEn') else '', border='RTB',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=35,h=5,txt='-Otros, especifique:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=5,txt=djnm.EspecificarOtro if hasattr(djnm, 'EspecificarOtro') else '', border='TBR',  align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.cell(w=35,h=5,txt='-Otros, especifique:', border='LTB',  align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.cell(w=65,h=5,txt=dja.EspecificarOtraAct if hasattr(dja, 'EspecificarOtraAct') else '', border='TBR',  align='L', fill=0)
        pdf.multi_cell(w=0,h=5, border=1)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0,h=6,txt='b) Este crédito será cancelado de acuerdo a las cuotas y plazos establecidos por Asociacion HPH El Salvador.', border='TRL', align='C', fill=0)
        pdf.cell(w=120,h=8,txt='   c) Tengo proyectado realizar pagos adicionales a las cuotas establecidas ',border='L', align='C', fill=0)
        if dj.RealizarPagoAdi =='Si':            
            pdf.cell(w=5,h=8,txt='Si', border='',  align='C', fill=False)
            pdf.cell(w=5,h=6,txt='X', border='B',  align='C', fill=False )
            pdf.cell(w=5,h=8,txt='No', border='',  align='C', fill=False)
            pdf.cell(w=5,h=6,txt='', border='B',  align='C', fill=False)      
        else:
            pdf.cell(w=5,h=8,txt='Si', border=0,  align='C', fill=False)
            pdf.cell(w=5,h=6,txt='', border='B',  align='C', fill=False)
            pdf.cell(w=5,h=8,txt='No', border=0,  align='C', fill=False)
            pdf.cell(w=5,h=6,txt='X', border='B',  align='C', fill=False)
        pdf.multi_cell(w=0,h=8,txt=', con fondos procedentes de:',border='R', align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0,h=8,txt=dj.ProcedenciaFond if hasattr(dj, 'ProcedenciaFond') else '', border='BLR',  align='L', fill=0)
        
        pdf.set_text_color(r,g,b)
        #pdf.cell(w=60,h=5,txt='Nombre', border=1,  align='C', fill=1)
        pdf.multi_cell(w=0,h=5,txt='(Especifique procedencia de fondos de las cuotas adicionales).', border='LTR',  align='C', fill=0)
        pdf.multi_cell(w=0,h=5,txt='La informacion procedente en este instrumento, es veridica y puede ser comprobada en cualquier momento po Asociacion HPH El Salvador. Ademas pueden solicitar otros documentos para la aprobacion de fondos.', border='LR',  align='L', fill=0)
        pdf.cell(w=25,h=5,txt='Lugar y fecha:', border='L',  align='L', fill=0)
        pdf.cell(w=50,h=5, txt='',border='B', align='C', fill=0)
        pdf.cell(w=3,h=5,txt=',',border=0)
        pdf.cell(w=30,h=5,txt='',border='B')
        pdf.cell(w=8,h=5,txt=', de',border=0)
        pdf.cell(w=20,h=5,txt='',border='B')
        pdf.cell(w=8,h=5,txt='de',border=0)
        pdf.cell(w=20,h=5,txt='',border='B')
        pdf.cell(w=1,h=5,txt='',border=0)
        pdf.cell(w=10,h=5,txt='',border='B')
        pdf.multi_cell(w=0,h=5,txt=', sello.', border='R',  align='L', fill=0)
        pdf.multi_cell(w=0,h=6,txt='ESPACIO RESERVADO PARA ASOCIACIÓN HPH EL SALVADOR.', border='BLR',  align='C', fill=0)
        pdf.multi_cell(w=0,h=35,txt='', border='LTR',  align='L', fill=0)
        pdf.set_xy(85, 210)
        #pdf.cell(w=30,h=10,txt='Ventanilla', border=0,  align='L', fill=0)
        #pdf.set_xy(105, 32)
        pdf.cell(w=25,h=28,txt='', border=1,  align='L', fill=0)
        #pdf.set_xy(140, 30)
        pdf.cell(w=10,h=5,txt='', border=0,  align='L', fill=0)
        #pdf.set_xy(150, 32)
        pdf.cell(w=25,h=28,txt='', border=1,  align='L', fill=0)
        
        pdf.set_xy(10, 240)
        pdf.cell(w=25, h=5, txt='Firma Cliente:', border='L', align='L', fill=0)
        pdf.cell(w=40, h=5, txt='', border='B', align='L', fill=0)
        pdf.cell(w=9, h=5, txt='', border=0, align='L', fill=0)
        pdf.cell(w=30, h=5, txt='Pulgar Izquierdo', border=0, align='L', fill=0)
        pdf.cell(w=7, h=5, txt='', border=0, align='L', fill=0)
        pdf.cell(w=30, h=5, txt='Pulgar Derecho', border=0, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt='', border='R', align='L', fill=0)
        pdf.cell(w=20, h=5, txt='No de DUI:', border='Ls', align='L', fill=0)
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(w=0, h=5, txt=per.Dui if hasattr(per, 'Dui') else '', border='R', align='L', fill=0)
        pdf.set_text_color(r,g,b)
        pdf.multi_cell(w=0, h=7, txt='SE FIRMA ÚNICAMENTE EN PRESENCIA DE UN FUNCIONARIO DE LA ASOCIACIÓN.', border='LBR', align='C', fill=0)
                
        pdf.output('declaracionJurada.pdf', 'F')
        return FileResponse(open('declaracionJurada.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
