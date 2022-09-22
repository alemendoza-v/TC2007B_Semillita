from .models import Planta, Uso, Imagen
from rest_framework import serializers

import base64

class UsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uso
        fields = ['nombre']

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['dato', 'tipo']

class PlantaSerializer(serializers.ModelSerializer):
    usos = serializers.StringRelatedField(many=True)
    Pimagenes = ImagenSerializer(many=True, read_only=True)
    class Meta:
        model = Planta
        fields = [
            'id', 'nombre_cientifico', 'nombre_tradicional', 'especie', 
            'origen', 'temporada', 'estatus', 'descripcion', 
            'fertilizante', 'riego', 'iluminacion', 'usos', 'Pimagenes'
            ]