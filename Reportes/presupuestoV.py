from fpdf import FPDF
from datetime import date
import locale
from termcolor import colored
from django.http import FileResponse
from PresupuestoVApp.models import *
from ClienteApp.models import *
from django.db.models import Q


class presupuestoVv(FPDF):
    
    def presupuestoV(request, id ):

        try:
            pvdg=  PresupuestoViviDatGen.objects.get(Id=id)
        except PresupuestoViviDatGen.DoesNotExist:
            pvdg=""
        try:
            s=  Solicitud.objects.get(Id=pvdg.IdSolicitud.Id)
        except Solicitud.DoesNotExist:
            s=""

        try:
            do= DatosObra.objects.get(IdSolicitud=pvdg.IdSolicitud.Id)
        except DatosObra.DoesNotExist:
            do=""
        
        try:
            d=  Detalle.objects.get(IdSolicitud=pvdg.IdSolicitud.Id)
        except Detalle.DoesNotExist:
            d=""
        
        try:
            listam=Materiales.objects.filter(Estado="activo")
        except Materiales.DoesNotExist:
            listam=""
        try:
            pvt=  PresupuestoViviTot.objects.get(IdPresupuestoViviDatGen=pvdg.Id)
        except PresupuestoViviTot.DoesNotExist:
            pvt=""

        try:
            lista_materiales= PresupuestoViviMat.objects.filter(IdPresupuestoViviDatGen=pvdg.Id)
            datos_materiales=[]
            for item in lista_materiales:
                datos_materiales.append ( {'id': item.Id, 'precio':item.PrecioUnit,'cantida': item.Cantidad,'total':item.SubTota,
                "nombre":item.IdMateriales.Nombre,"descripcion":item.IdMateriales.Descripcion,"unidad":item.IdMateriales.Unidad,"idm":item.IdMateriales.Id })
        except PresupuestoViviMat.DoesNotExist:
            lista_materiales=""

        try:
            lista_mano_obra= PresupuestoViviManObr.objects.filter(IdPresupuestoViviDatGen=pvdg.Id)
            datos_mano_obra=[]
            for item in lista_mano_obra:
                datos_mano_obra.append({
                    "id":item.Id,
                    "descripcion":item.Descripcion,
                    "unidad":item.Unidad,
                    "preciouni":item.PrecioUnit,
                    "cantidad":item.Cantidad,
                    "total":item.SubTota,
                })
        except PresupuestoViviManObr.DoesNotExist:
            lista_mano_obra=""
    

        r=59
        g=93
        b=149
        aux=[0, 1, 2, 3]
        aux2=[0, 1, 2]    
        subtot=0
        subtotmo=0
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=10, y=12, w=55, h=30)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=0,h=8,txt='PRESUPUESTO DE VIVIENDA HABITAT', border=1,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 7)
        pdf.cell(w=96,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=25,h=5,txt='AGENCIA:', border=1,  align='L', fill=False)
        pdf.cell(w=30,h=5,txt=s.IdPerfil.IdAgencia.Nombre if hasattr(s, 'IdPerfil') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='COSTO TOTAL=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt='$      ' + str(d.Monto) if hasattr(d, 'Monto') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=96,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=25,h=5,txt='FECHA:', border=1,  align='L', fill=False)
        pdf.cell(w=30,h=5,txt=pvdg.Fecha.strftime("%d/%m/%Y") if hasattr(pvdg, 'Fecha') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='CANT. VIVIENDA=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(pvdg.CantidadVivi) if hasattr(pvdg, 'CantidadVivi') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=96,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=40,h=5,txt='TIEMPO DE CONSTRUCCION:', border=1,  align='L', fill=False)
        pdf.cell(w=15,h=5,txt=pvdg.TiempoCons if hasattr(pvdg, 'TiempoCons') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='COSTO TOTAL=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt='$      '+ str(pvdg.CostoTotaViv) if hasattr(pvdg, 'CostoTotaViv') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=96,h=5,txt='CLIENTE', border=1, align='C', fill=False)
        pdf.cell(w=100,h=5,txt=(s.IdPerfil.Nombres if hasattr(s, 'IdPerfil') else '') +' '+ (s.IdPerfil.Apellidos if hasattr(s, 'IdPerfil') else ''), border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='MODELO:', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='TIPO   '+ pvdg.Modelo if hasattr(pvdg, 'Modelo') else '', border=1, align='L', fill=True)
        pdf.cell(w=40,h=5,txt='DIMENSION DE VIVIENDA:', border=1,  align='L', fill=False)
        pdf.cell(w=0,h=5,txt=pvdg.DimensionVivi if hasattr(pvdg, 'DimensionVivi') else '', border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=96,h=5,txt='DIRECCIÓN DEL INMUEBLE:', border=1, align='L', fill=False)
        pdf.cell(w=100,h=5,txt=str(do.DireccionExac) if hasattr(do, 'DireccionExac') else '', border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)

        pdf.cell(w=15,h=5,txt='COD', border=1, align='C', fill=True)
        pdf.cell(w=81,h=5,txt='DESCRIPCION', border=1, align='C', fill=True)
        pdf.cell(w=20,h=5,txt='UNIDAD', border=1,  align='C', fill=True)
        pdf.cell(w=20,h=5,txt='P.U.', border=1,  align='C', fill=True)
        pdf.cell(w=15,h=5,txt='CANT', border=1,  align='C', fill=True)
        pdf.cell(w=25,h=5,txt='CANTIDAD TOTAL', border=1,  align='C', fill=True)
        pdf.cell(w=0,h=5,txt='SubTotal', border=1,  align='C', fill=True, ln=1)

        pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
        pdf.cell(w=161,h=5,txt='', border=1, align='C', fill=False)
        for mat in datos_materiales:
                stmat = mat["total"]
                subtot=subtot+stmat
        tot=pdf.cell(w=0,h=5,txt='$  '+str(subtot) or '', border=1,  align='R', fill=False, ln=1)

        #### Tabla de materiales
        if datos_materiales !='' and len(datos_materiales):
            for mat in datos_materiales:
                nmat = mat["nombre"]
                umat = mat["unidad"]
                pumat = mat["precio"]
                cmat = mat["cantida"]
                stmat = mat["total"]
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt=nmat, border=1, align='L', fill=False)
                pdf.cell(w=20,h=5,txt=umat, border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='$  '+str(pumat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=15,h=5,txt='$  '+str(cmat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=25,h=5,txt='$  '+str(stmat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
               
        else:
            
            for i in aux:
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)

        
        #### Tabla de mano de obra
        pdf.cell(w=15,h=5,txt='MO', border=1, align='C', fill=False)
        pdf.cell(w=161,h=5,txt='MANO DE OBRA', border=1, align='L', fill=False)
        for mo in datos_mano_obra:
                stmo = mo["total"]
                subtotmo=subtotmo+stmo
        tot=pdf.cell(w=0,h=5,txt='$  '+str(subtotmo) or '', border=1,  align='R', fill=False, ln=1)

        if datos_mano_obra !='' and len(datos_mano_obra):
            for mo in datos_mano_obra:
                dmo = mo["descripcion"]
                umo = mo["unidad"]
                pumo = mo["preciouni"]
                cmo = mo["cantidad"]
                stmo = mo["total"]
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt=dmo, border=1, align='L', fill=False)
                pdf.cell(w=20,h=5,txt=umo, border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='$  '+str(pumo) or '', border=1,  align='R', fill=False)
                pdf.cell(w=15,h=5,txt='$  '+str(cmo) or '', border=1,  align='R', fill=False)
                pdf.cell(w=25,h=5,txt='$  '+str(stmo) or '', border=1,  align='R', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
                
        else:
            
            for i in aux:
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
        
        pdf.cell(w=15,h=5,txt='A', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='MATERIALES', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+ str(pvt.Materiales) if hasattr(pvt, 'Materiales') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='B', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='MANO DE OBRA', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.ManoObra) if hasattr(pvt, 'ManoObra') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='C', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='TRANSPORTE', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.Transporte) if hasattr(pvt, 'Transporte') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='D', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='SOLUCIÓN SANITARIA', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.SolucionSani) if hasattr(pvt, 'SolucionSani') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='E', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='KIT DE EMERGENCIA', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.KitEmer) if hasattr(pvt, 'KitEmer') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='F', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='HERRAMIENTAS', border=1, align='L', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.Herramientas) if hasattr(pvt, 'Herramientas') else '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=15,h=5,txt='', border=1, align='L', fill=False)
        pdf.cell(w=81,h=5,txt='TOTAL COSTOS DIRECTOS', border=1, align='L', fill=True)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=True)
        pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=True)
        pdf.cell(w=15,h=5,txt='', border=1,  align='C', fill=True)
        pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=True)
        pdf.cell(w=0,h=5,txt='$  '+str(pvt.TotalCostDir) if hasattr(pvt, 'TotalCostDir') else '', border=1,  align='R', fill=True, ln=1)
        y=pdf.get_y()
        pdf.cell(w=0,h=70,txt='', border=1,  align='C', fill=False)


        pdf.text(x=20, y=y+13, txt='F')
        pdf.line(20, y+15, 80, y+15)
        pdf.text(x=20, y=y+20, txt='ELABORO ')
        pdf.text(x=20, y=y+25, txt='Nombre. ')
        pdf.text(x=20, y=y+30, txt='Dui')

        pdf.text(x=130, y=y+13, txt='F')
        pdf.line(130, y+15, 190, y+15)
        pdf.text(x=130, y=y+20, txt='AUTORIZO ')
        pdf.text(x=130, y=y+25, txt='Nombre. ')
        pdf.text(x=130, y=y+30, txt='Dui')

        #y=pdf.get_y()
        pdf.text(x=20, y=y+43, txt='F')
        pdf.line(20, y+45, 80, y+45)
        pdf.text(x=20, y=y+50, txt='REVISADO')
        pdf.text(x=20, y=y+55, txt='Nombre. ')
        pdf.text(x=20, y=y+60, txt='Admin ')
        pdf.text(x=20, y=y+65, txt='Dui')

        #tot.txt=str('10')
        pdf.output('presupuestoVivienda.pdf', 'F')
        return FileResponse(open('presupuestoVivienda.pdf', 'rb'), as_attachment=True, content_type='application/pdf')