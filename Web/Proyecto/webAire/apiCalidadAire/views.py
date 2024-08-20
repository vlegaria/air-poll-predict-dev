from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['POST'])
def prediccion(request):

    if request.method == 'POST':
        contaminante =  request.POST.get("contaminante")
        print(contaminante)
        prediccion1 = request.POST.get("prediccion1")
        print(prediccion1)
        prediccion24 = request.POST.get("prediccion24")
        print(prediccion24)

        texto = f'Se recibio {contaminante}, {prediccion1}, {prediccion24}'

        return Response(texto,status=status.HTTP_200_OK)
