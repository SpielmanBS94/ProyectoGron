from django.core.exceptions import DisallowedHost, ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render
from appFuncionario.forms import *
from appFuncionario.models import *
from datetime import datetime
from django.db.models import Q
import locale
# Create your views here.

def obtenerFecha():
    locale.setlocale(locale.LC_ALL, 'es-ES')
    return datetime.now().strftime("%A , %d-%m-%Y").capitalize()

def obtenerElementos(criterio):
    listaElementos = list()
    queryset=Bicicleta.objects.filter(Q(id__contains=criterio) | Q(nombre__contains=criterio) | Q(marca__contains=criterio)| Q(color__contains=criterio)| Q(observaciones__contains=criterio)| Q(accesorios__contains=criterio)| Q(estado__contains=criterio)| Q(activoFijo=False))
    for elemento in queryset:
        listaElementos.append(elemento)
    queryset2=Estacionamiento.objects.filter(Q(id__contains=criterio) | Q(nombre__contains=criterio) | Q(marca__contains=criterio)| Q(numero_estacionamiento__contains=criterio)| Q(area__contains=criterio)).filter(Q(disponibilidad=True))
    for elemento in queryset2:
        listaElementos.append(elemento)
    queryset3=Herramienta.objects.filter(Q(id__contains=criterio) | Q(nombre__contains=criterio) | Q(marca__contains=criterio)| Q(instrucciones__contains=criterio)| Q(estado__contains=criterio))
    for elemento in queryset3:
        listaElementos.append(elemento)
    queryset4=EPP.objects.filter(Q(id__contains=criterio) | Q(nombre__contains=criterio) | Q(marca__contains=criterio)| Q(color__contains=criterio)| Q(talla__contains=criterio))
    for elemento in queryset4:
        listaElementos.append(elemento)
    return listaElementos

def login(request):
    return render(request,"login.html")

def badlogin(request):
    return render(request,"badlogin.html")

def home(request):
    if(request.method == "POST"):
        try:
            request.POST["username"] and  request.POST["pwd"]
            fecha =obtenerFecha()
            func=Funcionario.objects.get(usuario=request.POST["username"],contrasena=request.POST["pwd"])
            return render(request,'home.html',{"Funcionario":func, "Fecha":fecha})
        except :
            return render(request,"badlogin.html")
    else:
        if(request.GET["accion"]=="tarjetaImpresa"):
            fecha =obtenerFecha()
            func=Funcionario.objects.get(rut=request.GET["func"])
            serv = Servicio.objects.get(num_servicio=request.GET["serv"])
            func.servicioListo(serv)
            return render(request,'home.html',{"Funcionario":func, "Fecha":fecha})
        if(request.GET["accion"]=="delServ"):
            fecha =obtenerFecha()
            func = Funcionario.objects.get(rut=request.GET["func"])
            serv = Servicio.objects.get(num_servicio=request.GET["serv"])
            serv.delete()
            return render(request,'home.html',{"Funcionario":func,"Fecha":fecha})
        elif(request.GET["accion"]=="delServplusClient"):
            fecha =obtenerFecha()
            func = Funcionario.objects.get(rut=request.GET["func"])
            serv = Servicio.objects.get(num_servicio=request.GET["serv"])
            client = Cliente.objects.get(rut=request.GET["rutCliente"])
            serv.delete()
            client.delete()
            return render(request,'home.html',{"Funcionario":func,"Fecha":fecha})
        elif(request.GET["accion"]=="cancelElemento"):
            fecha =obtenerFecha()
            func = Funcionario.objects.get(rut=request.GET["func"])
            return render(request,'home.html',{"Funcionario":func,"Fecha":fecha})

def registro(request):
    func = Funcionario.objects.get(rut=request.POST["func"])
    if(request.POST["Momento"] == "inicio"):
        serv = func.crearServicio("registro",None)
        form = ClienteForm().as_table
        return render(request,"crearUsuario/registro.html",{"Funcionario":func,"Servicio":serv,"FormCliente":form,"Momento":request.POST["Momento"]})
    elif(request.POST["Momento"] == "enviado"):
        serv = Servicio.objects.get(num_servicio=request.POST["serv"])
        clienteForm = ClienteForm(request.POST,request.FILES)
        if clienteForm.is_valid():
            cliente = serv.solicitarDatos(clienteForm)
            serv.save()
            return render(request,"crearUsuario/registro.html",{"Funcionario":func,"Servicio":serv,"Cliente":cliente,"FormCliente":clienteForm,"Momento":request.POST["Momento"]})
    else:
        serv = Servicio.objects.get(num_servicio=request.POST["serv"])
        client = Cliente.objects.get(rut=request.POST["rutCliente"])
        confirmacion = func.confirmarServicio("registro",serv)
        if(confirmacion):
            numero = client.generarTarjeta()
            return render(request,"crearUsuario/registro.html",{"Funcionario":func,"Cliente":client,"Servicio":serv,"Numero":numero,"Momento":request.POST["Momento"]})

def almacenar(request):
    if(request.method == "GET"):
        try:
            func = Funcionario.objects.get(rut=request.GET["func"])
            client = Cliente.objects.get(rut=request.GET["rutCliente"])
            serv = func.crearServicio("almacenamiento",client)
            fecha =obtenerFecha()
            listaElementosAgregados = list()
            return render(request,"almacenar/principal.html",{"Funcionario":func,"Servicio":serv,"Cliente":client,"Fecha":fecha, "ListaAgregados":listaElementosAgregados, "Momento":"Inicio"})
        except ObjectDoesNotExist:
            fecha =obtenerFecha()
            return render(request,"home.html",{"Funcionario":func,"Momento":"badRut","Fecha":fecha})
    else:
        func = Funcionario.objects.get(rut=request.POST["func"])
        client = Cliente.objects.get(rut=request.POST["rutCliente"])
        serv = Servicio.objects.get(num_servicio=request.POST["serv"])
        fecha =obtenerFecha()
        lista = request.POST["ListaAgregados"].replace("[","").replace("]","").split(",")
        listaElementosAgregados = list()
        for elemento in lista:
            tipo = elemento[elemento.find("<")+1:elemento.find(":")]
            idEle = elemento[elemento.find("(")+1:elemento.find(")")]
            ele = None
            if(tipo == "Bicicleta"):
                ele = Bicicleta.objects.get(id=idEle)
            elif(tipo == "EPP"):
                ele = EPP.objects.get(id=idEle)
            elif(tipo == "Estacionamiento"):
                 ele = Estacionamiento.objects.get(id=idEle)
            elif(tipo == "Herramienta"):
                ele = Herramienta.objects.get(id=idEle)
            if(ele != None):
                listaElementosAgregados.append(ele)
        if(request.POST["accion"] == "Buscar"):
            listaElementosBuscados = obtenerElementos(request.POST["criterio"])
            return render(request,"almacenar/principal.html",{"Funcionario":func,"Servicio":serv,"Cliente":client,"Fecha":fecha, "ListaAgregados":listaElementosAgregados , "ListaBuscados":listaElementosBuscados, "Momento":"Busqueda"})
        elif(request.POST["accion"] == "Agregar"):
            listaSelect = request.POST["seleccion"].split(",")
            for elemento in listaSelect:
                tipo = elemento[:elemento.find(":")]
                idEle = elemento[elemento.find(":")+1:]
                ele = None
                if(tipo == "Bicicleta"):
                    ele = Bicicleta.objects.get(id=idEle)
                elif(tipo == "EPP"):
                    ele = EPP.objects.get(id=idEle)
                elif(tipo == "Estacionamiento"):
                    ele = Estacionamiento.objects.get(id=idEle)
                elif(tipo == "Herramienta"):
                    ele = Herramienta.objects.get(id=idEle)
                if(ele != None):
                    listaElementosAgregados.append(ele)
            return render(request,"almacenar/principal.html",{"Funcionario":func,"Servicio":serv,"Cliente":client,"Fecha":fecha, "ListaAgregados":listaElementosAgregados ,"Momento":"Agregados"})

def guardar(request):
    fecha = obtenerFecha()
    if(request.method == "GET"):
        func = Funcionario.objects.get(rut=request.GET["func"])
        opcion = request.GET["radio"]
        if(request.GET["Momento"] == "Cancelado"):
            ele = None
            if(opcion == "Bicicleta"):
                ele = Bicicleta.objects.get(id=request.GET["Elemento"])
            elif(opcion == "EPP"):
                ele = EPP.objects.get(id=request.GET["Elemento"])
            elif(opcion == "Estacionamiento"):
                ele = Estacionamiento.objects.get(id=request.GET["Elemento"])
            else:
                ele = Herramienta.objects.get(id=request.GET["Elemento"])
            ele.delete()
        form = None
        if(opcion == "Bicicleta"):
            form = BicicletaForm().as_table
        elif(opcion == "EPP"):
            form = EPPForm().as_table
        elif(opcion == "Estacionamiento"):
            form = EstacionamientoForm().as_table
        else:
            form = HerramientaForm().as_table
        return render(request,"agregarElemento/guardarElemento.html",{"Funcionario":func,"formElemento":form, "Opcion":opcion, "Fecha":fecha})
    else:
        if(request.POST["Momento"] == "Enviado"):
            func = Funcionario.objects.get(rut=request.POST["func"])
            opcion = request.POST["opcion"]
            eleForm = None
            if(opcion == "Bicicleta"):
                eleForm = BicicletaForm(request.POST)
            elif(opcion == "EPP"):
                eleForm = EPPForm(request.POST)
            elif(opcion == "Estacionamiento"):
                eleForm = EstacionamientoForm(request.POST)
            else:
                eleForm = HerramientaForm(request.POST)
            if eleForm.is_valid():
                ele = func.agregarElemento(eleForm,opcion,func)
                return render(request,"agregarElemento/guardarElemento.html",{"Funcionario":func,"Opcion":opcion,"Elemento":ele,"Momento":"Enviado", "Fecha":fecha})
        elif(request.POST["Momento"] == "Registrado"):
            func = Funcionario.objects.get(rut=request.POST["func"])
            ele = None
            opcion = request.POST["opcion"]
            form = None
            if(opcion == "Bicicleta"):
                ele = Bicicleta.objects.get(id=request.POST["Elemento"])
                form = BicicletaForm().as_table
            elif(opcion == "EPP"):
                ele = EPP.objects.get(id=request.POST["Elemento"])
                form = EPPForm().as_table
            elif(opcion == "Estacionamiento"):
                ele = Estacionamiento.objects.get(id=request.POST["Elemento"])
                form = EstacionamientoForm().as_table
            else:
                ele = Herramienta.objects.get(id=request.POST["Elemento"])
                form = HerramientaForm().as_table
            ele.confirmarRegistro()
            return render(request,"agregarElemento/guardarElemento.html",{"Funcionario":func,"formElemento":form, "Opcion":opcion, "Fecha":fecha, "Momento":"Registrado"})