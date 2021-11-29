from django.http.response import HttpResponse
from django.shortcuts import render
from appFuncionario.models import *
# Create your views here.

def login(request):
    return render(request,"login.html")

def badlogin(request):
    return render(request,"badlogin.html")

def home(request):
    if request.POST["username"] and  request.POST["pwd"]:
        try:
            respuesta = Funcionario.objects.get(usuario=request.POST["username"],contrasena=request.POST["pwd"])
            func = Funcionario(respuesta.rut,respuesta.usuario,respuesta.contrasena)
            return render(request,'home.html',{"Funcionario":func})
        except:
            return render(request,"badlogin.html")
    else:
        return render(request,"badlogin.html")

def registro(request):
    if request.method == "POST":
        respuesta = Funcionario.objects.get(rut=request.POST["func"])
        func = Funcionario(respuesta.rut,respuesta.usuario,respuesta.contrasena)
        serv = func.crearServicio("crearUsuario")
        return render(request,"registro.html",{"Funcionario":func,"Servicio":serv})

def confirmarRegistro(request):
    if(request.method == "GET"):
        idServ = Servicio.objects.get(num_servicio=request.GET["serv"])
        serv = Servicio(idServ.num_servicio,idServ.fecha_reserva_servicio,idServ.fecha_inicio_servicio,idServ.fecha_termino_servicio,idServ.Cliente,idServ.Funcionario)
        cliente = serv.solicitarDatos([request.GET["rut"],request.GET["nombre"],request.GET["correo"],request.GET["telefono"]])
        serv.save()
        return render(request,"confirmarRegistro.html",{"Servicio":serv,"Cliente":cliente})
    else:
        idFunc = Funcionario.objects.get(rut=request.GET["func"])
        func = Funcionario(idFunc.rut,idFunc.usuario,idFunc.contrasena)
        idServ = Servicio.objects.get(num_servicio=request.GET["serv"])
        serv = Servicio(idServ.num_servicio,idServ.fecha_reserva_servicio,idServ.fecha_inicio_servicio,idServ.fecha_termino_servicio,idServ.Cliente,idServ.Funcionario)
        idClient = Cliente.objects.get(rut=request.GET["rut"])
        client = Cliente(idClient.rut,idClient.correo,idClient.nombre,idClient.deuda,idClient.telefono)
        confirmacion = func.confirmarServicio("registro",serv)
        if(confirmacion):
            numero = client.generarTarjeta()
            return render(request,"confirmado.html",{"Funcionario":func,"Cliente":client,"Servicio":serv,"Numero":numero})

def confirmado(request):
    if (request.method=="GET"):
        idFunc = Funcionario.objects.get(rut=request.GET["func"])
        func = Funcionario(idFunc.rut,idFunc.usuario,idFunc.contrasena)
        idServ = Servicio.objects.get(num_servicio=request.GET["serv"])
        serv = Servicio(idServ.num_servicio,idServ.fecha_reserva_servicio,idServ.fecha_inicio_servicio,idServ.fecha_termino_servicio,idServ.Cliente,idServ.Funcionario)
        serv.setTerminoServicio()
        return render(request,"home.html",{"Funcionario":func})