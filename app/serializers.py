from .models import Planta, Uso, Imagen
from rest_framework import serializers

class UsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uso
        fields = ['id', 'nombre']

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'dato', 'tipo']

class PlantaSerializer(serializers.ModelSerializer):
    usos = serializers.StringRelatedField(many=True)
    Pimagenes = ImagenSerializer(many=True, read_only=True)
    class Meta:
        model = Planta
        fields = [
            'id', 'nombre_cientifico', 'nombre_tradicional', 'especie', 
            'origen', 'temporada', 'estatus', 'descripcion', 
            'fertilizante', 'riego', 'iluminacion', 'usos', 'Pimagenes',
            ]