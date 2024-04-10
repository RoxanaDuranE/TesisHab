from fpdf import FPDF
from datetime import date
import locale
from django.http import FileResponse
from SolicitudesApp.models import *
from EvaluacionMicroApp.models import *
from SolicitudInscripcionSApp.models import *


class hojaP(FPDF):
    
    def hojaPre(request, id ):

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
            med=Medio.objects.get(IdSolicitud=id)                    
        except Medio.DoesNotExist:
            med=""
        ##############################################3
        try:
            ba=  BalanceSituMic.objects.get(IdPerfil=s.IdPerfil.Id,Estado="1")
        except BalanceSituMic.DoesNotExist:
            ba=""
        try:
            eg=  EgresoFlujMic.objects.get(IdBalanceSituMic=ba.Id)
        except EgresoFlujMic.DoesNotExist:
            eg=""
        try:
            ca=  CapacidadPagoMic.objects.get(IdEgresoFlujMic=eg.Id)
        except CapacidadPagoMic.DoesNotExist:
            ca=""

        try:
            ss=  SolicitudInscSeg.objects.get(IdSolicitud=id)
        except SolicitudInscSeg.DoesNotExist:
            ss=""
        try:
            varp=(int(ss.Plazo) *12)
        except :
            varp=""
                 
        locale.setlocale(locale.LC_TIME, '')
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        
        pdf.set_margins(left=20, top=10, right=-1) # agrega el mergen a la pagina
        pdf.set_font('Arial', 'B', 10)
        #pdf.set_fill_color(r,g,b)
        #pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='         ASOCIACIÓN HPH EL SALVADOR EL SALVADOR', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='AGENCIA  '+ s.IdPerfil.IdAgencia.Nombre if hasattr(s, 'IdPerfil') else '', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='HOJA DE PRE-APROBACIÓN DE CRÉDITO', border='',  align='C', fill=False, ln=1)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=9, y=9, w=45, h=20)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)

        pdf.set_font('Arial', '', 9)
        pdf.cell(w=30,h=5,txt=s.IdPerfil.IdAgencia.Departamento if hasattr(s, 'IdPerfil') else '', border=0, align='L', fill=False)
        pdf.cell(w=0,h=5,txt=s.Fecha.strftime("%A, %d de %B de %Y") if hasattr(s, 'Fecha') else '', border='', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        
        pdf.cell(w=30,h=5,txt='Comunidad:', border=0, align='L', fill=False)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=60,h=5,txt=s.Comunidad if hasattr(s, 'Comunidad') else '', border='B', align='C', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=25,h=5,txt='Municipio:', border=0, align='L', fill=False)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=45,h=5,txt=s.IdPerfil.IdDistrito.Distrito if hasattr(s, 'IdPerfil') else '', border='B', align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='Destino de la Solicitud:', border=0, align='L', fill=False)
        pdf.cell(w=45,h=5,txt='Mejora de Vivienda', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'MEJORAMIENTO' else '', border=1, align='C', fill=False)
        pdf.cell(w=45,h=5,txt='Lote + Vivienda', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'LOTE MAS VIVIENDA' else '', border=1, align='C', fill=False)
        pdf.cell(w=0,h=5,txt='', border=0, align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='', border=0, align='L', fill=False)
        pdf.cell(w=45,h=5,txt='Vivienda In Situ', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'CONSTRUCCION VIVIENDA IN SITU' else '', border=1, align='C', fill=False)
        pdf.cell(w=45,h=5,txt='Vivienda Usada', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='', border=1, align='C', fill=False)
        pdf.cell(w=0,h=5,txt='', border=0, align='C', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
        pdf.cell(w=100,h=5,txt='Datos del Solicitante', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=4,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=30,h=8,txt='Nombre:', border=0, align='L', fill=False)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=116,h=8,txt=(s.IdPerfil.Nombres if hasattr(s, 'IdPerfil') else '') +' '+ (s.IdPerfil.Apellidos if hasattr(s, 'IdPerfil') else '') , border='B', align='C', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=8,txt='', border='', align='R', fill=False, ln=1)
        pdf.cell(w=30,h=8,txt='Dirección:', border=0, align='L', fill=False)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=0,h=8,txt=(d.Direccion if hasattr(d, 'Direccion') else '') +' '+ (d.Referencia if hasattr(d, 'Referencia') else ''), border='B', align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=30,h=8,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=60,h=8,txt=s.IdPerfil.Telefono if hasattr(s, 'IdPerfil') else '', border='B', align='C', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=8,txt='', border='', align='R', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', 'B', 10)
        if s.TipoObra =='mejora':
            pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
            pdf.cell(w=100,h=5,txt='Mejoramiento de Vivienda', border=1,  align='C', fill=False)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Tipo de Mejoramiento:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0,h=8,txt=(do.IdModeloVivi.TipoVivi if hasattr(do, 'IdModeloVivi') else '')+''+ (do.DetalleAdic if hasattr(do, 'DetalleAdic') else ''), border='B', align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=45,h=8,txt='Monto Solicitado:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=25,h=8,txt=str(do.Presupuesto) if hasattr(do, 'Presupuesto') else '', border='B', align='C', fill=False)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=25,h=8,txt='Plazo (meses):', border=0, align='C', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=35,h=8,txt=str(varp) if hasattr(ss, 'Plazo') else '', border='B', align='C', fill=False)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=27,h=8,txt='Cuota Solicitada:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0,h=8,txt=str(ca.Cuota) if hasattr(ca, 'Cuota') else '', border='B', align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        else:
            pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
            pdf.cell(w=100,h=5,txt='Mejoramiento de Vivienda', border=1,  align='C', fill=False)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Tipo de Mejoramiento:', border=0, align='L', fill=False)
            pdf.cell(w=0,h=8,txt='', border='B', align='R', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Monto Solicitado:', border=0, align='L', fill=False)
            pdf.cell(w=25,h=8,txt='', border='B', align='C', fill=False)
            pdf.cell(w=25,h=8,txt='Plazo (meses):', border=0, align='L', fill=False)
            pdf.cell(w=35,h=8,txt='', border='B', align='R', fill=False)
            pdf.cell(w=27,h=8,txt='Cuota Solicitada:', border=0, align='L', fill=False)
            pdf.cell(w=0,h=8,txt='', border='B', align='C', fill=False, ln=1)
            pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)

        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', 'B', 10)
        if s.TipoObra =='vivienda':
            pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
            pdf.cell(w=100,h=5,txt='Vivienda', border=1,  align='C', fill=False)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Modelo de Vivienda:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0,h=8,txt=do.IdModeloVivi.TipoVivi if hasattr(do, 'IdModeloVivi') else '', border='B', align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=45,h=8,txt='Dirección de la Obra:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0,h=8,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border='B', align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=45,h=8,txt='Monto Propuesto:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=25,h=8,txt=str(do.Presupuesto) if hasattr(do, 'Presupuesto') else '', border='B', align='C', fill=False)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=25,h=8,txt='Plazo (meses):', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=35,h=8,txt=str(varp) if hasattr(ss, 'Plazo') else '', border='B', align='C', fill=False)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=27,h=8,txt='Cuota Solicitada:', border=0, align='L', fill=False)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0,h=8,txt=str(ca.Cuota) if hasattr(ca, 'Cuota') else '', border='B', align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=3,txt='', border='', align='R', fill=False, ln=1)
        else:
            pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
            pdf.cell(w=100,h=5,txt='Vivienda', border=1,  align='C', fill=False)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Modelo de Vivienda:', border=0, align='L', fill=False)
            pdf.cell(w=0,h=8,txt='', border='B', align='R', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Dirección de la Obra:', border=0, align='L', fill=False)
            pdf.cell(w=0,h=8,txt='', border='B', align='C', fill=False, ln=1)
            pdf.cell(w=45,h=8,txt='Monto Propuesto:', border=0, align='L', fill=False)
            pdf.cell(w=25,h=8,txt='', border='B', align='C', fill=False)
            pdf.cell(w=25,h=8,txt='Plazo (meses):', border=0, align='L', fill=False)
            pdf.cell(w=35,h=8,txt='', border='B', align='R', fill=False)
            pdf.cell(w=27,h=8,txt='Cuota Solicitada:', border=0, align='L', fill=False)
            pdf.cell(w=0,h=8,txt='', border='B', align='C', fill=False, ln=1)
            pdf.cell(w=0,h=3,txt='', border='', align='R', fill=False, ln=1)

        pdf.cell(w=25,h=5,txt='Aprobado:', border='', align='L', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
        pdf.cell(w=25,h=8,txt='', border='', align='R', fill=False)
        pdf.cell(w=25,h=5,txt='Observado:', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='', border=1, align='C', fill=False)
        pdf.cell(w=25,h=8,txt='', border='', align='R', fill=False)
        pdf.cell(w=25,h=5,txt='Denegado:', border='', align='L', fill=False)
        pdf.cell(w=12,h=5,txt='', border=1, align='C', fill=False)
        pdf.cell(w=0,h=8,txt='', border='', align='R', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)

        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=45,h=5,txt='', border='',  align='C', fill=False)
        pdf.cell(w=100,h=5,txt='Estrategia de Colocación', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=8,txt=(med.Referenciado or '') + (med.CampanaProm or '') + (med.RedesSoci or '') + (med.Pvv or '') + (med.FeriaVivi or '') + (med.Perifoneo or '') + (med.Radio or '') +(med.Especifique or ''), border='B', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=4,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=8,txt='Observaciones:', border=0, align='L', fill=False)
        pdf.cell(w=0,h=8,txt='', border='B', align='R', fill=False, ln=1)
        pdf.cell(w=45,h=8,txt='', border=0, align='L', fill=False)
        pdf.cell(w=0,h=8,txt='', border='B', align='R', fill=False, ln=1)
        pdf.cell(w=0,h=22,txt='', border='', align='R', fill=False, ln=1)

        pdf.cell(w=40,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='', border='B', align='L', fill=False, ln=1)
        pdf.cell(w=40,h=5,txt='Gerente de Agencia', border='', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Oficial de Créditos', border='', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Oficial de Créditos', border='', align='L', fill=False, ln=1)
        pdf.cell(w=40,h=5,txt='Martin Barrillas', border='', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Fernando Díaz', border='', align='L', fill=False)
        pdf.cell(w=25,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Presenta a Cómite', border='', align='L', fill=False, ln=1)

        

        pdf.output('hojaPreAprobacion.pdf', 'F')
        return FileResponse(open('hojaPreAprobacion.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
