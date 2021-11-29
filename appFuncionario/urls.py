from django import views
from django.contrib import admin
from django.urls import path
from appFuncionario.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),
    path('badlogin',badlogin),
    path('home',home),
    path('registro',registro),
    path('confirmarRegistro',confirmarRegistro),
    path('confirmado',confirmado),
]
