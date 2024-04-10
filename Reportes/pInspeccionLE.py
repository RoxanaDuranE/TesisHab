from fpdf import FPDF
from datetime import date
import locale

from django.http import FileResponse
from InspeccionLoteApp.models import *
from PresupuestoVApp.models import *


class pinspl(FPDF):
    x=0
    y=0
    def se_desborda(self, width, height):
        # Get current position
        current_x = self.get_x()
        current_y = self.get_y()

        # Set the cell
        self.cell(width, height, '', border=1)

        # Get new position after setting cell
        new_x = self.get_x()
        new_y = self.get_y()

        # Reset the position to the original
        self.set_xy(current_x, current_y)

        # Check if the new position is different from the original
        return new_x != current_x or new_y != current_y
    
    def pInspeccionLE(request, id):
        try:
            pil=PrimeraInspLot.objects.get(Id=id)
        except PrimeraInspLot.DoesNotExist:
            pil=""
        try:
            inspeccionl=InspeccionLote.objects.get(Id=pil.IdInspeccionLote.Id)
        except InspeccionLote.DoesNotExist:
            inspeccionl=""
        try:
            pdg= PresupuestoViviDatGen.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
        except PresupuestoViviDatGen.DoesNotExist:
            pdg= ""
        try:
            do= DatosObra.objects.get(IdSolicitud=inspeccionl.IdSolicitud.Id)
        except DatosObra.DoesNotExist:
            do=""       
        try:
            DPipl = DescripcionProyInsLot.objects.get(IdInspeccionLote=inspeccionl.Id)
        except DescripcionProyInsLot.DoesNotExist:
            DPipl=""


        pdf=FPDF(orientation='P', unit='mm', format='Letter')
        pdf.add_page()
        #pdf.multi_cell(w=0, h=40, txt='', border=1)
        #Margenes de la pagina
        pdf.set_auto_page_break(auto=True, margin=5)
        pdf.set_draw_color(0,0,0)
        pdf.set_line_width(0.5)
        pdf.rect(5, 3,205,265)
     
        pdf.rect(6, 4,203,55)
        pdf.set_line_width(0.1)

        pdf.rect(10, 62,196,167)
        pdf.set_line_width(0.1)

        try:  
            # Agregar la imagen desde la instancia pil
            img_path = pil.Esquema.path  # Asumiendo pil.esquema que es un campo FileField o ImageField
            x = 11  # Coordenada horizontal 
            y = 75  # Coordenada vertical... arriba
            w = 194 # Ancho de la imagen en puntos
            h = 147  # Altura de la imagen en puntos
            pdf.image(img_path , x=x, y=y, w=w, h=h)
        except:
            pass

        pdf.image('TesisApp/static/TesisApp/images/logohabib.png', x=7, y=6, w=43, h=28)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=45,h=8,txt='', border=0, align='C', fill=False)
        pdf.cell(w=0,h=8,txt='ESQUEMA DE UBICACIÓN DEL INMUEBLE', border=1,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='', border=0, align='C', fill=False)
        pdf.cell(w=40,h=5,txt='AGENCIA:', border=1,  align='L', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt=inspeccionl.IdSolicitud.IdPerfil.IdAgencia.Nombre if hasattr(inspeccionl, 'IdSolicitud') else '', border=1,  align='L', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='', border=0, align='C', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=40,h=5,txt='FECHA:', border=1,  align='L', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt=str(pil.Fecha) if hasattr(pil, 'Fecha') else '', border=1,  align='L', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=45,h=5,txt='', border=0, align='C', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=65,h=5,txt='TIEMPO DE CONSTRUCCIÓN:', border=0,  align='L', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt=pdg.TiempoCons if hasattr(pdg, 'TiempoCons') else '', border=0,  align='C', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=40,h=5,txt='CLIENTE:', border=1, align='L', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt=(inspeccionl.IdSolicitud.IdPerfil.Nombres if hasattr(inspeccionl, 'IdSolicitud') else '') +' '+ (inspeccionl.IdSolicitud.IdPerfil.Apellidos if hasattr(inspeccionl, 'IdSolicitud') else '' ), border=1,  align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=60,h=6,txt='MODELO DE LA VIVIENDA:', border=1, align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=35,h=6,txt=DPipl.ModeloViviCon if hasattr(DPipl, 'ModeloViviCon') else '', border=1,  align='L', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=40,h=6,txt='MUNICIPIO:', border=1, align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=6,txt=inspeccionl.IdSolicitud.IdPerfil.IdDistrito.Distrito if hasattr(inspeccionl, 'IdSolicitud') else '', border=1,  align='L', fill=False, ln=1)
        pdf.set_font('Arial', 'B', 10)
        py = pdf.get_y()
        pdf.cell(w=60,h=10,txt='DIRECCIÓN DE LA MEJORA:', border=1, align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        
        x_antes = pdf.get_x() # Obtener la posición y antes de multi_cell
        pdf.multi_cell(w=70,h=5,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border='TLR',  align='L', fill=False)
        x_ancho = 70 # Obtener la posición y después de multi_cell
        x_act=x_ancho+x_antes
        pdf.set_xy(x=x_act, y=py) # Establecer la posición de inicio de la siguiente celda
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30,h=10,txt='TELÉFONO:', border=1, align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=10,txt=inspeccionl.IdSolicitud.IdPerfil.Telefono if hasattr(inspeccionl, 'IdSolicitud') else '', border=1,  align='L', fill=False, ln=1)
        #pdf.cell(w=0, h=1, txt='', border='T', ln=1)
        #pdf.cell(w=65,h=6,txt='DIRECCIÓN DE LA MEJORA:', border=1, align='C', fill=False)
        #pdf.set_font('Arial', '', 9)
        # Width and height of cell
        width = 60
        height = 6

        # Text to be added to the cell
        text = getattr(do, 'DireccionExac', '')
        #pdf.cell(w=60,h=6,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border=1,  align='L', fill=False)
        pinsplins = pinspl() 
        """if pinspl.se_desborda(width, height):
            pdf.cell(w=65,h=10,txt='DIRECCIÓN DE LA MEJORA:', border=1, align='C', fill=False)
            pdf.set_font('Arial', '', 10)
            y_after_multicell = pdf.get_y() # Obtener la posición y después de multi_cell
            pdf.multi_cell(w=60,h=5,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border=1,  align='L', fill=False)
            pdf.set_xy(x=pdf.get_x(), y=y_after_multicell) # Establecer la posición de inicio de la siguiente celda
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(w=30,h=10,txt='TELÉFONO:', border=1, align='C', fill=False)
            pdf.set_font('Arial', '', 10)
            pdf.cell(w=0,h=10,txt=inspeccionl.IdSolicitud.IdPerfil.Telefono if hasattr(inspeccionl, 'IdSolicitud') else '', border=1,  align='L', fill=False, ln=1)
        else:
            #pdf.cell(w=cell_width, h=cell_height, txt=text, border=1, align='L', fill=False)
            pdf.cell(w=65,h=6,txt='DIRECCIÓN DE LA MEJORA:', border=1, align='C', fill=False)
            pdf.set_font('Arial', '', 10)
            pdf.cell(w=60,h=6,txt=do.DireccionExac if hasattr(do, 'DireccionExac') else '', border=1,  align='L', fill=False)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(w=30,h=6,txt='TELÉFONO:', border=1, align='C', fill=False)
            pdf.set_font('Arial', '', 10)
            pdf.cell(w=0,h=6,txt=inspeccionl.IdSolicitud.IdPerfil.Telefono if hasattr(inspeccionl, 'IdSolicitud') else '', border=1,  align='L', fill=False, ln=1)
        """
        pdf.cell(w=0,h=5,txt='', border='T',  align='C', fill=False, ln=1)
        pdf.cell(w=120,h=6,txt='', border='LRT', align='C', fill=False)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=38,h=6,txt=str(inspeccionl.Latitud) if hasattr(inspeccionl, 'Latitud') else '', border=1,  align='L', fill=False)
        pdf.cell(w=38,h=6,txt=str(inspeccionl.Longitud) if hasattr(inspeccionl, 'Longitud') else '', border=1,  align='L', fill=False, ln=1)      
        pdf.cell(w=120,h=6,txt='', border='LR', align='C', fill=False)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=38,h=6,txt='LATITUD', border=1,  align='L', fill=False)
        pdf.cell(w=38,h=6,txt='LONGITUD', border=1,  align='L', fill=False, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0,h=5,txt='', border=0,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=150,txt='', border=0,  align='C', fill=False, ln=1)
        pdf.cell(w=0,h=1,txt='', border='',  align='C', fill=False, ln=1)
        pdf.cell(w=95,h=32,txt='', border=1, align='C', fill=False)
        pdf.cell(w=3,h=32,txt='', border=0, align='C', fill=False)
        pdf.cell(w=65,h=32,txt='', border=1, align='C', fill=False)
        pdf.cell(w=2,h=32,txt='', border=0, align='C', fill=False)
        pdf.cell(w=30,h=32,txt='', border=1, align='C', fill=False)

        pdf.text(x=109, y=234, txt='SELLO ')
        pdf.text(x=15, y=239, txt='F. ')
        pdf.line(15, 240, 90, 240)
        pdf.text(x=15, y=245, txt='TECNICO EN SERVICIOS CONSTRUCTIVOS ')
        
        

        pdf.output('pInspeccionLoteEsquema.pdf', 'F')
        return FileResponse(open('pInspeccionLoteEsquema.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
