from fpdf import FPDF
from datetime import date
import locale
from termcolor import colored
from django.http import FileResponse
from InspeccionMejViviendaApp.models import *
from PresupuestoVApp.models import *


class pinspmu(FPDF):
    
    def pInspeccionMU(request, id ):
        try:
            pim=PrimeraInspMej.objects.get(Id=id)
        except PrimeraInspMej.DoesNotExist:
            pim=""
        try:
            inspeccionm=InspeccionMejo.objects.get(Id=pim.IdInspeccionMejo.Id)
        except InspeccionMejo.DoesNotExist:
            inspeccionm=""
        try:
            do= DatosObra.objects.get(IdSolicitud=inspeccionm.IdSolicitud.Id)
        except DatosObra.DoesNotExist:
            do=""    
        try:
            DMipm = DescripcionMejoInsMej.objects.get(IdInspeccionMejo=inspeccionm.Id)
        except DescripcionMejoInsMej.DoesNotExist:
            DMipm=""   


        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
   
        #Margenes de la pagina
        pdf.rect(10, 55,196,177)
        pdf.set_line_width(0.1)  
        
        try:  
            # Agregar la imagen desde la instancia pil
            img_path = pim.Esquema.path  # Asumiendo que es un campo FileField o ImageField
            x = 11  # Coordenada horizontal 
            y = 70  # Coordenada vertical... arriba
            w = 194 # Ancho de la imagen en puntos
            h = 127  # Altura de la imagen en puntos
            pdf.image(img_path , x=x, y=y, w=w, h=h)
        except:
            pass

        pdf.image('TesisApp/static/TesisApp/images/logohabitat.jpg', x=20, y=4, w=40, h=25)    
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=65,h=9,txt='', border=0, align='C', fill=False)
        pdf.cell(w=0,h=9,txt=pim.NumeroInsp + ' INSPECCIÓN', border=1,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=7,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.text(x=15, y=60, txt='UBICACIÓN DEL MEJORAMIENTO ')

        pdf.set_font('Arial', '', 10)
        pdf.set_fill_color(166,166,166)
        pdf.cell(w=65,h=6,txt='Nombre del Cliente:', border=1, align='C', fill=True)
        pdf.cell(w=50,h=6,txt='Municipio del mejoramiento:', border=1, align='C', fill=True)
        pdf.cell(w=20,h=6,txt='Agencia:', border=1, align='C', fill=True)
        pdf.cell(w=0,h=6,txt=inspeccionm.IdSolicitud.IdPerfil.IdAgencia.Nombre if hasattr(inspeccionm, 'IdSolicitud') else '', border=1, align='C', fill=False, ln=1)
        pdf.cell(w=65,h=5,txt=(inspeccionm.IdSolicitud.IdPerfil.Nombres if hasattr(inspeccionm, 'IdSolicitud') else '') +' '+ (inspeccionm.IdSolicitud.IdPerfil.Apellidos if hasattr(inspeccionm, 'IdSolicitud') else '' ), border=1,  align='C', fill=False)
        pdf.cell(w=50,h=5,txt=inspeccionm.IdSolicitud.IdPerfil.IdDistrito.Distrito if hasattr(inspeccionm, 'IdSolicitud') else '', border=1, align='C', fill=False)
        pdf.cell(w=20,h=5,txt='Fecha', border=1, align='C', fill=True)
        x=pdf.get_x()
        pdf.cell(w=0,h=5,txt=pim.Fecha.strftime("%d/%m/%Y") if hasattr(pim, 'Fecha') else '', border=1, align='C', fill=False, ln=1)
        pdf.cell(w=65,h=10,txt='Dirección del proyecto:', border=1, align='C', fill=True)
        y=pdf.get_y()
        pdf.multi_cell(w=70,h=5,txt=str(do.DireccionExac) if hasattr(do, 'DireccionExac') else '', border='TLR',  align='C', fill=False)
        pdf.set_xy(x, y)
        pdf.multi_cell(w=0,h=5,txt='Dias estimados para la construcción de la obra:', border=1, align='C', fill=True)
        
        pdf.cell(w=65,h=6,txt='Mejora a realizar:', border=1, align='C', fill=True)
        pdf.cell(w=70,h=6,txt=DMipm.Descripcion if hasattr(DMipm, 'Descripcion') else '', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=6,txt=str(DMipm.DiasEsti) if hasattr(DMipm, 'DiasEsti') else '', border=1, align='C', fill=False, ln=1)

        pdf.text(x=20, y=249, txt='F. ')
        pdf.line(20, 250, 60, 250)
        pdf.text(x=20, y=255, txt='Nombre. ')
        pdf.text(x=20, y=259, txt='Tec. de Construcción ')
       

        pdf.output('pInspeccionMejoraUbicacion.pdf', 'F')
        return FileResponse(open('pInspeccionMejoraUbicacion.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
