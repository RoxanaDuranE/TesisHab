from fpdf import FPDF
from datetime import date
import locale
from termcolor import colored
from django.http import FileResponse
from SolicitudesApp.models import *
from InspeccionLoteApp.models import *
from InspeccionMejViviendaApp.models import *
from HistorialApp.models import *


class solDen(FPDF):
    
    def solicitudesDen(request, id ):

        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
        try:
            d=  Domicilio.objects.get(IdSolicitud=id, Tipo="Solicitante")
        except Domicilio.DoesNotExist:
            d=""
        try:
            do=  DatosObra.objects.get(IdSolicitud=id)
        except DatosObra.DoesNotExist:
            do=""
        try:
            dt=  Detalle.objects.get(IdSolicitud=id)
        except Detalle.DoesNotExist:
            dt=""
        
        try:
            rh=  RegistroHist.objects.get(IdSolicitud=id)
        except RegistroHist.DoesNotExist:
            rh=""
        
        if s.TipoObra=='mejora':
            try:
                inspm=InspeccionMejo.objects.get(IdSolicitud=s.Id)  
                ft=FactibilidadInsMej.objects.get(IdInspeccionMejo=inspm.Id) 
            except InspeccionMejo.DoesNotExist:
                inspm=""   
                
        else:
            try:
                inspl=InspeccionLote.objects.get(IdSolicitud=s.Id) 
                ft=FactibilidadInsLot.objects.get(IdInspeccionLote=inspl.Id)   
            except InspeccionLote.DoesNotExist:
                inspl=""
                  
        
        locale.setlocale(locale.LC_TIME, '')
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()      

        pdf.set_font('Arial', 'B', 12)
        pdf.set_y(20)
        pdf.set_left_margin(20)
        pdf.cell(w=0,h=5,txt='ASOCIACIÓN HPH EL SALVADOR ', border='',  align='C', fill=False, ln=1)  
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=5,txt=s.IdPerfil.IdAgencia.Departamento if hasattr(s, 'IdPerfil') else '', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=0,h=5,txt="Datos de Solicitud Denegada ", border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=15, y=15, w=55, h=20)
        pdf.cell(w=0,h=10,txt='', border='',  align='C', fill=False, ln=1)

        pdf.cell(w=0,h=5,txt=s.Fecha.strftime("%A, %d de %B de %Y") if hasattr(s, 'Fecha') else '', border='', align='R', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=190,h=5,txt='Datos del Solicitante:', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=60,h=6,txt='DUI:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=s.IdPerfil.Dui if hasattr(s, 'IdPerfil') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Nombre del Cliente:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=s.IdPerfil.Nombres +' '+ s.IdPerfil.Apellidos, border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Dirección:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=d.Direccion if hasattr(d, 'Direccion') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=s.IdPerfil.Telefono if hasattr(s, 'IdPerfil') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Profesión u oficio:', border=0, align='L', fill=False)
        pdf.set_font('Arial', '', 7)
        pdf.cell(w=110,h=6,txt=s.IdPerfil.IdOcupacion.Nombre if hasattr(s, 'IdPerfil') else '', border=0, align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=60,h=6,txt='Ingresos:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt='$   '+ str(d.SalarioIngr) if hasattr(d, 'SalarioIngr') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Puntaje DICOM:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt= str(rh.Puntaje) if hasattr(rh, 'Puntaje') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=6,txt='', border=0, align='L', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=190,h=5,txt='Datos de la Obra a Realizar:', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=60,h=6,txt='Destino del Credito:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=do.IdAlternativa.Alternativa if hasattr(do, 'IdAlternativa') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Detalle de la Obra:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=do.IdModeloVivi.TipoVivi  if hasattr(do, 'IdModeloVivi') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Presupuesto de la Obra:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt='$   '+ str(do.Presupuesto) if hasattr(do, 'Presupuesto') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=6,txt='', border=0, align='L', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=190,h=5,txt='Detalle de la Solicitud:', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=60,h=6,txt='Monto a Solicitar:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt='$   '+ str(dt.Monto) if hasattr(dt, 'Monto') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Plazo solicitado:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=dt.Plazo if hasattr(dt, 'Plazo') else '' , border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Cuota:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt='$   '+ str(dt.Cuota) if hasattr(dt, 'Cuota') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=60,h=6,txt='Fecha que Solicita Pagar:', border=0, align='L', fill=False)
        pdf.cell(w=110,h=6,txt=dt.FechaPago if hasattr(dt, 'FechaPago') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=6,txt='', border=0, align='L', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=190,h=5,txt='Observaciones:', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=6,txt=s.Observaciones if hasattr(s, 'Observaciones') else '', border=0, align='L', fill=False, ln=1)

    
        pdf.output('solicitudesDenegadas.pdf', 'F')
        return FileResponse(open('solicitudesDenegadas.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
