import json
from fpdf import FPDF
from datetime import date
import locale
from ClienteApp.models import *
from django.http import FileResponse
from SolicitudesApp.models import *
from InspeccionLoteApp.models import *


class InspeccionL(FPDF):
    
    def inspeccionL(request, id):

        try:
            ipm=  InspeccionLote.objects.get(Id=id)
        except InspeccionLote.DoesNotExist:
            ipm=""
        try:
            s=  Solicitud.objects.get(Id=ipm.IdSolicitud.Id)
        except Solicitud.DoesNotExist:
            s=""
        
        try:
            do= DatosObra.objects.get(IdSolicitud=ipm.IdSolicitud.Id)
        except DatosObra.DoesNotExist:
            do=""
        
        try:
            vias_acceso= ViasAcceInsLot.objects.get(IdInspeccionLote=ipm)
        except ViasAcceInsLot.DoesNotExist:
            vias_acceso=""

        try:
            riesgo_distancia= RiesgosInspLot.objects.get(IdInspeccionLote=ipm)
        except RiesgosInspLot.DoesNotExist:
            riesgo_distancia=""

        try:
            factibilida_tecnica= FactibilidadInsLot.objects.get(IdInspeccionLote=ipm)
        except FactibilidadInsLot.DoesNotExist:
            factibilida_tecnica=""

        try:
            descripcion_proyecto= DescripcionProyInsLot.objects.get(IdInspeccionLote=ipm)
        except DescripcionProyInsLot.DoesNotExist:
            descripcion_proyecto=""

        try:
            resp_sol=ResponsabilidadSoliInsLot.objects.get(IdInspeccionLote=ipm)
        except ResponsabilidadSoliInsLot.DoesNotExist:
            resp_sol=""

        try:
            comentarios= ComentariosObseInsLot.objects.get(IdInspeccionLote=ipm)
        except ComentariosObseInsLot.DoesNotExist:
            comentarios=""     

        try:
            liip=InspeccionLoteConInfSanSerRie.objects.filter(IdInspeccionLote=ipm.Id)
        except InspeccionLoteConInfSanSerRie.DoesNotExist:
            liip=""
        liip_data = [
            {
                'existe': item.Existe,
                'id': item.Id,
                'idif':item.IdInfraestructura.Nombre,
            }
            for item in liip
            ]      

        lista_general=InspeccionLoteConInfSanSerRie.objects.filter(IdInspeccionLote=ipm.Id)

        lista_espacios_construcciones=[]
        for item in lista_general:
            if item.IdInfraestructura.Tipo == "2":
                lista_espacios_construcciones.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.IdInfraestructura.Nombre,})
        
        lista_infraetructura_datos=[]
        for item in lista_general:
            if item.IdInfraestructura.Tipo == "3":
                lista_infraetructura_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.IdInfraestructura.Nombre,})
        
       
        lista_saneamiento_datos=[]
        for item in lista_general:
            if item.IdInfraestructura.Tipo == "4":
                lista_saneamiento_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.IdInfraestructura.Nombre,})
             
        lista_servicios_basicos_datos=[]
        for item in lista_general:
            if item.IdInfraestructura.Tipo == "5":
                lista_servicios_basicos_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.IdInfraestructura.Nombre,})
        
        lista_riesgos_datos=[]
        for item in lista_general:
            if item.IdInfraestructura.Tipo == "6":
                lista_riesgos_datos.append ( {'existe': item.Existe, 'id': item.Id, 'idif':item.IdInfraestructura.Nombre,})
        

        
        locale.setlocale(locale.LC_TIME, '')    
        pdf=FPDF(orientation='P', unit='mm', format='Letter') 
        pdf.add_page()
        
            
        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=7, y=1, w=40, h=28)#, link=url)
        pdf.set_font('Arial', 'B', 9)      
        pdf.set_x(50)
        
        pdf.set_fill_color(207,188,188) # 1   
        pdf.multi_cell(w=140, h=5, txt='HOJA DE INSPECCIÓN PARA LOTE', border=1, align='C', fill=True)
        pdf.set_x(50)
        pdf.set_fill_color(232,221,221) # 2
        pdf.cell(w=20,h=8, txt='Agencia', border=1, fill=True)
        pdf.cell(w=50, h=8, txt=s.IdPerfil.IdAgencia.Nombre if hasattr(s, 'IdPerfil') else '', border=1)
        pdf.cell(w=15, h=4, txt='DIA', border=1, fill=True)
        pdf.cell(w=25, h=4, txt='MES', border=1, fill=True)
        pdf.cell(w=15, h=4, txt='AÑO', border=1, fill=True)
        pdf.multi_cell(w=15, h=4, txt='HORA', border=1, fill=True)
        pdf.set_xy(120, 19) # para ubicar el multicel
        
        pdf.cell(w=55, h=4, txt= ipm.Fecha.strftime("%A, %d de %B de %Y") if hasattr(ipm, 'Fecha') else '' , border='TBR', align='C')
        pdf.multi_cell(w=15, h=4, txt=str(ipm.Hora) if hasattr(ipm, 'Hora') else '', border=1)
        pdf.ln(2)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.multi_cell(w=0, h=5, txt='1. INFORMACIÓN GENERAL', border=1, align='C', fill=True)
        
        pdf.set_font('Arial', size=6)
        pdf.set_fill_color(232,221,221) # 2
        pdf.cell(w=22, h=5, txt='SOLICITANTE', border=1 , fill=True)
        pdf.cell(w=121, h=5, txt=(s.IdPerfil.Nombres if hasattr(s, 'IdPerfil') else '') +' '+ (s.IdPerfil.Apellidos if hasattr(s, 'IdPerfil') else ''), border=1)
        pdf.cell(w=19, h=5, txt='TELÉFONOS:', border='TL', fill=True)
        pdf.multi_cell(w=0, h=5, txt=(ipm.TelefonoPrim  if hasattr(ipm, 'TelefonoPrim') else '')+'; '+ (ipm.TelefonoSegu if hasattr(ipm, 'TelefonoSegu') else ''), border='TR')
        pdf.cell(w=25, h=5, txt='GRUPO FAMILIAR', border='TBL', align='C' , fill=True)
        pdf.cell(w=25, h=5, txt='TERCERA EDAD:', border='BT')
        pdf.cell(w=5, h=5, txt=ipm.TerceraEdad if hasattr(ipm, 'TerceraEdad') else '', border='BT')
        pdf.cell(w=17, h=5, txt='ADULTOS:', border='BT')
        pdf.cell(w=5, h=5, txt=ipm.Adultos if hasattr(ipm, 'Adultos') else '', border='BT')
        pdf.cell(w=13, h=5, txt='NIÑOS:', border='BT')
        pdf.cell(w=5, h=5, txt=ipm.Ninos if hasattr(ipm, 'Ninos') else '', border='BT')
        pdf.cell(w=48, h=5, txt='PERSONAS CON DISCAPACIDAD:', border='BT', align='C')
        pdf.multi_cell(w=0, h=5, txt=ipm.PersonaDisc if hasattr(ipm, 'PersonaDisc') else '', border='BTLR')
        #pdf.multi_cell(w=0, h=5, txt=ipm.telefonos, border='BLR')
        pdf.cell(w=22, h=8, txt='DIRECCIÓN', border=1, fill=True)
        pdf.cell(w=110, h=8, txt=str(do.DireccionExac) if hasattr(do, 'DireccionExac') else '', border=1)
        pdf.cell(w=0, h=4, txt='MUNICIPIO', border=1 , fill=True)
        pdf.set_xy(142, 44)
        pdf.multi_cell(w=0, h=4, txt=s.IdPerfil.IdDistrito.Distrito if hasattr(s, 'IdPerfil') else '', border=1)
        
        pdf.cell(w=40, h=5, txt='PROPIETARIO DEL TERRENO', border=1, fill=True)
        pdf.multi_cell(w=0, h=5, txt=ipm.PropietarioTerr if hasattr(ipm, 'PropietarioTerr') else '' , border=1)
        pdf.cell(w=70, h=5, txt='LATITUD/LONGITUD', border=1, align='C' , fill=True)
        
        pdf.cell(w=25, h=10, txt='INMUEBLE', border=1, align='C', fill=True)
        pdf.cell(w=30, h=5, txt='RURAL', border='TL', align='L')
        pdf.set_fill_color(0,0,0) # color negro   
        if ipm.Inmueble=='Urbano':
            pdf.ellipse(120,54,3,3, '') # rural
            pdf.ellipse(120,58.5,3,3, 'F') # urbano
        elif ipm.Inmueble=='Rural':
            pdf.ellipse(120,54,3,3, 'F') # rural
            pdf.ellipse(120,58.5,3,3, '') # urbano
        else:
            pdf.ellipse(120,54,3,3, '') # rural
            pdf.ellipse(120,58.5,3,3, '') # urbano

        pdf.set_fill_color(232,221,221) # 2
        pdf.cell(w=55, h=5, txt='EXISTEN OTRAS VIVIENDAS', border=1, align='C' , fill=True)
        
        pdf.multi_cell(w=0, h=5, txt=ipm.ExisteOtraViv if hasattr(ipm, 'ExisteOtraViv') else '', border=1, align='C')
        pdf.cell(w=70, h=5, txt=(ipm.Latitud if hasattr(ipm, 'Latitud') else '') +'; '+ (ipm.Longitud if hasattr(ipm, 'Longitud') else ''), border=1, align='C')
        
        pdf.set_xy(105, 58)
        pdf.cell(w=30, h=5, txt='URBANO', border='BL', align='L')
        pdf.set_xy(135, 58)
        pdf.cell(w=55, h=5, txt='TERRENO AGRICOLA', border=1, align='C' , fill=True)
        pdf.multi_cell(w=0, h=5, txt=ipm.TerrenoAgri if hasattr(ipm, 'TerrenoAgri') else '', border=1, align='C')
        
        
        pdf.cell(w=80, h=5, txt='DIMENSIONES DISPONIBLES PARA CONSTRUIR VIVIENDA', border=1, align='L', fill=True)
        pdf.cell(w=20, h=5, txt='ANCHO(M):', border=1, align='L')
        pdf.cell(w=20, h=5, txt=ipm.AnchoConsViv if hasattr(ipm, 'AnchoConsViv') else '', border=1, align='C')
        pdf.cell(w=20, h=5, txt='LARGO(M):', border=1, align='L')
        pdf.cell(w=20, h=5, txt=ipm.LargoConsViv if hasattr(ipm, 'LargoConsViv') else '', border=1, align='C')
        pdf.cell(w=20, h=5, txt='AREA(M2):', border=1, align='L')
        pdf.multi_cell(w=0, h=5, txt=ipm.AreaConsViv if hasattr(ipm, 'AreaConsViv') else '', border=1, align='C')
        pdf.cell(w=80, h=5, txt='DIMENSIONES DISPONIBLES PARA AMPLIACIONES FUTURAS', border=1, align='L', fill=True)
        pdf.cell(w=20, h=5, txt='ANCHO(M):', border=1, align='L')
        pdf.cell(w=20, h=5, txt=ipm.AnchoAmplFut if hasattr(ipm, 'AnchoAmplFut') else '', border=1, align='C')
        pdf.cell(w=20, h=5, txt='LARGO(M):', border=1, align='L')
        pdf.cell(w=20, h=5, txt=ipm.LargoAmplFut if hasattr(ipm, 'LargoAmplFut') else '', border=1, align='C')
        pdf.cell(w=20, h=5, txt='AREA(M2):', border=1, align='L')
        pdf.multi_cell(w=0, h=5, txt=ipm.AreaAmplFut if hasattr(ipm, 'AreaAmplFut') else '', border=1, align='C')
        pdf.ln(2)
        
        pdf.ln(1)
        pdf.set_font('Arial','B',size=7)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.cell(w=55, h=5, txt='2. CONSTRUCCIONES', border=1, align='L', fill=True)      
        pdf.cell(w=7.5, h=5, txt='SI', border='LBT', align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='NO', border='TBR', align='C', fill=True)
        #pdf.set_font('Arial', size=6)
        pdf.set_fill_color(0,0,0) # color negro 
        pdf.cell(w=3, h=5, txt='', border='LR')
        txi=pdf.get_x()
        pdf.set_fill_color(207,188,188) # 1 
        pdf.cell(w=45, h=5, txt='3. INFRAESTRUCTURA', border=1, align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='SI', border='LBT', align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='NO', border='TBR', align='C', fill=True)
        pdf.set_fill_color(0,0,0) # color negro 
        pdf.set_font('Arial','B',size=7)
        pdf.cell(w=3, h=5, txt='', border='LR')
        txs=pdf.get_x()
        pdf.set_fill_color(207,188,188) # 1 
        pdf.cell(w=40, h=5, txt='4. SANEAMIENTO', border=1,  align='L', fill=True)
        pdf.cell(w=7.5, h=5, txt='SI', border='LBT', align='C', fill=True)
        pdf.multi_cell(w=0, h=5, txt='NO', border='TBR', align='C', fill=True)
        
        pdf.set_fill_color(0,0,0) # color negro 
        #Fila 1
        ty=pdf.get_y()
        y=pdf.get_y()
        
        #### TABLA CONSTRUCCIONES
        for esp in lista_espacios_construcciones:
            ex = esp["existe"]
            idif=esp["idif"]
            yt=pdf.get_y()
            pdf.multi_cell(w=55, h=4, txt=idif, border='LTB', align='L')
            yy=pdf.get_y()
            xt=pdf.get_x()
            pdf.set_xy(65, yt)
                        
            if yy > yt + 4:
                pdf.multi_cell(w=7.5, h=8, txt='', border='LBT', align='C')
                pdf.set_xy(72.5, yt)
                pdf.multi_cell(w=7.5, h=8, txt='', border='TBR', align='C')
            else: 
                pdf.multi_cell(w=7.5, h=4, txt='', border='LBT', align='C')
                pdf.set_xy(72.5, yt)
                pdf.multi_cell(w=7.5, h=4, txt='', border='TBR', align='C')
            

            if (ex=='Si'):
                pdf.ellipse(67,y+0.5,3,3, 'F')
                pdf.ellipse(75,y+0.5,3,3, '')
            else:
                pdf.ellipse(67,y+0.5,3,3, '')
                pdf.ellipse(75,y+0.5,3,3, 'F')
            y=y+4

        ##### TABLA INFRAESTRUCTURA
        pdf.set_xy(txi, ty)
        y=ty
        for esp in lista_infraetructura_datos:
            ex = esp["existe"]
            
            idif=esp["idif"]
            pdf.set_x(txi)
            pdf.cell(w=45, h=4, txt=idif, border='LTB', align='L')
            pdf.cell(w=7.5, h=4, txt='', border='LBT', align='C')
            pdf.multi_cell(w=7.5, h=4, txt='', border='TBR', align='C')
            
            if (ex=='Si'):
                pdf.ellipse(130,y+0.5,3,3, 'F')
                pdf.ellipse(138,y+0.5,3,3, '')
            else:
                pdf.ellipse(130,y+0.5,3,3, '')
                pdf.ellipse(138,y+0.5,3,3, 'F')
            y=y+4


        #### TABLA SANEAMIENTO
        pdf.set_xy(txs, ty)
        y=ty
        for esp in lista_saneamiento_datos:
            ex = esp["existe"]
            #es= inm["estado"]
            idif=esp["idif"]
            pdf.set_x(txs)
            pdf.cell(w=40, h=4, txt=idif, border='LTB', align='L')
            pdf.cell(w=7.5, h=4, txt='', border='LBT', align='C')
            pdf.multi_cell(w=0, h=4, txt='', border='TBR', align='C')
            

            if (ex=='Si'):
                pdf.ellipse(188,y+0.5,3,3, 'F')
                pdf.ellipse(198,y+0.5,3,3, '')
            else:
                pdf.ellipse(188,y+0.5,3,3, '')
                pdf.ellipse(198,y+0.5,3,3, 'F')
            y=y+4

        #Fila 2
        

        #para hacer el for y que las rueditas se vayan moviendo de posicion tiene que crear una variable y=80.5 e irle sumando 4 cada vez que recorra el for

        pdf.ln(5)

        pdf.set_font('Arial','B',size=7)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.cell(w=55, h=5, txt='5. SERVICIOS BASICOS', border=1, align='L', fill=True)
        pdf.cell(w=7.5, h=5, txt='SI', border='LBT', align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='NO', border='TBR', align='C', fill=True)
        #pdf.set_font('Arial', size=6)
        pdf.set_fill_color(0,0,0) # color negro
        pdf.cell(w=3, h=5, txt='', border='LR')
        txi=pdf.get_x()
        pdf.set_fill_color(207,188,188) # 1 
        pdf.cell(w=45, h=5, txt='6. RIESGOS', border=1, align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='SI', border='LBT', align='C', fill=True)
        pdf.cell(w=7.5, h=5, txt='NO', border='TBR', align='C', fill=True)
        pdf.set_fill_color(0,0,0) # color negro
        pdf.set_font('Arial','B',size=7)  
        pdf.cell(w=3, h=5, txt='', border='LR')
        txs=pdf.get_x()
        pdf.set_fill_color(207,188,188) # 1 
        pdf.multi_cell(w=0, h=5, txt=' COMENTARIOS / OBSERVACIONES', border=1,  align='L', fill=True)

        pdf.set_fill_color(0,0,0) # color negro       
        #### TABLA CONSTRUCCIONES
        ty=pdf.get_y()
        y=ty
        for esp in lista_servicios_basicos_datos:
            ex = esp["existe"]
            #es= inm["estado"]
            idif=esp["idif"]
            #pdf.set_x(155)
            pdf.cell(w=55, h=4, txt=idif, border='LTB', align='L')
            pdf.cell(w=7.5, h=4, txt='', border='LBT', align='C')
            pdf.multi_cell(w=7.5, h=4, txt='', border='TBR', align='C')
            

            if (ex=='Si'):
                pdf.ellipse(67,y+0.5,3,3, 'F')
                pdf.ellipse(75,y+0.5,3,3, '')
            else:
                pdf.ellipse(67,y+0.5,3,3, '')
                pdf.ellipse(75,y+0.5,3,3, 'F')
            y=y+4
        pdf.multi_cell(w=70, h=5, txt='', border=1,  align='L')
        pdf.multi_cell(w=70, h=15, txt='', border=1,  align='L')
        ys=pdf.get_y()

        pdf.set_xy(txi, ty)
        y=ty
        for esp in lista_riesgos_datos:
            ex = esp["existe"]
            #es= inm["estado"]
            idif=esp["idif"]
            pdf.set_font('Arial','',size=6)
            pdf.set_x(txi)
            pdf.cell(w=45, h=4, txt=idif, border='LTB', align='L')
            pdf.cell(w=7.5, h=4, txt='', border='LBT', align='C')
            pdf.multi_cell(w=7.5, h=4, txt='', border='TBR', align='C')
            
            if (ex=='Si'):
                pdf.ellipse(130,y+0.5,3,3, 'F')
                pdf.ellipse(138,y+0.5,3,3, '')
            else:
                pdf.ellipse(130,y+0.5,3,3, '')
                pdf.ellipse(138,y+0.5,3,3, 'F')
            y=y+4
        
        pdf.set_x(txi)
        
        pdf.cell(w=45, h=4, txt='DISTANCIA A TALUDES(m)', border='LRT', align='L')
        pdf.multi_cell(w=15, h=4, txt=str(riesgo_distancia.DistanciaTalu) or '0', border=1,  align='C')
        
        pdf.set_x(txi)
        pdf.cell(w=45, h=4, txt='DISTANCIA A RIOS CERCANOS(m)', border='LR', align='L')
        pdf.multi_cell(w=15, h=4, txt=str(riesgo_distancia.DistanciaRiosCer) or '0', border=1,  align='C')
        
        pdf.set_x(txi)
        pdf.cell(w=45, h=4, txt='DISTANCIA A LADERAS CERCANAS(m)', border='LR', align='L')
        pdf.multi_cell(w=15, h=4, txt=str(riesgo_distancia.DistanciaLadeCer) or '0', border=1,  align='C')
        
        pdf.set_x(txi)
        pdf.cell(w=45, h=4, txt='DISTANCIA A TORRES O ANTENAS(m)', border='LR', align='L')
        pdf.cell(w=15, h=4, txt=str(riesgo_distancia.DistanciaTorrAnt) or '0', border=1,  align='C')
        
        pdf.set_x(txi)
        pdf.multi_cell(w=60, h=4, txt='', border='LRB',  align='L')
        yr=pdf.get_y()
        

        pdf.set_xy(txs, ty)
        y=ty
        pdf.multi_cell(w=0, h=4, txt=comentarios.Comentarios if hasattr(comentarios, 'Comentarios') else '', border='LTR', align='L')
        pdf.set_x(txs)
        pdf.multi_cell(w=0, h=4, txt=comentarios.Observaciones if hasattr(comentarios, 'Observaciones') else '', border='LRB', align='L')
        yc=pdf.get_y()
       
        if ys>yr and ys>yc:
            y=ys
        elif yr>ys and yr>yc:
            y=yr
        else:
            y=yc
        pdf.set_y(y)
        pdf.ln(2)
        pdf.set_font('Arial','B',size=7)
        pdf.set_fill_color(232,221,221) # 2
        pdf.cell(w=27, h=5, txt='7. VIAS DE ACCESO', border='TLB', fill=True)
        pdf.set_font('Arial','',size=7)
        pdf.set_fill_color(0,0,0) # color negro 
        y=pdf.get_y()
        pdf.multi_cell(w=0, h=5, txt='                  CARRETERA / CALLE PAVIMENTADA                      CALLE RURAL                     SERVIDUMBRE                       PASAJE PEATONAL   ', border='TBR')
        
        ty=y+1
        if(vias_acceso.TipoVias=='Carretera / Calle Paviment'):
            pdf.ellipse(46,ty, 3,3, 'F') # calle pavimentada
            pdf.ellipse(105,ty,3,3, '') # calle rural
            pdf.ellipse(136,ty,3,3, '') # servidumbre
            pdf.ellipse(170,ty,3,3, '') # pasaje peatonal
        elif(vias_acceso.TipoVias=='Calle Rural'):
            pdf.ellipse(46,ty, 3,3, '') # calle pavimentada
            pdf.ellipse(105,ty,3,3, 'F') # calle rural
            pdf.ellipse(136,ty,3,3, '') # servidumbre
            pdf.ellipse(170,ty,3,3, '') # pasaje peatonal
        elif(vias_acceso.TipoVias=='Servidumbre'):
            pdf.ellipse(46,ty, 3,3, '') # calle pavimentada
            pdf.ellipse(105,ty,3,3, '') # calle rural
            pdf.ellipse(136,ty,3,3, 'F') # servidumbre
            pdf.ellipse(170,ty,3,3, '') # pasaje peatonal
        elif(vias_acceso.TipoVias=='Pasaje Peatonal'):
            pdf.ellipse(46,ty, 3,3, '') # calle pavimentada
            pdf.ellipse(105,ty,3,3, '') # calle rural
            pdf.ellipse(136,ty,3,3, '') # servidumbre
            pdf.ellipse(170,ty,3,3, 'F') # pasaje peatonal
        else:
            pdf.ellipse(46,ty, 3,3, '') # calle pavimentada
            pdf.ellipse(105,ty,3,3, '') # calle rural
            pdf.ellipse(136,ty,3,3, '') # servidumbre
            pdf.ellipse(170,ty,3,3, '') # pasaje peatonal
        #pdf.cell(w=0, h=5, txt='', border=0, ln=1)
        #pdf.ln(2)
        pdf.set_font('Arial','B',size=7)
       
        
        pdf.ln(2)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.multi_cell(w=0, h=4, txt='8.FACTIBILIDAD TECNICA DEL PROYECTO', border=1, align='C', fill=True)
        
        pdf.set_fill_color(0,0,0) # color negro 
        y=pdf.get_y()
        pdf.cell(w=10, h=4, txt='', border='TLB', align='C')
        pdf.cell(w=60, h=4, txt='PROCEDE', border='TB', align='L')
        
        pdf.cell(w=50, h=4, txt='NO PROCEDE', border='TB', align='C')
        pdf.multi_cell(w=0, h=4, txt=' PARA CASO ESPECIAL', border='TBR', align='C')
        y=y+0.5
        if (factibilida_tecnica.Detalle =='Procede'):
            pdf.ellipse(17,y,3,3, 'F') # Procede
            #pdf.ellipse(48.5,y,3,3, '') # Procede con Condicionamiento
            pdf.ellipse(92,y,3,3, '') #  No Procede
            pdf.ellipse(150.5,y,3,3, '') # Para Caso Especial
        
        elif(factibilida_tecnica.Detalle=='No Procede'):
            pdf.ellipse(17,y,3,3, '') # Procede
            #pdf.ellipse(48.5,y,3,3, '') # Procede con Condicionamiento
            pdf.ellipse(92,y,3,3, 'F') #  No Procede
            pdf.ellipse(150.5,y,3,3, '') # Para Caso Especial
        elif(factibilida_tecnica.Detalle=='Para Caso Especial'):
            pdf.ellipse(17,y,3,3, '') # Procede
            #pdf.ellipse(48.5,y,3,3, '') # Procede con Condicionamiento
            pdf.ellipse(92,y,3,3, '') #  No Procede
            pdf.ellipse(150.5,y,3,3, 'F') # Para Caso Especial
        else:
            pdf.ellipse(17,y,3,3, '') # Procede
            #pdf.ellipse(48.5,y,3,3, '') # Procede con Condicionamiento
            pdf.ellipse(92,y,3,3, '') #  No Procede
            pdf.ellipse(150.5,y,3,3, '') # Para Caso Especial

        pdf.ln(4)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.multi_cell(w=0, h=4, txt='9. DESCRIPCIÓN DELPROYECTO', border=1, align='C', fill=True)
        pdf.set_fill_color(232,221,221) # 2
        pdf.cell(w=60, h=4, txt='MODELO DE VIVIENDA A CONSTRUIR', border=1, align='C', fill=True)
        pdf.multi_cell(w=0, h=4, txt=descripcion_proyecto.ModeloViviCon if hasattr(descripcion_proyecto, 'ModeloViviCon') else '', border=1, align='L')
        pdf.cell(w=60, h=4, txt='SOLUCION SANITARIA PROPUESTA', border=1, align='C', fill=True)
        pdf.multi_cell(w=0, h=4, txt=descripcion_proyecto.SolucionSaniPro if hasattr(descripcion_proyecto, 'SolucionSaniPro') else '', border=1, align='L')
        pdf.cell(w=60, h=4, txt='OBRAS ADICIONALES A CONSTRUIR', border=1, align='C', fill=True)
        x=pdf.get_x()
        pdf.multi_cell(w=0, h=4, txt=descripcion_proyecto.ObrasAdicCon if hasattr(descripcion_proyecto, 'ObrasAdicCon') else '', border=1, align='L')
        y=pdf.get_y()
        pdf.multi_cell(w=60, h=4, txt='OBSERVACIONES TECNICAS GENERALES Y/O CONDICIONAMIENTOS', border=1, align='C', fill=True)
        pdf.set_xy(x, y)
        pdf.multi_cell(w=0, h=8, txt=descripcion_proyecto.ObservacionesTecn if hasattr(descripcion_proyecto, 'ObservacionesTecn') else '', border=1, align='L')
        pdf.multi_cell(w=0, h=4, txt='DESCRIPCION DE ACTIVIDADES BAJO LA RESPONSABILIDAD DEL FUTURO PROPIETARIO ANTES DE INICIAR LA CONSTRUCCION:', border=1, align='C', fill=True)
        pdf.multi_cell(w=0, h=4, txt=descripcion_proyecto.ActividadRespFia if hasattr(descripcion_proyecto, 'ActividadRespFia') else '', border=1, align='L', fill=False)
        pdf.set_fill_color(207,188,188) # 1 
        pdf.multi_cell(w=0, h=4, txt='10. RESPONSABILIDADES DEL SOLICITANTE (EL O LA SOLICITANTE SE COMPROMETE A FACILITAR):', border=1, align='C', fill=True)
        pdf.set_fill_color(0,0,0) # color negro 
        pdf.set_font('Arial','',size=6)
        pdf.cell(w=40, h=4, txt='MOJONES DEL LOTE', border=1, align='C')
        y=pdf.get_y()
        pdf.cell(w=20, h=4, txt='SI  /  NO', border=1, align='C')
        pdf.cell(w=70, h=4, txt='RESGUARDO DE MATERIALES Y HERRAMIENTAS', border=1, align='C')
        pdf.cell(w=20, h=4, txt='SI  /  NO', border=1, align='C')
        pdf.cell(w=30, h=4, txt='AGUA POTABLE', border=1, align='C')
        pdf.multi_cell(w=0, h=4, txt='SI  /  NO', border=1, align='C')
        if resp_sol.MojonesLote == 'Si':
            pdf.ellipse(55,y,4,4, '')
        else:
            pdf.ellipse(60.5,y,4,4, '')
        
        if resp_sol.ResguardoMate == 'Si':
            pdf.ellipse(145,y,4,4, '')
        else:
            pdf.ellipse(150.5,y,4,4, '')

        if resp_sol.AguaPota == 'Si':
            pdf.ellipse(193,y,4,4, '')
        else:
            pdf.ellipse(198.5,y,4,4, '')
        pdf.cell(w=40, h=4, txt='LINDEROS DEL LOTE', border=1, align='C')
        y=pdf.get_y()
        pdf.cell(w=20, h=4, txt='SI  /  NO', border=1, align='C')
        pdf.cell(w=70, h=4, txt='AUXILIARES DE CONSTRUCCION', border=1, align='C')
        pdf.cell(w=20, h=4, txt='SI  /  NO', border=1, align='C')
        pdf.cell(w=30, h=4, txt='ENERGIA ELECTRICA', border=1, align='C')
        pdf.multi_cell(w=0, h=4, txt='SI  /  NO', border=1, align='C')
        #pdf.set_y(y)
        if resp_sol.LinderosLote == 'Si':
            pdf.ellipse(55,y,4,4, '')
        else:
            pdf.ellipse(60.5, y,4,4, '')

        if resp_sol.AuxiliaresCons == 'Si':
            pdf.ellipse(145,y,4,4, '')
        else:
            pdf.ellipse(150.5,y,4,4, '')
        
        if resp_sol.EnergiaElec== 'Si':
            pdf.ellipse(193,y,4,4, '')
        else:
            pdf.ellipse(198.5,y,4,4, '')
            
        
        pdf.ln(3)
        pdf.cell(w=70, h=3, txt='REALIZO LA INSPECCION', border='TLR')
        pdf.cell(w=25, h=3, txt='', border=0)
        pdf.cell(w=70, h=3, txt='ATENCIO LA VISITA', border=1)
        pdf.multi_cell(w=0, h=3, txt='', border=0, align='C')
        pdf.cell(w=70, h=6, txt='F:', border='LBR', align='L')
        pdf.cell(w=25, h=6, txt='', border=0)
        pdf.cell(w=70, h=6, txt='F:', border='LBR')
        pdf.multi_cell(w=0, h=6, txt='', border=0, align='C')
        pdf.cell(w=70, h=6, txt='NOMBRE:', border='LBR', align='L')
        pdf.cell(w=25, h=6, txt='', border=0)
        pdf.cell(w=70, h=6, txt='NOMBRE:', border='LBR')
        pdf.multi_cell(w=0, h=6, txt='', border=0, align='C')
        pdf.cell(w=70, h=6, txt='DUI:', border='LBR', align='L')
        pdf.cell(w=25, h=6, txt='', border=0)
        pdf.cell(w=70, h=6, txt='DUI:', border='LBR')
        pdf.multi_cell(w=0, h=6, txt='', border=0, align='C')
        
        
        pdf.output('InspeccionLote.pdf', 'F')
        return FileResponse(open('InspeccionLote.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

