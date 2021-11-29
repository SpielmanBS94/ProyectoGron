from django.contrib import admin
from appFuncionario.models import *

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display=("rut","nombre","correo","deuda","telefono")
    search_fields=("rut","nombre","correo","deuda","telefono")

class funcAdmin(admin.ModelAdmin):
    list_display=("rut","usuario","contrasena")
    search_fields=("rut","usuario","contrasena")

class tarjetaAdmin(admin.ModelAdmin):
    list_display=("numero_tarjeta","habilitada","Dueno")
    search_fields=("numero_tarjeta","habilitada","Dueno")

class servAdmin(admin.ModelAdmin):
    list_display=("num_servicio","fecha_reserva_servicio","fecha_inicio_servicio","fecha_termino_servicio","Cliente","Funcionario")
    search_fields=("num_servicio","fecha_reserva_servicio","fecha_inicio_servicio","fecha_termino_servicio","Cliente","Funcionario")
    list_filter=("fecha_reserva_servicio","fecha_inicio_servicio","fecha_termino_servicio")

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Funcionario,funcAdmin)
admin.site.register(Tarjeta,tarjetaAdmin)
admin.site.register(Servicio,servAdmin)
