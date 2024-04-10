from fpdf import FPDF
from datetime import date
import locale
from termcolor import colored
from django.http import FileResponse
from ClienteApp.models import *
import locale



class perN(FPDF):
    
    def perfilesNA(request, id ):

        try:
            p=  PerfilNoApl.objects.get(Id=id)
        except PerfilNoApl.DoesNotExist:
            p=""
     
        
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()      

        pdf.set_font('Arial', 'B', 12)
        pdf.set_y(20)
        pdf.set_left_margin(20)
        pdf.cell(w=0,h=5,txt='ASOCIACIÓN HPH EL SALVADOR ', border='',  align='C', fill=False, ln=1)  
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=5,txt=p.IdAgencia.Departamento if hasattr(p, 'IdAgencia') else '', border='',  align='C', fill=False, ln=1)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=15, y=15, w=55, h=20)
        pdf.cell(w=0,h=5,txt='Datos del Solicitante que No Aplica', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=10,txt='', border='',  align='C', fill=False, ln=1)

        #pdf.cell(w=0,h=5,txt=s.fecha.strftime("%A, %d de %B de %Y"), border='', align='R', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=190,h=5,txt='Datos del Solicitante:', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=60,h=6,txt='Fecha de Registro:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.FechaRegi.strftime("%d/%m/%Y") if hasattr(p, 'FechaRegi') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='DUI:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Dui if hasattr(p, 'Dui') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Nombre del Cliente:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Nombres +' '+ p.Apellidos, border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Dirección:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Direccion if hasattr(p, 'Direccion') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Telefono if hasattr(p, 'Telefono') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Nacionalidad:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Nacionalidad if hasattr(p, 'Nacionalidad') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Fecha de Nacimiento:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Fecha.strftime("%d/%m/%Y") if hasattr(p, 'Fecha') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Edad:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=str(p.Edad) if hasattr(p, 'Edad') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Salario:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=str(p.Salario) if hasattr(p, 'Salario') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Observaciones:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=p.Observaciones if hasattr(p, 'Observaciones') else '', border=0, align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        
    
        pdf.output('perfilesNoAplican.pdf', 'F')
        return FileResponse(open('perfilesNoAplican.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
