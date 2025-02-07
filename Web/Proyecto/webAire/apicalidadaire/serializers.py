from rest_framework import serializers
from apicalidadaire.models import  *

class estacionesCAMESerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediccion
        fields = '__all__'

class EstatusCalidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstatusCalidad
        fields = '__all__'

class ContaminantesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contaminantes
        fields = '__all__'

class UnidadesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unidades
        fields = '__all__'

class PrediccionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Prediccion
        fields = '__all__'

    def to_representation(self, instance):

        return {
            'idPredicicon' : instance.idPrediccion,
            'nombre_estacion' : instance.Estacion.name,
            'color_punto' : instance.Estatus.valorColor,
            'contaminante' : instance.Contaminante.descContaminante,
            'valor_contaminante' : instance.valorContaminante,
            'unidad' : instance.Unidad.descUnidad, 
            'recomendaciones' : instance.Estatus.recomendacion
        }
