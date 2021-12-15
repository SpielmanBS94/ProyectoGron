from django.core.exceptions import DisallowedHost, ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render
from appFuncionario.forms import *
from appFuncionario.models import *
from datetime import datetime
import locale
# Create your views here.

def obtenerFecha():
    locale.setlocale(locale.LC_ALL, 'es-ES')
    return datetime.now().strftime("%A , %d-%m-%Y").capitalize()

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
            return render(request,"almacenar/principal.html",{"Funcionario":func,"Servicio":serv,"Cliente":client,"Fecha":fecha})
        except ObjectDoesNotExist:
            fecha =obtenerFecha()
            return render(request,"home.html",{"Funcionario":func,"Momento":"badRut","Fecha":fecha})

def guardar(request):
    if(request.method == "GET"):
        func = Funcionario.objects.get(rut=request.GET["func"])
        opcion = request.GET["radio"]
        form = None
        if(opcion == "Bicicleta"):
            form = BicicletaForm().as_table
        elif(opcion == "EPP"):
            form = EPPForm().as_table
        elif(opcion == "Estacionamiento"):
            form = EstacionamientoForm().as_table
        else:
            form = HerramientaForm().as_table
        return render(request,"agregarElemento/guardarElemento.html",{"Funcionario":func,"formElemento":form, "Opcion":opcion})
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
                return render(request,"agregarElemento/guardarElemento.html",{"Funcionario":func,"Opcion":opcion,"Elemento":ele,"Momento":"Enviado"})