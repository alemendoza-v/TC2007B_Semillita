from .models import Planta, Uso
from rest_framework import serializers

class UsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uso
        fields = ['nombre']

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = [
            'nombre_cientifico', 'nombre_tradicional', 'especie', 
            'origen', 'temporada', 'estatus', 'descripcion', 
            'fertilizante', 'riego', 'iluminacion', 'usos'
            ]