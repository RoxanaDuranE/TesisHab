from fpdf import FPDF
from datetime import date
import locale
from ConozcaClienteApp.models import ClienteDatoGen
from HistorialApp.models import RegistroHist
from django.http import FileResponse
from SolicitudesApp.models import *
from EvaluacionIvEFApp.models import *
from SolicitudInscripcionSApp.models import *


class formularioCN(FPDF):
    
    def formComiteN(request, id ):

        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
        try:    
            cdg=  ClienteDatoGen.objects.get(IdSolicitud=s.Id)
        except ClienteDatoGen.DoesNotExist:
            cdg="" 
        try:
            d=  Domicilio.objects.get(IdSolicitud=id, Tipo="Solicitante")
        except Domicilio.DoesNotExist:
            d=""
        try:
            df=  Domicilio.objects.get(IdSolicitud=id, Tipo="codeudor")
        except Domicilio.DoesNotExist:
            df=""
            
        try:
            dpf=  DatosPersFia.objects.get(IdSolicitud=id)
        except DatosPersFia.DoesNotExist:
            dpf=""
        try:
            do=  DatosObra.objects.get(IdSolicitud=id)
        except DatosObra.DoesNotExist:
            do=""
        try:
            dt=  Detalle.objects.get(IdSolicitud=id)
        except Detalle.DoesNotExist:
            dt=""
        try:
            rh=  RegistroHist.objects.get(IdSolicitud=s.Id)
        except RegistroHist.DoesNotExist:
            rh=""
        ##############################################3
        try:
            eg=  EgresosFami.objects.get(IdPerfil=s.IdPerfil.Id, Estado="1")
        except EgresosFami.DoesNotExist:
            eg=""
        try:
            ca=  CapacidadPagoFam.objects.get(IdEgresosFami=eg.Id)
        except CapacidadPagoFam.DoesNotExist:
            ca=""
                 
        try:
            ss=  SolicitudInscSeg.objects.get(IdSolicitud=id)
        except SolicitudInscSeg.DoesNotExist:
            ss=""
            
        try:
            ssd=  SolicitudInscSegDefAmpDefFis.objects.get(IdSolicitudInscSeg=ss.Id)
        except SolicitudInscSegDefAmpDefFis.DoesNotExist:
            ssd=""
                  
        # para calcular el plazo en meses          
        try:
            varp=(int(ss.Plazo) *12)
        except :
            varp=""

        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()      

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=0,h=5,txt='ASOCIACIÓN HPH EL SALVADOR ', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(w=0,h=5,txt='Formulario de Comite de Crédito', border='',  align='C', fill=False, ln=1)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=9, y=6, w=55, h=20)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        
        pdf.cell(w=98,h=5,txt='     Datos del Solicitante:', border=0, align='L', fill=False)
        pdf.cell(w=98,h=5,txt='     Datos Actividad Economica Solicitante', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=38,h=6,txt='Codigo de Cliente:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=cdg.Codigo if hasattr(cdg, 'Codigo') else '', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Sector Productivo:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt='', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Nombre del Cliente:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=(s.IdPerfil.Nombres if hasattr(s, 'IdPerfil') else '') +' '+ (s.IdPerfil.Apellidos if hasattr(s, 'IdPerfil') else ''), border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Dirección Actividad', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=d.DireccionTrabMic if hasattr(d, 'DireccionTrabMic') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Dirección:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=d.Direccion if hasattr(d, 'Direccion') else '', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=d.TelefonoTrabMic if hasattr(d, 'TelefonoTrabMic') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=s.IdPerfil.Telefono if hasattr(s, 'IdPerfil') else '', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Tiempo de Servicio:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=d.TiempoEmprTieFun if hasattr(d, 'TiempoEmprTieFun') else '', border=0, align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=98,h=5,txt='     Datos del Codeudor:', border=0, align='L', fill=False)
        pdf.cell(w=98,h=5,txt='     Datos Actividad Economica Codeudor', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=38,h=6,txt='Codigo de Codeudor:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt='', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Sector Productivo:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt='', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Nombre del Codeudor:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=(dpf.NombreFiad if hasattr(dpf, 'NombreFiad') else '' ) +' '+ (dpf.ApellidoFiad if hasattr(dpf, 'ApellidoFiad') else '' ) , border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Dirección Actividad', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=df.DireccionTrabMic if hasattr(df, 'DireccionTrabMic') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Dirección:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=df.Direccion  if hasattr(df, 'Direccion') else '', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=df.TelefonoTrabMic if hasattr(df, 'TelefonoTrabMic') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='Teléfono:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=df.Telefono if hasattr(df, 'Telefono') else '', border=0, align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Tiempo de Servicio:', border=0, align='L', fill=False)
        pdf.cell(w=60,h=6,txt=df.TiempoEmprTieFun if hasattr(df, 'TiempoEmprTieFun') else '', border=0, align='L', fill=False, ln=1)

        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(w=0,h=5,txt='CREDITO SOLICITADO ', border='',  align='C', fill=False, ln=1)   
        pdf.cell(w=0,h=2,txt='', border=0, align='C', fill=False, ln=1)   
        pdf.cell(w=98,h=6,txt='Cuenta Número:', border=0, align='R', fill=False)
        pdf.cell(w=98,h=6,txt='', border=0, align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 8)

        pdf.cell(w=0,h=3,txt='', border=0, align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='Linea de Financiamiento:', border=0, align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'alternativa') and do.IdAlternativa.Alternativa == 'CONSTRUCCION VIVIENDA IN SITU' else '', border=1, align='C', fill=False)
        pdf.cell(w=30,h=5,txt='Const. Vivienda', border='', align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'alternativa') and do.IdAlternativa.Alternativa == 'MEJORAMIENTO' else '', border=1, align='C', fill=False)
        pdf.cell(w=30,h=5,txt='Mejoramiento', border='', align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'alternativa') and do.IdAlternativa.Alternativa == 'VIVIENDA USADA' else '', border=1, align='C', fill=False)
        pdf.cell(w=20,h=5,txt='V. Usada', border='', align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'alternativa') and do.IdAlternativa.Alternativa == 'VIVIENDA NUEVA' else '', border=1, align='C', fill=False)
        pdf.cell(w=20,h=5,txt='V. Nueva', border='', align='C', fill=False, ln=1)
        pdf.cell(w=0,h=3,txt='', border=0, align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='', border=0, align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'LOTE MAS VIVIENDA' else '', border=1, align='C', fill=False)
        pdf.cell(w=30,h=5,txt='Lote + Vivienda', border='', align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'CORPORATIVO' else '', border=1, align='C', fill=False)
        pdf.cell(w=30,h=5,txt='Coorporativo', border='', align='C', fill=False)
        pdf.cell(w=7,h=3,txt='X' if hasattr(do, 'IdAlternativa') and do.IdAlternativa.Alternativa == 'PROYECTO ESPECIAL' else '', border=1, align='C', fill=False)
        pdf.cell(w=35,h=5,txt='Proyecto Especial', border='', align='C', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='C', fill=False, ln=1)

        pdf.cell(w=0,h=5,txt='', border=0, align='C', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Monto', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Cuota', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Plazo (Meses)', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Forma de Pago:', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='No Cuotas', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='Solicitado:', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt=str(dt.Monto) if hasattr(dt, 'Monto') else '', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0 ', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='Sugerido:', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt=str(do.Presupuesto) if hasattr(do, 'Presupuesto') else '', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt=str(ca.Cuota) if hasattr(ca, 'Cuota') else '', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt=str(varp) if hasattr(ss, 'Plazo') else '', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Mensual', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt=str(varp) if hasattr(ss, 'Plazo') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='Prima:', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Analista', border=0, align='L', fill=False)
        pdf.cell(w=0,h=6,txt='  ', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='Subsidio:', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='0', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Puntuación Dicom', border=0, align='L', fill=False)
        pdf.cell(w=64,h=6,txt= str(rh.Puntaje) if hasattr(rh, 'Puntaje') else '', border='B', align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border=0, align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 8)                    
        pdf.cell(w=64,h=7,txt='Destino del Financiamiento:', border=0, align='L', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=64,h=6,txt=do.IdAlternativa.Alternativa if hasattr(do, 'IdAlternativa') else '', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=32,h=6,txt='Garantía:', border=0, align='L', fill=False)
        pdf.cell(w=64,h=6,txt=ss.Garantia if hasattr(ss, 'Garantia') else '', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='', border=0, align='L', fill=False)
        pdf.cell(w=32,h=6,txt='Tasa de Interes:', border=0, align='R', fill=False)
        pdf.cell(w=32,h=6,txt=(str(do.IdAlternativa.IdTasaInte.Interes) if hasattr(do, 'IdAlternativa') else '') +'%', border=0, align='L', fill=False, ln=1)
        pdf.cell(w=64,h=6,txt='Nombre de Línea de Financiamiento:', border=0, align='L', fill=False)
        pdf.cell(w=64,h=6,txt=str(do.IdAlternativa.Alternativa) +" "+ (str(do.IdAlternativa.IdTasaInte.Interes)) + '%', border=0, align='L', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(w=0,h=5,txt='CHEQUEO DE RELACIONES INTERNAS ', border='',  align='C', fill=False, ln=1)   
        pdf.cell(w=0,h=7,txt='', border=0, align='C', fill=False, ln=1)  

        pdf.cell(w=0,h=5,txt='RESOLUCION DEL COMITE DE CREDITO ', border='',  align='C', fill=False, ln=1)   
        pdf.cell(w=0,h=3,txt='', border=0, align='C', fill=False, ln=1)  
        pdf.cell(w=35,h=5,txt='', border=0, align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border=0, align='C', fill=False)
        if s.EstadoSoli == 4:
            pdf.cell(w=7,h=3,txt='X', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Aprobado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Denegado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Observado', border='', align='L', fill=False, ln=1 )
        elif s.EstadoSoli == 6:
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Aprobado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='X', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Denegado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Observado', border='', align='L', fill=False, ln=1 )
        elif s.EstadoSoli == 5:
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Aprobado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Denegado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='X', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Observado', border='', align='L', fill=False, ln=1 )
        else:
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Aprobado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Denegado', border='', align='L', fill=False)
            pdf.cell(w=7,h=3,txt='', border=1, align='C', fill=False)
            pdf.cell(w=45,h=5,txt='    Observado', border='', align='L', fill=False, ln=1 )
        pdf.set_font('Arial', '', 8)

        pdf.cell(w=0,h=3,txt='', border='', align='C', fill=False, ln=1 )
        pdf.cell(w=28,h=6,txt='Monto Aprob. $:', border=0, align='L', fill=False)
        pdf.cell(w=27,h=6,txt='', border='B', align='L', fill=False)
        pdf.cell(w=12,h=6,txt='Plazo:', border=0, align='L', fill=False)
        pdf.cell(w=12,h=6,txt='', border='B', align='L', fill=False)
        pdf.cell(w=20,h=6,txt='Nro. Cuota:', border=0, align='L', fill=False)
        pdf.cell(w=12,h=6,txt='', border='B', align='L', fill=False)
        pdf.cell(w=27,h=6,txt='Forma de Pago:', border=0, align='L', fill=False)
        pdf.cell(w=15,h=6,txt='', border='B', align='L', fill=False)
        pdf.cell(w=25,h=6,txt='Tasa Inflación:', border=0, align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border='B', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=42,h=6,txt='Aplica a Seguro de Desempleo:', border=0, align='L', fill=False)
        pdf.cell(w=8,h=6,txt=ssd.SeguroDese if hasattr(ssd, 'SeguroDese') else '', border='B', align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=2,txt='', border='', align='C', fill=False, ln=1 )
        pdf.cell(w=38,h=6,txt='Fecha del Cómite:', border=0, align='L', fill=False)
        pdf.cell(w=35,h=7,txt='', border='B', align='L', fill=False)
        pdf.cell(w=38,h=6,txt='Fuente de Fondos.', border=0, align='C', fill=False)
        pdf.cell(w=35,h=6,txt='F..', border=0, align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border=0, align='L', fill=False, ln=1)

        pdf.cell(w=38,h=6,txt='Observaciones:', border=0, align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border='B', align='R', fill=False, ln=1)
        pdf.cell(w=38,h=6,txt='', border=0, align='L', fill=False)
        pdf.cell(w=0,h=6,txt='', border='B', align='R', fill=False, ln=1)
        pdf.cell(w=0,h=6,txt='', border='', align='R', fill=False, ln=1)

        pdf.cell(w=35,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='', border='B', align='L', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='', border='B', align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=35,h=5,txt='Gerente de Créditos', border='', align='C', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='Gerencia de Operaciones', border='', align='C', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='Gerencia de Admón. y finanzas', border='', align='C', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='Supervisor de Construcción', border='', align='C', fill=False)
        pdf.cell(w=5,h=5,txt='', border='', align='R', fill=False)
        pdf.cell(w=35,h=5,txt='Superv. de Créditos', border='', align='C', fill=False, ln=1)



        pdf.output('formularioComiteNatural.pdf', 'F')
        return FileResponse(open('formularioComiteNatural.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
