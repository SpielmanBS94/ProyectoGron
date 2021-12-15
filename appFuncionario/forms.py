from django import forms
from django.db.models.fields import CharField
from appFuncionario.models import *

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['deuda']

class BicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = '__all__'
        exclude = ['fecha_ingreso','fecha_baja','Funcionario']

class EPPForm(forms.ModelForm):
    class Meta:
        model = EPP
        fields = '__all__'
        exclude = ['fecha_ingreso','fecha_baja','Funcionario']

class EstacionamientoForm(forms.ModelForm):
    class Meta:
        model = Estacionamiento
        fields = '__all__'
        exclude = ['fecha_ingreso','fecha_baja','Funcionario']

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = '__all__'
        exclude = ['fecha_ingreso','fecha_baja','Funcionario']