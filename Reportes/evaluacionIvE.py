from fpdf import FPDF
from datetime import date
import locale
from termcolor import colored
from django.http import FileResponse
from EvaluacionIvEFApp.models import *


class evaluacionIvEF(FPDF):
    
    def evaluacionIvE(request, id ):
        locale.setlocale(locale.LC_ALL, '')
        fecha=date.today()

        ide=int(id)
        try:    
            egf=  EgresosFami.objects.get(Id=ide)
        except EgresosFami.DoesNotExist:
            egf="" 
        try: 
            cliente = Perfil.objects.get(Id=egf.IdPerfil.Id)
        except Perfil.DoesNotExist:
            cliente=""        
        try:    
            igf=  IngresosFami.objects.get(IdEgresosFami=ide)
        except IngresosFami.DoesNotExist:
            igf="" 
        try:    
            cpf=  CapacidadPagoFam.objects.get(IdEgresosFami=ide)
        except CapacidadPagoFam.DoesNotExist:
            cpf="" 
        try:
            bns=BienesHoga.objects.filter(IdEgresosFami=ide)
        except BienesHoga.DoesNotExist:
            bns=""

        r=59
        g=93
        b=149
        aux=[0, 1, 2, 3, 4]
        aux2=[0, 1, 2]    
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        #pdf.multi_cell(w=0, h=40, txt='', border=1)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=8, y=5, w=45, h=30)#, link=url) 
        pdf.set_font('Arial', 'B', 12)
        pdf.set_y(30)
        pdf.set_left_margin(10)       
        pdf.cell(w=142,h=8,txt='EVALUACIÓN PERSONAL', border=1,  align='C', fill=False, ln=1)
        pdf.cell(w=142,h=6,txt='', border='T',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=20,h=6,txt='Solicitante: ' , border='', align='L', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=122,h=6,txt= (cliente.Nombres if hasattr(cliente, 'Nombres') else '') +' '+ (cliente.Apellidos if hasattr(cliente, 'Apellidos') else '') , border='', align='L', fill=True, ln=1)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='Descripción de los bienes del hogar encontrados en la vivienda', border='', align='L', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=30,h=5,txt='No.', border=1, align='C', fill=False)
        pdf.cell(w=50,h=5,txt='Descripcioón del bien', border=1, align='C', fill=False)
        pdf.cell(w=32,h=5,txt='Precio de Compra', border=1, align='C', fill=False)
        pdf.cell(w=30,h=5,txt='Cuota mensual', border=1, align='C', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L', align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)

        if bns!='' and len(bns)>0:
            for i in bns:
                pdf.cell(w=30,h=5,txt=i.Numero, border=1, align='L', fill=False)
                pdf.cell(w=50,h=5,txt=i.DescripcionBien, border=1, align='L', fill=False)
                pdf.cell(w=32,h=5,txt='$ '+str(i.PrecioComp), border=1, align='R', fill=False)
                pdf.cell(w=30,h=5,txt='$ '+str(i.CuotaMens), border=1, align='R', fill=False)
                pdf.cell(w=0,h=5,txt='', border='L', align='L', fill=False, ln=1)
        else:
            
            for i in aux:
                pdf.cell(w=30,h=5,txt='', border=1, align='L', fill=False)
                pdf.cell(w=50,h=5,txt='', border=1, align='L', fill=False)
                pdf.cell(w=32,h=5,txt='', border=1, align='L', fill=False)
                pdf.cell(w=30,h=5,txt='', border=1, align='L', fill=False)
                pdf.cell(w=0,h=5,txt='', border='L', align='L', fill=False, ln=1)

               
        pdf.cell(w=170,h=10,txt='', border='B',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=170,h=6,txt='EVALUACIÓN DE INGRESOS VRS. EGRESOS FAMILIARES', border=1,  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=170,h=5,txt='', border='TB',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(191,191,191)
        pdf.cell(w=170,h=6,txt='Flujo de Caja', border=1,  align='C', fill=True, ln=1)
        pdf.cell(w=105,h=6,txt='Egresos', border=1,  align='C', fill=True)
        pdf.cell(w=65,h=6,txt='Ingresos', border=1,  align='C', fill=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=6,txt='', border='L',  align='C', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Alimentación del grupo familiar', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Alimentacion) if hasattr(egf, 'Alimentacion') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Familiar', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(igf.Familiar) if hasattr(igf, 'Familiar') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Educación del grupo familiar', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Educacion) if hasattr(egf, 'Educacion') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Otros ingresos', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(igf.OtrosIngr)if hasattr(igf, 'OtrosIngr') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Transporte', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Transporte) if hasattr(egf, 'Transporte') else '0', border='RBT',  align='R', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=40,h=5,txt='Total(2)', border=1,  align='L', fill=False)      
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(igf.TotalIngr) if hasattr(igf, 'TotalIngr') else '0', border='RBT',  align='R', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Salud / ISSS / ISBM / Otros gastos de salud', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Salud) if hasattr(egf, 'Salud') else '0', border='RBT',  align='R', fill=False)
        pdf.set_fill_color(191,191,191)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=65,h=5,txt='Análisis de Capacidad de Pago', border=1,  align='C', fill=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt='Porcentajes', border=1,  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='AFP / IPSFA / IRS / Otros', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Afp) if hasattr(egf, 'Afp') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=65,h=5,txt='Endeudamiento Actual:', border=1,  align='C', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=0,h=5,txt=str(cpf.PorcentajeEnde) if hasattr(cpf, 'PorcentajeEnde') else '0.0%', border=1,  align='C', fill=True, ln=1)
        pdf.cell(w=80,h=5,txt='Servicios', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Servicios) if hasattr(egf, 'Servicios') else '0', border='RBT',  align='R', fill=False)
        pdf.set_fill_color(191,191,191)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=40,h=5,txt='Disponible = 2-1', border=1,  align='C', fill=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=25,h=5,txt='', border='LRT',  align='L', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=0,h=5,txt='', border='LRT',  align='L', fill=True, ln=1)
        pdf.cell(w=80,h=5,txt='Alquiler', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Alquiler) if hasattr(egf, 'Alquiler') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=40,h=5,txt='Ingresos - Egresos', border=1,  align='C', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='B',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(cpf.Disponible) if hasattr(cpf, 'Disponible') else '0', border='RB',  align='R', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=0,h=5,txt=str(cpf.PorcentajeDisp) if hasattr(cpf, 'PorcentajeDisp') else '0', border='LRB',  align='C', fill=True, ln=1)
        pdf.cell(w=35,h=5,txt='', border='LRT',  align='L', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=45,h=5,txt='En Planilla', border=1,  align='L', fill=True)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=True)
        pdf.cell(w=20,h=5,txt=str(egf.PorcentajePlan) if hasattr(egf, 'PorcentajePlan') else '0', border='RBT',  align='R', fill=True)
        pdf.cell(w=40,h=5,txt='Cuota', border=1,  align='C', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(cpf.Cuota) if hasattr(cpf, 'Cuota') else '0', border='RBT',  align='R', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=0,h=5,txt=str(cpf.PorcentajeCuot) if hasattr(cpf, 'PorcentajeCuot') else '0', border=1,  align='C', fill=True, ln=1)
        pdf.cell(w=35,h=5,txt='Préstamos Actuales', border='LR',  align='C', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=45,h=5,txt='En Ventanilla', border=1,  align='L', fill=True)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=True)
        pdf.cell(w=20,h=5,txt=str(egf.PorcentajeVent) if hasattr(egf, 'PorcentajeVent') else '0', border='RBT',  align='R', fill=True)
        pdf.cell(w=40,h=5,txt='Superávit', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(cpf.Superavit) if hasattr(cpf, 'Superavit') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=35,h=5,txt='', border='LRB',  align='L', fill=False)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=45,h=5,txt='HPH EL SALVADOR', border=1,  align='L', fill=True)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=True)
        pdf.cell(w=20,h=5,txt=str(egf.PorcentajeHplhes) if hasattr(egf, 'PorcentajeHplhes') else '0', border='RBT',  align='R', fill=True)
        pdf.cell(w=40,h=5,txt='Deficit', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(cpf.Deficit) if hasattr(cpf, 'Deficit') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Otros descuentos', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.OtrosDesc) if hasattr(egf, 'OtrosDesc') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Recreación', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Recreacion) if hasattr(egf, 'Recreacion') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=5,txt='Imprevistos', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Imprevistos) if hasattr(egf, 'Imprevistos') else '0', border='RBT',  align='R', fill=False)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=80,h=5,txt='Total(1)', border=1,  align='L', fill=False)
        pdf.cell(w=5,h=5,txt='$', border='LBT',  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(egf.Total) if hasattr(egf, 'Total') else '0', border='RBT',  align='R', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt='', border='L',  align='L', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='', border='', align='L', fill=False, ln=1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=80,h=7,txt='Crédito presentado por:', border='',  align='L', fill=False)
        pdf.cell(w=60,h=7,txt='', border='B',  align='L', fill=False)
        pdf.cell(w=0,h=7,txt='', border='',  align='L', fill=False, ln=1)
        pdf.cell(w=80,h=7,txt='Cargo:', border='',  align='L', fill=False)
        pdf.cell(w=60,h=7,txt='', border='B',  align='L', fill=False)
        pdf.cell(w=0,h=7,txt='', border='',  align='L', fill=False, ln=1)
        pdf.cell(w=0,h=25,txt='', border='', align='L', fill=False, ln=1)
        pdf.cell(w=80,h=7,txt='Firma:', border='',  align='L', fill=False)
        pdf.cell(w=60,h=7,txt='', border='B',  align='L', fill=False)
        pdf.cell(w=0,h=7,txt='', border='',  align='L', fill=False, ln=1)
  
     
        pdf.output('evaluacionPersonal.pdf', 'F')
        return FileResponse(open('evaluacionPersonal.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

