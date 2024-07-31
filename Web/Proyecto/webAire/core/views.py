from django.shortcuts import render, HttpResponse
html_base="""
<h1> Mi web personal </h1>
<u1>
    <l1><a href="/">Portada</a></li>
    <l1><a href="/about/">Modulo de Pronóstico</a></li>
    <l1><a href="/about/">Conócenos</a></li>
    <l1><a href="/about/">Contacto</a></li>
</u1>
"""

# Create your views here.
def home(request):
    return HttpResponse(html_base+"<h1>Portada</h1>")
def pronostico(request):
    return HttpResponse(html_base+"<h1>Módulo de Pronóstico</h1>")
def conocenos(request):
    return HttpResponse(html_base+"<h1>Conócenos</h1>")
def contacto(request):
    return HttpResponse(html_base+"<h1>Contacto</h1>")