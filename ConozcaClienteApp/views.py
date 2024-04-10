from django.shortcuts import render,redirect, HttpResponse
from ClienteApp.models import Perfil
from ConozcaClienteApp.models import *
from SolicitudesApp.models import *
from DireccionApp.models import *
from datetime import date, datetime
from django.contrib import messages
from ConfiguracionApp.models import Ocupacion

from TesisApp.views import registroBit


# Create your views here.

def ccliente(request, id):
    sol= ClienteDatoGen.objects.filter(IdSolicitud=id,CalidadActu="Cliente").exists() # comprueba si en la tabla existe el registro de la solicitud
    if sol == True :
        solv= ClienteDatoGen.objects.get(IdSolicitud=id)
    
        return redirect('editarCliente', id=solv.Id)
    else:
        try:
            s=  Solicitud.objects.get(Id=id)
        except Solicitud.DoesNotExist:
            s=""
        
        try:
            d=  Domicilio.objects.get(IdSolicitud=id, Tipo="Solicitante")
        except Domicilio.DoesNotExist:
            d=""
        try:
            r= Referencias.objects.filter(IdSolicitud=id)
        except Referencias.DoesNotExist:
            r=""
        try:
            dp=DatosPers.objects.get(IdSolicitud=id)
        except DatosPers.DoesNotExist:
            dp=""

        try:
            dpcy=DatosPersFia.objects.get(IdSolicitud=id, Tipo="conyuge")
        except DatosPersFia.DoesNotExist:
            dpcy=""

        try:
            dpc=DatosPersFia.objects.get(IdSolicitud=id, Tipo="codeudor")
        except DatosPersFia.DoesNotExist:
            dpc=""
        try:
            listao=Ocupacion.objects.filter(Estado="activo")
        except Ocupacion.DoesNotExist:
            listao=""

        sol = [s, d, r, dpcy, dp, dpc]

        return render(request, "ConozcaClienteApp/cclientedg.html", {"ocupaciones":listao,"sol":sol}) 

def cclientedgf(request): # carga la vista para completar el formulario codeudor
    id=request.GET['idsol']
    fsol= ClienteDatoGen.objects.filter(IdSolicitud=id,CalidadActu="Fiador").exists() 
    if fsol == '' :
        solv= ClienteDatoGen.objects.get(IdSolicitud=id)
    
        return redirect('editarCliente', id=solv.Id)
    else:
        try:
            d=  Domicilio.objects.get(IdSolicitud=id, Tipo="codeudor")
        except Domicilio.DoesNotExist:
            d=""

        try:
            dp=DatosPersFia.objects.get(IdSolicitud=id, Tipo="codeudor")
        except DatosPersFia.DoesNotExist:
            dp=""
        try:
            listao=Ocupacion.objects.filter(Estado="activo")
        except Ocupacion.DoesNotExist:
            listao=""

        return render(request, "ConozcaClienteApp/cclientedgf.html",{"ocupaciones":listao,"d":d,"dp":dp}) 


def registrarD(request): 
  
    ids=request.POST['ids']
    codigo=request.POST['codigo']
    
    nombrecc=request.POST['nombre']
    try:
        conocidocomo=request.POST['conocidoc']
    except :
        conocidocomo=""
    try:
        calidadactua=request.POST['calidad']
    except :
        calidadactua="Cliente"
    profesiondui =request.POST['profesionsd']
    idocu=Ocupacion.objects.get(Id=profesiondui) 
    
    nacionalidad=request.POST['nacionalidad']
    docidentidad=request.POST['documento']
    numerodoc=request.POST['ndoc']
    fechavdoc=request.POST['fechavd']
    direcciondomic=request.POST['direcciond']
    correoe=request.POST['correo']
    telcelular=request.POST['telefonoc']
    telfijo=request.POST['telefonof']
    estatusp=request.POST['estatusp']
    try:
        nombrecony=request.POST['nombrecony']
    except :
        nombrecony=""

    fecha= date.today()
    estado= request.POST['estadoM']
    
    idsol= Solicitud.objects.get(Id=ids)
    
    
    clientedg=ClienteDatoGen.objects.create(Fecha=fecha,Codigo=codigo,
                                            CalidadActu=calidadactua,
                                            NombreConzCli=nombrecc,
                                            ConocidoComo=conocidocomo,
                                            Nacionalidad=nacionalidad,
                                            DocumentoIden=docidentidad,
                                            NumeroDocu=numerodoc,
                                            FechaVencdoc=fechavdoc,
                                            DireccionDomi=direcciondomic,
                                            CorreoElec=correoe,
                                            TelefonoCelu=telcelular,
                                            TelefonoFijo=telfijo,
                                            EstatusProp=estatusp,
                                            NombreCony=nombrecony,
                                            Estado=estado,
                                            IdSolicitud=idsol)
   
    
    idsol.Id=ids
    if(calidadactua =="Cliente"):
        perfil = Perfil.objects.get(Id=idsol.IdPerfil.Id)
        perfil.IdOcupacionDUI=idocu
        perfil.save()
    else:
        fiador = DatosPersFia.objects.get(IsSolicitud =idsol.IdPerfil.Id)
        fiador.IdOcupacionDUIFia=idocu
        fiador.save()

    registroBit(request, "Llenado de formulario Conozca a su cliente", Nivel="Registro")

    iddgen= ClienteDatoGen.objects.all().last() #obtengo la ultima solicitud registrada 
   
    bandera= request.POST['passAED']  # guarda los datos de la empr
    if(bandera == '1'):
        tipoact= request.POST['tipoa']
        lugartrab= request.POST['lugart']
        cargodes= request.POST['cargode']         
        tiempolaborar= request.POST['tiempolab']
        procedenciafod= request.POST['procedenciafonda']
        rangoingresosemp= request.POST['rangoing']
        otrosingresos= request.POST['otingresos']
        try:
            procedenciaoi= request.POST['procedencia']
        except :
            procedenciaoi=""   

        estado="curso"

        clienteaec=ClienteActiEco.objects.create(IdClienteDatoGen=iddgen,TipoActi=tipoact,LugarTrab=lugartrab,CargoDese=cargodes,TiempoLabo=tiempolaborar,ProcedenciaFond= procedenciafod,RangoIngrMen=rangoingresosemp,OtrosIngr=otrosingresos,ProcedenciaOtroIng=procedenciaoi,Estado=estado)
   

    bandera= request.POST['passDN']  # guarda los datos de la empresa
    if(bandera == '1'):
        try:
            nombreneg= request.POST['nombreng'] 
        except :
            nombreneg==""
        try: 
            prodserv= request.POST['descps']
        except :
            prodserv=""
        try:
            direccionneg= request.POST['direccionneg']
        except :
            direccionneg=""
        try:
            fechaia= request.POST['fechaia']
        except :
            fechaia=""

        if(fechaia=="" ):
            fechaia = None 
        try:
            rangoingresos= request.POST['rangoimn']
        except :
            rangoingresos=""
        try:
            otrosingresos= request.POST['otrosidn']
        except :
            otrosingresos=""
        try:
            procedenciaoi= request.POST['procedenciadn']
        except :
            procedenciaoi=""   
    
        estado="curso"

        clientedn=ClienteDatoNeg.objects.create(IdClienteDatoGen=iddgen,NombreNego=nombreneg,ProductoServ=prodserv,DireccionNego=direccionneg,FechaInicAct=fechaia,RangoIngrMen=rangoingresos,OtrosIngrMen=otrosingresos,ProcedenciaOtroIng=procedenciaoi,Estado=estado)
   
    bandera= request.POST['passRRF']  # guarda los datos de la empresa
    if(bandera == '1'):
        rremesa= request.POST['reciberf']  
        nombreremitente= request.POST.getlist('nombrer')
        parentesco= request.POST.getlist('parentescor')
        paisorigenr= request.POST.getlist('paisorg')
        monto= request.POST.getlist('montor') 
        estado="curso"    

        if(rremesa=="Si"):  
            for i in range(len(nombreremitente)):
                if (nombreremitente[i] != ""):
                    clienterrf=ClienteReciRemFam.objects.create(IdClienteDatoGen=iddgen,RecibeReme=rremesa,NombreRemi=nombreremitente[i],Parentesco=parentesco[i],PaisOrig=paisorigenr[i],Monto=monto[i],Estado=estado)
        elif(rremesa=="No"): 
            clienterrf=ClienteReciRemFam.objects.create(IdClienteDatoGen=iddgen,RecibeReme=rremesa,NombreRemi=" ",Parentesco=" ",PaisOrig=" ",Monto=" ",Estado=estado)
   

    bandera= request.POST['passDCF']  # guarda los datos del cliente o fiador
    if(bandera == '1'):
        try:
            clasifcredito= request.POST['clasificacionc']  
        except:
            clasifcredito=""
        try:
            montodc= request.POST['montodc']
        except:
            montodc=""
        try:        
            cuotadc= request.POST['cuotadc']
        except:
            cuotadc=""
            
        rpagosadic= request.POST['rpagosadic'] 

        try:
            procpagosadic= request.POST['procfondos']
        except:
            procpagosadic=""
    
        estado="curso"

        clientedc=ClienteDeclCli.objects.create(IdClienteDatoGen=iddgen,ClasificacionCred=clasifcredito,MontoDeclCli=montodc, CuotaDeclCli=cuotadc,RealizarPagoAdi=rpagosadic,ProcedenciaPagoAdi=procpagosadic,Estado=estado)
   
    bandera= request.POST['passBPEP']  # guarda los datos del cliente o fiador
    if(bandera == '1'):
        try:
            noaplica= request.POST['noaplica'] 
        except:
            noaplica="" 
        try:
            nombrecomp= request.POST['nombrecb']
        except:
            nombrecomp=""
        try:
            direccionp= request.POST['direcpermanente']
        except:
            direccionp=""
        try:
            tdocumento= request.POST['tdocumento']
        except:
            tdocumento=""
        try:
            ndocumento= request.POST['ndocumento']
        except:
            ndocumento=""
        try:
            benefpeps= request.POST['beneficiariopeps']
        except:
            benefpeps=""
        estado="curso"

        clientepbo=ClientePersBen.objects.create(IdClienteDatoGen=iddgen,NoApli=noaplica,NombreComp=nombrecomp, DireccionPerm=direccionp,TipoDocuPers=tdocumento,NumeroDocuPers=ndocumento,BeneficiarioPeps=benefpeps,Estado=estado)
   

    bandera= request.POST['passPT']  # guarda los datos del perefil de transacciones
    if(bandera == '1'):
        try:
            prestamos= request.POST['prestamos']  
        except :
            prestamos=""
        try:
            espotros= request.POST['otrosesp']
        except :
            espotros=""
    
        estado="curso"

        clientept=ClientePerfTra.objects.create(IdClienteDatoGen=iddgen,Prestamos=prestamos,EspecificarOtroPer=espotros,Estado=estado)
   

    bandera= request.POST['passPEP']  # guarda los datos de las personas expuestas politicamente
    if(bandera == '1'):
        ustedpeps= request.POST['ustpeps']  
        relacionpeps= request.POST['relpeps']
        try:
            nombrep= request.POST['nombrep']
        except :
            nombrep=""
        try:
            puestdesemp= request.POST['puestodes']
        except :
            puestdesemp=""
        try:
            pergestiondesde= request.POST['periodogd']
        except :
            pergestiondesde=""
        try:
            pergestionhasta= request.POST['periodogh']
        except :
            pergestionhasta=""    
        try:
            grado= request.POST['grado']
        except :
            grado=""
        try:
            pparentesco= request.POST['pparentesco']
        except :
             pparentesco=""  
        try:
            sparentesco= request.POST['sparentesco']
        except :
            sparentesco=""

        if  grado== "Primero" and pparentesco != "":
            parentesco= pparentesco
        elif grado== "Segundo" and sparentesco != "":
            parentesco= sparentesco
        else:
            parentesco=""
        
    
        estado="curso"

        clientepeps=ClientePeps.objects.create(IdClienteDatoGen=iddgen,UstedPeps=ustedpeps,RelacionPeps=relacionpeps,NombrePeps=nombrep,PuestoDese=puestdesemp,PeriodoGestDes=pergestiondesde,PeriodoGestHas=pergestionhasta,Grado=grado,Parentesco=parentesco,Estado=estado)
   
    bandera= request.POST['passCD']  # guarda de datos de comprobacion
    if(bandera == '1'):
        valedefnf= request.POST['validefnf']  
        veridireccion= request.POST['verdirec']
        verificadopor= request.POST['nombrever']
        codigoe= request.POST['codigoemp']
    
        estado="curso"

        clientepus=ClienteParaUsoExc.objects.create(IdClienteDatoGen=iddgen,ValideFirmNomFot=valedefnf,VerifiqueDire=veridireccion,VerificadoPor=verificadopor,CodigoEmpl=codigoe,Estado=estado)
   
        mensaje="Datos guardados"
        messages.success(request, mensaje)
    return redirect('administrarPerfil', id=clientedg.IdSolicitud.IdPerfil.Id)  # id de perfil 
 

def listaConozcaC(request,id):
    listc=  ClienteDatoGen.objects.filter(IdSolicitud__IdPerfil__IdAgencia=id)
    return render(request, "ConozcaClienteApp/listaCC.html", {"listc":listc})


def editarCliente(request, id):
    try:    
        cdg=  ClienteDatoGen.objects.get(Id=id)
    except ClienteDatoGen.DoesNotExist:
        cdg="" 
    
    #########################################
    try:
        s=  Solicitud.objects.get(Id=cdg.IdSolicitud.Id)
    except Solicitud.DoesNotExist:
        s=""
    idSol=cdg.IdSolicitud.Id
    try:
         d=  Domicilio.objects.get(IdSolicitud=idSol, Tipo="Solicitante")
    except Domicilio.DoesNotExist:
        d=""

    try:
        dpc=DatosPersFia.objects.get(IdSolicitud=idSol,Tipo = "codeudor")
    except Exception:
        dpc=""

    try:
        dp=DatosPers.objects.get(IdSolicitud=idSol)
    except DatosPers.DoesNotExist:
        dp=""
   ##########################################

    try:
        cdaec=  ClienteActiEco.objects.get(IdClienteDatoGen=id)
    except ClienteActiEco.DoesNotExist:
        cdaec=""
    try: 
        cddn= ClienteDatoNeg.objects.get(IdClienteDatoGen=id)
    except ClienteDatoNeg.DoesNotExist:
        cddn="" 

    try:
        cdc=  ClienteDeclCli.objects.get(IdClienteDatoGen=id)
    except ClienteDeclCli.DoesNotExist:
        cdc=""
    
    try:
        cdpbo=  ClientePersBen.objects.get(IdClienteDatoGen=id)
    except ClientePersBen.DoesNotExist:
        cdpbo=""

    try:
        cpt=  ClientePerfTra.objects.get(IdClienteDatoGen=id)
    except ClientePerfTra.DoesNotExist:
        cpt=""
    try:
        cpeps=  ClientePeps.objects.get(IdClienteDatoGen=id)
    except ClientePeps.DoesNotExist:
        cpeps=""
    try:
        cpus=  ClienteParaUsoExc.objects.get(IdClienteDatoGen=id)
    except ClienteParaUsoExc.DoesNotExist:
        cpus=""
    try:
            listao=Ocupacion.objects.filter(Estado="activo")
    except Ocupacion.DoesNotExist:
            listao=""

    return render(request, "ConozcaClienteApp/editarCliente.html", {"ocupaciones":listao,"cdg":cdg,"cdaec":cdaec,"cddn":cddn, "cdc":cdc , "cdpbo":cdpbo,"cpt":cpt, "cpeps":cpeps, "cpus":cpus, "s":s, "d":d, "dpc":dpc, "dp":dp   })


def editarD(request): 
  
    iddgm=request.POST['iddgm']
    codigo=request.POST['codigo']
    try:
        calidadactua=request.POST['calidad']
    except :
        calidadactua="Cliente"
    try:
        conocidocomo=request.POST['conocidoc']
    except :
        conocidocomo=""
    profesiondui =request.POST['profesionsd']
    idocu=Ocupacion.objects.get(Id=profesiondui) 
    
    nacionalidad=request.POST['nacionalidad']
    docidentidad=request.POST['documento']
    numerodoc=request.POST['ndoc']
    fechavdoc=request.POST['fechavd']
    direcciondomic=request.POST['direcciond']
    correoe=request.POST['correo']
    telcelular=request.POST['telefonoc']
    telfijo=request.POST['telefonof']
    estatusp=request.POST['estatusp']
    try:
        nombrecony=request.POST['nombrecony']
    except :
        nombrecony=""
    
    cdg=ClienteDatoGen.objects.get(Id=iddgm)
    cdg.Codigo=codigo
    cdg.CalidadActu=calidadactua
    cdg.ConocidoComo=conocidocomo
    cdg.Nacionalidad=nacionalidad
    cdg.DocumentoIden=docidentidad    
    cdg.NumeroDocu=numerodoc
    cdg.FechaVencdoc=fechavdoc
    cdg.DireccionDomi=direcciondomic
    cdg.CorreoElec=correoe
    cdg.TelefonoCelu=telcelular
    cdg.TelefonoFijo=telfijo
    cdg.EstatusProp=estatusp
    cdg.NombreCony=nombrecony
    cdg.save()
    idsol= Solicitud.objects.get(Id=cdg.IdSolicitud.Id)
    if(calidadactua =="Cliente"):
        perfil = Perfil.objects.get(Id=idsol.IdPerfil.Id)
        perfil.IdOcupacionDUI=idocu
        perfil.save()
    else:
        fiador = DatosPersFia.objects.get(IsSolicitud =idsol.IdPerfil.Id)
        fiador.IdOcupacionDUIFia=idocu
        fiador.save()
    
    

    bandera= request.POST['passAED']  # guarda los datos de la empr
    if(bandera == '1'):
        tipoact= request.POST['tipoa']
        lugartrab= request.POST['lugart']
        cargodes= request.POST['cargode']         
        tiempolaborar= request.POST['tiempolab']
        procedenciafod= request.POST['procedenciafonda']
        rangoingresosemp= request.POST['rangoing']
        otrosingresos= request.POST['otingresos']
        try:
            procedenciaoi= request.POST['procedencia']
        except :
            procedenciaoi=""   
               
        caec=ClienteActiEco.objects.get(IdClienteDatoGen=iddgm)
        caec.TipoActi=tipoact
        caec.LugarTrab=lugartrab
        caec.CargoDese=cargodes
        caec.TiempoLabo=tiempolaborar
        caec.ProcedenciaFond= procedenciafod
        caec.RangoIngrMen=rangoingresosemp
        caec.OtrosIngr=otrosingresos
        caec.ProcedenciaOtroIng=procedenciaoi
        caec.save()

    bandera= request.POST['passDN']  # guarda los datos de la empresa
    if(bandera == '1'):
        try:
            nombreneg= request.POST['nombreng'] 
        except :
            nombreneg==""
        try: 
            prodserv= request.POST['descps']
        except :
            prodserv=""
        try:
            direccionneg= request.POST['direccionneg']
        except :
            direccionneg=""
        try:
            fechaia= request.POST['fechaia']
        except :
            fechaia=""
        
        if(fechaia=="" ):
            fechaia = None 

        try:
            rangoingresos= request.POST['rangoimn']
        except :
            rangoingresos=""
        try:
            otrosingresos= request.POST['otrosidn']
        except :
            otrosingresos=""
        try:
            procedenciaoi= request.POST['procedenciadn']
        except :
            procedenciaoi=""   
       
        cdn=ClienteDatoNeg.objects.get(IdClienteDatoGen=iddgm)
        cdn.NombreNego=nombreneg
        cdn.ProductoServ=prodserv
        cdn.DireccionNego=direccionneg
        cdn.FechaInicAct=fechaia
        cdn.RangoIngrMen=rangoingresos
        cdn.OtrosIngrMen=otrosingresos
        cdn.ProcedenciaOtroIng=procedenciaoi
        cdn.save()

    bandera= request.POST['passDCF']  # guarda los datos del cliente o fiador
    if(bandera == '1'):
        try:
            clasifcredito= request.POST['clasificacionc'] 
        except:
            clasifcredito="" 
        try:
            montodc= request.POST['montodc']
        except:
            montodc=""
        try:        
            cuotadc= request.POST['cuotadc']
        except:
            cuotadc=""
            
        rpagosadic= request.POST['rpagosadic'] 

        try:
            procpagosadic= request.POST['procfondos']
        except:
            procpagosadic=""
    

        cdc=ClienteDeclCli.objects.get(IdClienteDatoGen=iddgm)
        cdc.ClasificacionCred=clasifcredito
        cdc.MontoDeclCli=montodc
        cdc.CuotaDeclCli=cuotadc
        cdc.RealizarPagoAdi=rpagosadic
        cdc.ProcedenciaPagoAdi=procpagosadic
        cdc.save()

    bandera= request.POST['passBPEP']  # persona benefiaria de la operacion
    if(bandera == '1'):
        try:
            noaplica= request.POST['noaplica'] 
        except:
            noaplica="" 
        try:
            nombrecomp= request.POST['nombrecb']
        except:
            nombrecomp=""
        try:
            direccionp= request.POST['direcpermanente']
        except:
            direccionp=""
        try:
            tdocumento= request.POST['tdocumento']
        except:
            tdocumento=""
        try:
            ndocumento= request.POST['ndocumento']
        except:
            ndocumento=""
        try:
            benefpeps= request.POST['beneficiariopeps']
        except:
            benefpeps=""
        

        cpbo=ClientePersBen.objects.get(IdClienteDatoGen=iddgm)
        cpbo.NoApli=noaplica
        cpbo.NombreComp=nombrecomp
        cpbo.DireccionPerm=direccionp
        cpbo.TipoDocuPers=tdocumento
        cpbo.NumeroDocuPers=ndocumento
        cpbo.BeneficiarioPeps=benefpeps
        cpbo.save()


    bandera= request.POST['passPT']  # guarda los datos del perfil de transacciones
    if(bandera == '1'):
        prestamos= request.POST['prestamos']  
        espotros= request.POST['otrosesp']

        cpt=ClientePerfTra.objects.get(IdClienteDatoGen=iddgm)
        cpt.Prestamos=prestamos
        cpt.EspecificarOtroPer=espotros
        cpt.save()
   

    bandera= request.POST['passPEP']  # guarda los datos de las personas expuestas politicamente
    if(bandera == '1'):
        try:
            ustedpeps= request.POST['ustpeps']  
        except :
            ustedpeps=""
        try:
            relacionpeps= request.POST['relpeps']
        except :
            relacionpeps=""
        try:
            nombrep= request.POST['nombrep']
        except :
            nombrep=""
        try:
            puestdesemp= request.POST['puestodes']
        except :
            puestdesemp=""
        try:
            pergestiondesde= request.POST['periodogd']
        except :
            pergestiondesde=""
        try:
            pergestionhasta= request.POST['periodogh']
        except :
            pergestionhasta=""
        try:
            grado= request.POST['grado']
        except :
            grado=""

        try:
            pparentesco= request.POST['pparentesco']
        except :
            pparentesco=""

        try:
            sparentesco= request.POST['sparentesco']
        except :
            sparentesco=""

        if grado=="Primero" and pparentesco != "":
            parentesco= pparentesco
        elif grado=="Segundo" and  sparentesco != "":
            parentesco= sparentesco
        else:
            parentesco=""
  
        cpeps=ClientePeps.objects.get(IdClienteDatoGen=iddgm)
        cpeps.UstedPeps=ustedpeps
        cpeps.RelacionPeps=relacionpeps
        cpeps.NombrePeps=nombrep
        cpeps.PuestoDese=puestdesemp        
        cpeps.PeriodoGestDes=pergestiondesde
        cpeps.PeriodoGestHas=pergestionhasta
        cpeps.Grado=grado
        cpeps.Parentesco=parentesco
        cpeps.save()
   
    bandera= request.POST['passCD']  # guarda de datos de comprobacion
    if(bandera == '1'):
        valedefnf= request.POST['validefnf']  
        veridireccion= request.POST['verdirec']
        verificadopor= request.POST['nombrever']
        codigoe= request.POST['codigoemp']
    

        cpus=ClienteParaUsoExc.objects.get(IdClienteDatoGen=iddgm)
        cpus.ValideFirmNomFot=valedefnf
        cpus.VerifiqueDire=veridireccion
        cpus.VerificadoPor=verificadopor
        cpus.CodigoEmpl=codigoe
        cpus.save()

    mensaje="Datos actualizados"     
    registroBit(request, "Actualización de datos de formulario conozca a su cliente " + cdg.Codigo,"Actualización")    
    messages.success(request, mensaje) 
    return redirect('administrarPerfil', id=cdg.IdSolicitud.IdPerfil.Id)  # id de perfil 
    
