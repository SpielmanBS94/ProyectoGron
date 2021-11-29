from django.shortcuts import render

# Create your views here.

def gron(request):
    return render(request,"login.html")
