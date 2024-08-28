from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from apicalidadaire.models import *
from apicalidadaire.serializers import *

import os

from apicalidadaire.prediccion.prediction import prediction

# Create your views here.


class prediccion(APIView):

    def get_object(self, id):
        try:
            return Prediccion.objects.get(idPrediccion=id)
        except Prediccion.DoesNotExist:
            raise Prediccion

    def post(self, request, format=None):
        contaminante =  request.POST.get("contaminante")
        prediccion1 = request.POST.get("prediccion1")

        predictionSel = True
        if(prediccion1 == "True"):
            predictionSel = False

        try:
            #Prediccion mer
            idPrediccion = prediction(27, predictionSel, contaminante)

            prediccion = self.get_object(idPrediccion)

            prediccionSerializer = PrediccionSerializer(prediccion)

            return Response(prediccionSerializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            print("Ocurrió un error:", e)

            return Response(status=status.HTTP_400_BAD_REQUEST)


        
