from fpdf import FPDF
from datetime import date
import locale

from django.http import FileResponse
from PresupuestoVApp.models import *
from ClienteApp.models import *
from django.db.models import Q


class presupuestoVvO(FPDF):
    
    def presupuestoVO(request, id ):

        try:
            pvdgo=  PresupuestoViviDatGenObr.objects.get(Id=id)
        except PresupuestoViviDatGenObr.DoesNotExist:
            pvdgo=""

        try:
            pdg=  PresupuestoViviDatGen.objects.get(Id=pvdgo.IdPresupuestoViviDatGen.Id)
        except PresupuestoViviDatGen.DoesNotExist:
            pdg=""
        
        try:
            do= DatosObra.objects.get(IdSolicitud=pdg.IdSolicitud.Id)
        except DatosObra.DoesNotExist:
            do=""

        try:
            lista_materiales= PresupuestoViviMatObr.objects.filter(IdPresupuestoViviDatGenObr=pvdgo.Id)
            datos_materiales=[]
            for item in lista_materiales:
                datos_materiales.append ( {'id': item.Id, 'precio':item.PrecioUnit,'cantida': item.Cantidad,'total':item.SubTota,
                "nombre":item.IdMateriales.Nombre,"descripcion":item.IdMateriales.Descripcion,"unidad":item.IdMateriales.Unidad,"idm":item.IdMateriales.Id })
        except PresupuestoViviMatObr.DoesNotExist:
            lista_materiales=""

        try:
            lista_mano_obra= PresupuestoViviManObrObr.objects.filter(IdPresupuestoViviDatGenObr=pvdgo.Id)
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
        except PresupuestoViviManObrObr.DoesNotExist:
            lista_mano_obra=""

        

        r=59
        g=93
        b=149
        aux=[0, 1, 2, 3]
        aux2=[0, 1, 2]    
        subtotmat=0
        subtotmo=0
        tot=0
        
        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=10, y=12, w=55, h=30)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=0,h=8,txt='PRESUPUESTO DE OBRAS ADICIONALES', border=1,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_font('Arial', '', 7)
        pdf.cell(w=66,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=35,h=5,txt='AGENCIA:', border=1,  align='L', fill=False)
        pdf.cell(w=30,h=5,txt=pdg.IdSolicitud.IdPerfil.IdAgencia.Nombre if hasattr(pdg, 'IdSolicitud') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=40,h=5,txt='COSTO OBRA ADICIONAL=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt='$      ' + str(pvdgo.CostoObra) if hasattr(pvdgo, 'CostoObra') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=66,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=35,h=5,txt='FECHA:', border=1,  align='L', fill=False)
        pdf.cell(w=30,h=5,txt=pvdgo.Fecha.strftime("%d/%m/%Y") if hasattr(pvdgo, 'Fecha') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=40,h=5,txt='SOLUCION SANITARIA=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt=str(pvdgo.SolucionSan) if hasattr(pvdgo, 'SolucionSan') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=66,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=50,h=5,txt='TIEMPO DE CONSTRUCCION:', border=1,  align='L', fill=False)
        pdf.cell(w=15,h=5,txt=pdg.TiempoCons if hasattr(pdg, 'TiempoCons') else '', border='LR',  align='C', fill=False)
        pdf.cell(w=40,h=5,txt='COSTO TOTAL=', border=1,  align='L', fill=False)
        pdf.cell(w=20,h=5,txt='$      '+ str(pvdgo.TotalObraAdi) if hasattr(pvdgo, 'TotalObraAdi') else '', border='L',  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.set_fill_color(217,217,217)
        pdf.cell(w=66,h=5,txt='CLIENTE', border=1, align='C', fill=False)
        pdf.cell(w=0,h=5,txt= (pdg.IdSolicitud.IdPerfil.Nombres if hasattr(pdg, 'IdSolicitud') else '') +' '+ (pdg.IdSolicitud.IdPerfil.Apellidos if hasattr(pdg, 'IdSolicitud') else ''), border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=66,h=5,txt='Tipo de obra adicional:', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt=pvdgo.TipoObra if hasattr(pvdgo, 'TipoObra') else '', border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=66,h=5,txt='DIRECCIÓN DEL INMUEBLE:', border=1, align='L', fill=False)
        pdf.cell(w=0,h=5,txt=str(do.DireccionExac) if hasattr(do, 'DireccionExac') else '', border=1, align='C', fill=True, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)

        pdf.cell(w=15,h=5,txt='COD', border=1, align='C', fill=True)
        pdf.cell(w=81,h=5,txt='DESCRIPCION', border=1, align='C', fill=True)
        pdf.cell(w=25,h=5,txt='CANTIDAD', border=1,  align='C', fill=True)
        pdf.cell(w=20,h=5,txt='UNIDAD', border=1,  align='C', fill=True)
        pdf.cell(w=30,h=5,txt='PRECIO UNITARIO.', border=1,  align='C', fill=True)
        pdf.cell(w=0,h=5,txt='SUBTOTAL', border=1,  align='C', fill=True, ln=1)

        #### Tabla de materiales
        pdf.cell(w=15,h=5,txt='MAD', border=1, align='C', fill=True)
        pdf.cell(w=0,h=5,txt='MATERIALES', border=1, align='L', fill=True, ln=1)
        
        if datos_materiales !='' and len(datos_materiales):
            for mat in datos_materiales:
                nmat = mat["nombre"]
                cmat = mat["cantida"]
                umat = mat["unidad"]
                pumat = mat["precio"]
                stmat = mat["total"]
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt=nmat, border=1, align='L', fill=False)
                pdf.cell(w=25,h=5,txt='$  '+str(cmat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=20,h=5,txt=umat, border=1,  align='C', fill=False)
                pdf.cell(w=30,h=5,txt='$  '+str(pumat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=25,h=5,txt='$  '+str(stmat) or '', border=1,  align='R', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
                subtotmat=subtotmat+stmat
        else:
            
            for i in aux:
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=30,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)

        
        #### Tabla de mano de obra
        pdf.cell(w=15,h=5,txt='OAD', border=1, align='C', fill=True)
        pdf.cell(w=0,h=5,txt='MANO DE OBRA', border=1, align='L', fill=True, ln=1)

        if datos_mano_obra !='' and len(datos_mano_obra):
            for mo in datos_mano_obra:
                dmo = mo["descripcion"]
                cmo = mo["cantidad"]
                umo = mo["unidad"]
                pumo = mo["preciouni"]               
                stmo = mo["total"]
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt=dmo, border=1, align='L', fill=False)
                pdf.cell(w=25,h=5,txt='$  '+str(cmo) or '', border=1,  align='R', fill=False)
                pdf.cell(w=20,h=5,txt=umo, border=1,  align='C', fill=False)
                pdf.cell(w=30,h=5,txt='$  '+str(pumo) or '', border=1,  align='R', fill=False)              
                pdf.cell(w=25,h=5,txt='$  '+str(stmo) or '', border=1,  align='R', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
                subtotmo=subtotmo+stmo
        else:
            
            for i in aux:
                pdf.cell(w=15,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=81,h=5,txt='', border=1, align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=20,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=30,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=25,h=5,txt='', border=1,  align='C', fill=False)
                pdf.cell(w=0,h=5,txt='', border=1,  align='C', fill=False, ln=1)
        
        
        
        pdf.cell(w=171,h=5,txt='TOTAL ', border=1, align='C', fill=True)
        tot=subtotmat+subtotmo
        #tot=pdf.cell(w=0,h=5,txt='$  '+str(subtot) or '', border=1,  align='R', fill=False, ln=1)
        pdf.cell(w=0,h=5,txt='$  '+str(tot), border=1,  align='R', fill=True, ln=1)
        y=pdf.get_y()
        pdf.cell(w=0,h=70,txt='', border=1,  align='C', fill=False)


        pdf.text(x=20, y=y+13, txt='F')
        pdf.line(20, y+15, 80, y+15)
        pdf.text(x=20, y=y+20, txt='Elaborado por ')
        pdf.text(x=20, y=y+25, txt='Nombre. ')
        pdf.text(x=20, y=y+30, txt='Supervisor de construcción ')
        pdf.text(x=20, y=y+35, txt='Dui')

       

        pdf.output('presupuestoViviendaObra.pdf', 'F')
        return FileResponse(open('presupuestoViviendaObra.pdf', 'rb'), as_attachment=True, content_type='application/pdf')