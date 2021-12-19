from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE,SET_NULL
# Create your models here.

class Cliente(models.Model): 

    rut = models.CharField(max_length = 10 ,primary_key = True)
    correo = models.EmailField()
    nombre = models.CharField(max_length = 50)
    deuda = models.BigIntegerField(default = 0)
    telefono = models.CharField(max_length = 9, null=True, blank=True)
    fotoPerfil = models.ImageField(null=True,upload_to = 'clientes/', default = 'funcionarios/userDefault.png')

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
        if(str(self.telefono) != "None"):
            return str(self.telefono)
        return "Sin Telefono"

    def getInfoTarj(self):
        return self.nombre.split(" ")
    
    def getNombres(self):
        lista = self.nombre.split(" ")
        pos = round(len(lista)/2)
        return lista[:pos]
    def getApellidos(self):
        lista = self.nombre.split(" ")
        pos = round(len(lista)/2)
        return lista[pos:]

    def generarTarjeta(self):
        trj=Tarjeta.objects.create(Dueno=self,habilitada=True)
        return trj.getNum()

    def getTarjeta(self):
        tarj = Tarjeta.objects.get(Dueno=self,habilitada=True)
        return tarj.getNum()

    def getImg(self):
        return self.fotoPerfil.url

class Funcionario(models.Model):

    rut = models.CharField(max_length = 10, primary_key = True)
    usuario = models.CharField(max_length = 20)
    contrasena = models.CharField(max_length = 20)
    imagen=models.ImageField(null=True,upload_to = 'funcionarios/', default = 'funcionarios/userDefault.png')

    def getRut(self):
        return self.rut

    def getUser(self):
        return self.usuario

    def crearServicio(self,tipo,cliente):
        if(tipo == "registro"):
            servicio=Servicio.objects.create(Funcionario=self,tipo=tipo,Cliente=None)
            return servicio
        elif(tipo == "almacenamiento"):
            servicio=Servicio.objects.create(Funcionario=self,tipo=tipo,Cliente=cliente)
            return servicio
    def confirmarServicio(self,tipo,servicioConfirm):
        if(tipo=="registro"):
            servicioConfirm.fecha_reserva_servicio=datetime.now()
            servicioConfirm.fecha_inicio_servicio=datetime.now()
            servicioConfirm.save()
        elif(tipo== "almacenamiento"):
            servicioConfirm.fecha_reserva_servicio=datetime.now()
            servicioConfirm.fecha_inicio_servicio=datetime.now()
            servicioConfirm.save()
        listaElementos = list()
        queryset=Detalle.objects.filter(servicio=servicioConfirm)
        for detalle in queryset:
            detalle.fecha_hora_entrega=datetime.now()
            detalle.fecha_hora_entrega_real=datetime.now()
            detalle.save()
        return True
    def servicioListo(self,servicio):
        servicio.fecha_termino_servicio=datetime.now()
        servicio.save()

    def __str__(self):
        return "Funcionario: %s Nombre: %s " %(self.rut,self.usuario)
    def getImg(self):
        return self.imagen.url
    def getPass(self):
        return self.contrasena

    def agregarElemento(self,elemForm,tipo,func):
        nombre = elemForm.cleaned_data.get("nombre")
        marca = elemForm.cleaned_data.get("marca")
        if(tipo=="Bicicleta"):
            color = elemForm.cleaned_data.get("color")
            observaciones = elemForm.cleaned_data.get("observaciones")
            accesorios = elemForm.cleaned_data.get("accesorios")
            activoFijo = elemForm.cleaned_data.get("activoFijo")
            estado = elemForm.cleaned_data.get("estado")
            ele = Bicicleta.objects.create(nombre=nombre,marca=marca,Funcionario=func,color=color,observaciones=observaciones,accesorios=accesorios,activoFijo=activoFijo,estado=estado)
            return ele
        elif(tipo=="EPP"):
            talla = elemForm.cleaned_data.get("talla")
            desechable = elemForm.cleaned_data.get("desechable")
            color = elemForm.cleaned_data.get("color")
            ele = EPP.objects.create(nombre=nombre,marca=marca,Funcionario=func,talla=talla,desechable=desechable,color=color)
            return ele
        elif(tipo=="Estacionamiento"):
            numero_estacionamiento = elemForm.cleaned_data.get("numero_estacionamiento")
            area = elemForm.cleaned_data.get("area")
            disponibilidad = elemForm.cleaned_data.get("disponibilidad")
            ele = Estacionamiento.objects.create(nombre=nombre,marca=marca,Funcionario=func,numero_estacionamiento=numero_estacionamiento,area=area,disponibilidad=disponibilidad)
            return ele
        else:
            instrucciones = elemForm.cleaned_data.get("instrucciones")
            desechable = elemForm.cleaned_data.get("desechable")
            requiere_epp = elemForm.cleaned_data.get("requiere_epp")
            lista_epp = elemForm.cleaned_data.get("lista_epp")
            estado = elemForm.cleaned_data.get("estado")
            ele = Herramienta.objects.create(nombre=nombre,marca=marca,Funcionario=func,instrucciones=instrucciones,desechable=desechable,requiere_epp=requiere_epp,lista_epp=lista_epp,estado=estado)
            return ele
class Tarjeta(models.Model):

    numero_tarjeta = models.BigAutoField(primary_key = True)
    habilitada = models.BooleanField()
    rut_propietario = models.ForeignKey(Cliente, name = "Dueno",on_delete = CASCADE,default="")

    def getNum(self):
        return self.numero_tarjeta


class Servicio(models.Model):

    num_servicio = models.BigAutoField(primary_key = True)
    tipo = models.CharField(max_length = 15, null=True)
    fecha_reserva_servicio = models.DateTimeField(null=True)
    fecha_inicio_servicio = models.DateTimeField(null=True)
    fecha_termino_servicio = models.DateTimeField(null=True)
    rut_cliente = models.ForeignKey(Cliente, name = "Cliente",on_delete = SET_NULL, default="",null=True)
    rut_funcionario = models.ForeignKey(Funcionario, name = "Funcionario",on_delete = SET_NULL,default="",null=True)

    
    def getNum(self):
        return self.num_servicio

    def getTipo(self):
        return self.num_servicio

    def solicitarDatos(self,datosCliente):
        rut = datosCliente.cleaned_data.get("rut")
        correo = datosCliente.cleaned_data.get("correo")
        nombre = datosCliente.cleaned_data.get("nombre")
        telefono = datosCliente.cleaned_data.get("telefono")
        fotoPerfil = datosCliente.cleaned_data.get("fotoPerfil")
        return self.crearCliente(rut,nombre,correo,telefono,fotoPerfil)

    def crearCliente(self,rut,nombre,correo,telefono,fotoPerfil):
        self.Cliente = Cliente.objects.create(rut=rut,nombre=nombre,correo=correo,telefono=telefono,fotoPerfil=fotoPerfil)
        return self.Cliente

    def getFunc(self):
        return self.Funcionario

    def getClient(self):
        return self.Cliente

    def setTerminoServicio(self):
        self.fecha_termino_servicio=datetime.now()
        self.save()

    def crearDetalle(self,idElemento,tipo):
        det = None
        if(tipo == "Bicicleta"):
            det,creado = Detalle.objects.get_or_create(servicio=self,bici=Bicicleta.objects.get(id=idElemento))
        elif(tipo == "EPP"):
            det,creado  = Detalle.objects.get_or_create(servicio=self,epp=EPP.objects.get(id=idElemento))
        elif(tipo == "Estacionamiento"):
            det,creado  = Detalle.objects.get_or_create(servicio=self,est=Estacionamiento.objects.get(id=idElemento))
        elif(tipo == "Herramienta"):
            det,creado  = Detalle.objects.get_or_create(servicio=self,herr=Herramienta.objects.get(id=idElemento))
        return det.getId()


class Elemento(models.Model):

    id = models.BigAutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    marca = models.CharField(max_length = 15, null=True, blank=True, default="Generico")
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    rut_funcionario = models.ForeignKey(Funcionario, name = "Funcionario",on_delete = SET_NULL,default="",null=True)

    class Meta:
        abstract = True

    def confirmarRegistro(self):
        self.fecha_ingreso = datetime.now()
        self.save()
    
    def getId(self):
        return self.id
    def getNombre(self):
        return self.nombre
    def getMarca(self):
        return self.marca

class EPP(Elemento):
    talla=models.CharField(max_length=10, null=True, blank=True,default="sin Talla")
    desechable=models.BooleanField()
    color=models.CharField(max_length=30, null=True, blank=True,default="No Especificado")

    def getListAdicional(self):
        return [("Talla",self.talla),("Desechable",self.desechable),("Color",self.color)]
    def getInfoAdicional(self,posicion):
        infos=[self.talla,self.desechable,self.marca]
        return infos[posicion]
    def getTipo(self):
        return "EPP"


class Herramienta(Elemento):
    instrucciones=models.CharField(max_length=100)
    desechable=models.BooleanField()
    requiere_epp=models.BooleanField()
    lista_epp=models.CharField(max_length=20, null=True, blank=True,default="No especificado")
    estado=models.CharField(max_length=50, null=True, blank=True,default="No especificado")

    def getListAdicional(self):
        return [("Instrucciones",self.instrucciones),("Desechable",self.desechable),("Requiere EPP",self.requiere_epp),("Lista EPP",self.lista_epp), ("Estado",self.estado)]
    def getInfoAdicional(self,posicion):
        infos=[self.instrucciones,self.desechable,self.requiere_epp,self.lista_epp,self.estado]
        return infos[posicion]
    def getTipo(self):
        return "Herramienta"

class Bicicleta(Elemento):
    color=models.CharField(max_length=10)
    observaciones=models.CharField(max_length=50, null=True, blank=True,default="No especificado")
    accesorios=models.CharField(max_length=50, null=True, blank=True,default="No especificado")
    activoFijo=models.BooleanField()
    estado=models.CharField(max_length=20)

    def getListAdicional(self):
        return [("Color",self.color),("Observaciones",self.observaciones),("Accesorios",self.accesorios),("Activo Fijo",self.activoFijo), ("Estado",self.estado)]
    def getInfoAdicional(self,posicion):
        infos=[self.color,self.observaciones,self.accesorios,self.activoFijo,self.estado]
        return infos[posicion]
    def getTipo(self):
        return "Bicicleta"

class Estacionamiento(Elemento):
    numero_estacionamiento=models.CharField(max_length=10)
    area=models.CharField(max_length=3, null=True, blank=True,default="")
    disponibilidad=models.BooleanField()

    def getListAdicional(self):
        return [("N° Estacionamiento",self.numero_estacionamiento),("Area",self.area),("Disponibilidad",self.disponibilidad)]
    def getInfoAdicional(self,posicion):
        infos=[self.numero_estacionamiento,self.area,self.disponibilidad]
        return infos[posicion]
    def getTipo(self):
        return "Estacionamiento"

class Detalle(models.Model):
    id_detalle = models.BigAutoField(primary_key = True)
    fecha_hora_entrega = models.DateTimeField(null=True)
    fecha_hora_entrega_real = models.DateTimeField(null=True)
    id_bici = models.ForeignKey(Bicicleta, name = "bici",on_delete = SET_NULL, default="",null=True)
    id_epp = models.ForeignKey(EPP, name = "epp",on_delete = SET_NULL, default="",null=True)
    id_est = models.ForeignKey(Estacionamiento, name = "est",on_delete = SET_NULL, default="",null=True)
    id_herr = models.ForeignKey(Herramienta, name = "herr",on_delete = SET_NULL, default="",null=True)

    num_servicio = models.ForeignKey(Servicio, name = "servicio",on_delete = CASCADE,default="",null=True)

    def getId(self):
        return self.id_detalle