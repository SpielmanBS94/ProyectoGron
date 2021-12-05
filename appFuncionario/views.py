from django.core.exceptions import DisallowedHost, ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render
from appFuncionario.models import *
from datetime import datetime
import locale
# Create your views here.

def login(request):
    return render(request,"login.html")

def badlogin(request):
    return render(request,"badlogin.html")

def home(request):
    if(request.method == "POST"):
        if request.POST["username"] and  request.POST["pwd"]:
            fecha =obtenerFecha()
            func=Funcionario.objects.get(usuario=request.POST["username"],contrasena=request.POST["pwd"])
            return render(request,'home.html',{"Funcionario":func, "Fecha":fecha})
        else :
            return render(request,"badlogin.html")
    else:
        if(request.GET["accion"]=="delServ"):
            fecha =obtenerFecha()
            func = Funcionario.objects.get(rut=request.GET["func"])
            serv = Servicio.objects.get(num_servicio=request.GET["serv"])
            serv.delete()
            return render(request,'home.html',{"Funcionario":func,"Fecha":fecha})

def registro(request):
    if(request.method == "POST"):
        func = Funcionario.objects.get(rut=request.POST["func"])
        serv = func.crearServicio("crearUsuario")
        return render(request,"crearUsuario/registro.html",{"Funcionario":func,"Servicio":serv})

def almacenar(request):
    if(request.method == "GET"):
        func = Funcionario.objects.get(rut=request.GET["func"])
        client = Cliente.objects.get(rut=request.GET["rutCliente"])
        return render(request,"almacenar/principal.html",{"Funcionario":func,"Cliente":client})

def confirmarRegistro(request):
    if(request.method == "GET"):
        serv = Servicio.objects.get(num_servicio=request.GET["serv"])
        cliente = serv.solicitarDatos([request.GET["rut"],request.GET["nombre"],request.GET["correo"],request.GET["telefono"]])
        serv.save()
        return render(request,"crearUsuario/confirmarRegistro.html",{"Servicio":serv,"Cliente":cliente})
    else:
        func = Funcionario.objects.get(rut=request.GET["func"])
        serv = Servicio.objects.get(num_servicio=request.GET["serv"])
        client = Cliente.objects.get(rut=request.GET["rut"])
        confirmacion = func.confirmarServicio("registro",serv)
        if(confirmacion):
            numero = client.generarTarjeta()
            return render(request,"crearUsuario/confirmado.html",{"Funcionario":func,"Cliente":client,"Servicio":serv,"Numero":numero})

def confirmado(request):
    if (request.method=="GET"):
        func = Funcionario.objects.get(rut=request.GET["func"])
        serv = Servicio.objects.get(num_servicio=request.GET["serv"])
        serv.setTerminoServicio()
        return render(request,"home.html",{"Funcionario":func})

def obtenerFecha():
    locale.setlocale(locale.LC_ALL, 'es-ES')
    return datetime.now().strftime("%A , %d-%m-%Y").capitalize()