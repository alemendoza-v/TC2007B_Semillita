from .models import Planta, Uso, Imagen
from rest_framework import serializers

# A serializer class that will be used to serialize the Uso model.
class UsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uso
        fields = ['id', 'nombre']

# A serializer class that will be used to serialize the model.
class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'dato', 'tipo']

# A serializer class that will be used to serialize the data from the model.
class PlantaSerializer(serializers.ModelSerializer):
    # A shortcut for a read-only field that returns the string representation of the objects.
    usos = serializers.StringRelatedField(many=True)
    # Creating a new field called Pimagenes that will be used to serialize the data from the Imagen model.
    Pimagenes = ImagenSerializer(many=True, read_only=True)
    class Meta:
        model = Planta
        fields = [
            'id', 'nombre_cientifico', 'nombre_tradicional', 'especie', 
            'origen', 'temporada', 'estatus', 'descripcion', 
            'fertilizante', 'riego', 'iluminacion', 'usos', 'Pimagenes',
            ]