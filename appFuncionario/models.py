from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE,SET_NULL
# Create your models here.

class Cliente(models.Model): 

    rut = models.CharField(max_length = 10 ,primary_key = True)
    correo = models.EmailField()
    nombre = models.CharField(max_length = 50)
    deuda = models.BigIntegerField(default = 0)
    telefono = models.CharField(max_length = 9)

    def __str__(self):
        return "Cliente: %s nombre: %s " %(self.rut,self.nombre)

    def getRut(self):
        return self.rut

    def getRutFormato(self):
        if(len(self.rut)>8):
            return "%s.%s.%s-%s" %(self.rut[0:2],self.rut[2:5],self.rut[5:8],self.rut[8])
        else:
            return "%s.%s.%s-%s" %(self.rut[0:1],self.rut[1:4],self.rut[4:7],self.rut[7])

    def getCorreo(self):
        return self.correo

    def getNombre(self):
        return self.nombre

    def getDeuda(self):
        return self.deuda
        
    def getTelefono(self):
        if(str(self.telefono) != ""):
            return str(self.telefono)
        return "Sin Telefono"

    def getInfoTarj(self):
        return self.nombre.split(" ")
        
    def generarTarjeta(self):
        trj=Tarjeta.objects.create(Dueno=self,habilitada=True)
        return trj.getNum()

class Funcionario(models.Model):

    rut = models.CharField(max_length = 10, primary_key = True)
    usuario = models.CharField(max_length = 20)
    contrasena = models.CharField(max_length = 20)
    imagen=models.ImageField(null=True,upload_to = 'funcionarios/', default = 'funcionarios/userDefault.png')

    def getRut(self):
        return self.rut

    def getUser(self):
        return self.usuario

    def crearServicio(self,tipo):
        if(tipo == "crearUsuario"):
            servicio=Servicio.objects.create(Funcionario=self,Cliente=None)
            return servicio

    def confirmarServicio(self,tipo,servicio):
        if(tipo=="registro"):
            servicio.fecha_reserva_servicio=datetime.now()
            servicio.fecha_inicio_servicio=datetime.now()
            servicio.save()
        return True
    def __str__(self):
        return "Funcionario: %s Nombre: %s " %(self.rut,self.usuario)
    def getImg(self):
        return self.imagen.url

class Tarjeta(models.Model):

    numero_tarjeta = models.BigAutoField(primary_key = True)
    habilitada = models.BooleanField()
    rut_propietario = models.ForeignKey(Cliente, name = "Dueno",on_delete = CASCADE,default="")

    def getNum(self):
        return self.numero_tarjeta

class Servicio(models.Model):

    num_servicio = models.BigAutoField(primary_key = True)
    fecha_reserva_servicio = models.DateTimeField(null=True)
    fecha_inicio_servicio = models.DateTimeField(null=True)
    fecha_termino_servicio = models.DateTimeField(null=True)
    rut_cliente = models.ForeignKey(Cliente, name = "Cliente",on_delete = SET_NULL, default="",null=True)
    rut_funcionario = models.ForeignKey(Funcionario, name = "Funcionario",on_delete = SET_NULL,default="",null=True)

    
    def getNum(self):
        return self.num_servicio

    def solicitarDatos(self,datosCliente):
        return self.crearCliente(datosCliente[0],datosCliente[1],datosCliente[2],datosCliente[3])

    def crearCliente(self,rut,nombre,correo,telefono):

        self.Cliente = Cliente.objects.create(rut=rut,nombre=nombre,correo=correo,telefono=telefono)
        return self.Cliente

    def getFunc(self):
        return self.Funcionario

    def getClient(self):
        return self.Cliente
    def setTerminoServicio(self):
        self.fecha_termino_servicio=datetime.now()
        self.save()
        