from fpdf import FPDF
from datetime import date
import locale

from django.http import FileResponse
from ListaChequeoApp.models import *
from SolicitudesApp.models import DatosPersFia


class listaCheq(FPDF):
    
    def listChequeo(request, id ):

        try:
            lc=  ListaCheq.objects.get(Id=id)
        except ListaCheq.DoesNotExist:
            lc=""

        try:
            codeudor =  DatosPersFia.objects.get(IdSolicitud=lc.IdSolicitud.Id, Tipo='codeudor')
            # Tu código para manejar el caso en que el codeudor existe
            codeudor=True
        except DatosPersFia.DoesNotExist:
            codeudor=False
  
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        #pdf.multi_cell(w=0, h=40, txt='', border=1)
        
        pdf.set_font('Arial', 'B', 10)
        #pdf.set_fill_color(r,g,b)
        #pdf.set_text_color(255,255,255)
        pdf.cell(w=0,h=5,txt='LISTA DE CHEQUEO PARA SOLICITUDES DE CRÉDITO', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='',  align='C', fill=False, ln=1)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=4, y=3, w=55, h=20)
        pdf.cell(w=0,h=3,txt='', border='',  align='C', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=45,h=5,txt='Nombre del Cliente:', border=0, align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=105,h=5,txt=lc.IdSolicitud.IdPerfil.Nombres +' '+ lc.IdSolicitud.IdPerfil.Apellidos , border='B', align='L', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=20,h=5,txt='Fecha:', border=0, align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=25,h=5,txt=str(lc.Fecha) if hasattr(lc, 'Fecha') else '', border='B', align='R', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=45,h=5,txt='Agencia:', border=0, align='L', fill=False)
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=35,h=5,txt=lc.IdSolicitud.IdPerfil.IdAgencia.Nombre if hasattr(lc, 'IdSolicitud') else '', border='B', align='L', fill=False , ln=1)

        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=0,h=2,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=80,h=6,txt='Información del Solicitante y Fiador:' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=150,h=5,txt='  1   Solicitud del Cliente', border='', align='L', fill=False)
        if lc.SolicitudCred =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=150,h=5,txt='  2   Fotocopias de DUI y NIT del Cliente', border='', align='L', fill=False)
        if lc.FotocopiaDui =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=150,h=5,txt='  3   Recibos de último mes, cancelados de agua, luz y teléfono', border='', align='L', fill=False)
        if lc.RecibosAgua =="Si" and lc.RecibosLuz =='Si' or lc.RecibosAgua =="Si" and lc.RecibosLuz =='Si' and lc.RecibosTele =='Si':
            pdf.cell(w=15,h=5,txt='X' or '', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=150,h=5,txt='  4   Constancia de ingresos', border='', align='L', fill=False)
        pdf.cell(w=15,h=5,txt='', border='', align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.1 ', border=0, align='C', fill=False)
        pdf.cell(w=45,h=6,txt='Para empleados' , border='B', align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.1.1 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Constancia de empleo actualizada' , border='', align='L', fill=False)
        if lc.ConstanciaEmpl =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.1.2 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Taco ISSS' , border='', align='L', fill=False)
        if lc.TacoIsss =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.2 ', border=0, align='C', fill=False)
        pdf.cell(w=85,h=6,txt='Para comerciantes o independientes' , border='B', align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.2.1 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Análisis económico del negocio' , border='', align='L', fill=False)
        if lc.AnalisisEcon =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.2.2 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Balance (para casos que aplique)' , border='', align='L', fill=False)
        if lc.Balance =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='4.2.3 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Balance de resultados (para casos que aplique)' , border='', align='L', fill=False)
        if lc.BalanceResu =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=150,h=5,txt='  5   Información del Fiador (para casos que aplique)', border='', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=15,h=5,txt='', border='', align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='5.1 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Copia de DUI y NIT' , border='', align='L', fill=False)
        
        if codeudor==True and lc.CopiaDuiFia =="Si":#Documentos fiador
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='5.2 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Copia de recibos de agua y luz' , border='', align='L', fill=False)
        if codeudor==True and lc.RecibosAguaFia =="Si" and lc.RecibosLuzFia=='Si':
            pdf.cell(w=15,h=5,txt='X' or '', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='5.3 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Constancia de empleo actualizada o análisis económico del negocio' , border='', align='L', fill=False)
        if codeudor==True and lc.ConstanciaEmplFia =="Si" :
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='6 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Referencias Crediticias del Solicitante y Fiador' , border='', align='L', fill=False)
        if codeudor==True and lc.ReferenciaCred=="Si" and lc.ReferenciaCredFia =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        elif codeudor==False and lc.ReferenciaCred=="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=45,h=6,txt='Información Técnica' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='7 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Inspección Técnica' , border='', align='L', fill=False)
        if lc.InspeccionTecn =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='8 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Presupuesto de Construcción' , border='', align='L', fill=False)
        if lc.PresupuestoCons =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=45,h=6,txt='Información Legal' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='9 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Certificación Extractada (máximo un mes de antiguedad)' , border='', align='L', fill=False)
        if lc.CertificadoExtr =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='10 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Carencia de Bienes (para casos que aplique)' , border='', align='L', fill=False)
        if lc.CarenciaBien =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='11 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Fotocopia de Escritura' , border='', align='L', fill=False)
        if lc.FotocopiaEscr =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=45,h=6,txt='Información de Riesgo' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='12 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Declaración de Salud' , border='', align='L', fill=False)
        if lc.DeclaracionSalu =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='13 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Informe DICOM' , border='', align='L', fill=False)
        if lc.InformeDico =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=45,h=6,txt='Anexos' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='14 ', border=0, align='C', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=105,h=6,txt='Documentos de soporte de ingresos (facturas, recibos, otros) ' , border='', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        if lc.DocumentoSopoIng =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='15 ', border=0, align='C', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=105,h=6,txt='Documentos de remesas de los últimos tres meses (para casos que aplique)' , border='', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        if lc.DocumentoReme =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='16 ', border=0, align='C', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=105,h=6,txt='Cancelaciones de préstamos o estados de cuenta (para casos que aplique)' , border='', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        if lc.CancelacionesPresEst =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='17 ', border=0, align='C', fill=False)
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=105,h=6,txt='Finiquitos (para casos que aplique)' , border='', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        if lc.Finiquitos =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=105,h=6,txt='Documentos de Orden de Inicio y Desembolso' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='18 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Hoja de Aprobación del Crédito' , border='', align='L', fill=False)
        if lc.HojaAproCre =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='19 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Carta para la Elaboración del Mutuo' , border='', align='L', fill=False)
        if lc.CartaElabMut =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='20 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Recibo de pago de prima (para casos que aplique)' , border='', align='L', fill=False)
        if lc.ReciboPagoPri =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='21 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Orden de Descuento Irrevocable (para casos que aplique)' , border='', align='L', fill=False)
        if lc.OrdenDeseIrr =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='22 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Permiso de Construcción (para casos que aplique)' , border='', align='L', fill=False)
        if lc.PermisoCons =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=105,h=6,txt='Documentos de entrega de costos y desemblsos ' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='23 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Carta de entrega de costos o de desembolso' , border='', align='L', fill=False)
        if lc.CartaEntrCosdes =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='24 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Fotocopia de Mutuo Hipotecario o Simple' , border='', align='L', fill=False)
        if lc.FotocopiaMutu =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=105,h=6,txt='Mantener Actualizado ' , border='B', align='L', fill=False)
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0,h=6,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='25 ', border=0, align='C', fill=False)
        pdf.cell(w=105,h=6,txt='Gestiones de Cobro' , border='', align='L', fill=False)
        if lc.GestionCobr =="Si":
            pdf.cell(w=15,h=5,txt='X', border=1, align='C', fill=False)
        else:
            pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)


        pdf.output('listaChequeo.pdf', 'F')
        return FileResponse(open('listaChequeo.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

