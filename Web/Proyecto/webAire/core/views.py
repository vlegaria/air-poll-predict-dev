from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request,"core/home.html")
def pronostico(request):
    return render(request,"core/pronostico.html")
def conocenos(request):
    return render(request,"core/conocenos.html")
def contacto(request):
    return render(request,"core/contacto.html")