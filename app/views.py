from rest_framework import viewsets, status
from rest_framework.response import Response

from app.models import Planta, Imagen
from app.serializers import PlantaSerializer, ImagenSerializer

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import base64
class PlantaViewSet(viewsets.ModelViewSet):
    serializer_class = PlantaSerializer

    def get_queryset(self):
        queryset = Planta.objects.all().filter(estatus=True).order_by('id')
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            new_plant = Planta.objects.create(
                nombre_cientifico=data['nombre_cientifico'],
                nombre_tradicional=data['nombre_tradicional'],
                especie=data['especie'],
                origen=data['origen'],
                temporada=data['temporada'],
                estatus=True,
                descripcion=data['descripcion'],
                fertilizante=data['fertilizante'],
                riego=data['riego'],
                iluminacion=data['iluminacion'],
            )
            new_plant.save()
            new_plant.usos.add(data['usos'])
            serializer_context = {
                'request': request,
            }
            serializer = PlantaSerializer(new_plant, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ImagenViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenSerializer

    def get_queryset(self):
        queryset = Imagen.objects.all().order_by('id')
        return queryset

    def create(self, request):
        data = request.data
        image = request.FILES.get('dato').read()
        image_encoded = base64.b64encode(image).decode('ascii')

        new_image = Imagen.objects.create(
            dato=image_encoded,
            tipo=data['tipo'],
        )
        new_plant = get_object_or_404(Planta, pk=data['planta_id'])
        new_image.planta = new_plant
        new_image.save()
        serializer_context = {
            'request': request,
        }
        serializer = ImagenSerializer(new_image, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        image = get_object_or_404(Imagen, pk=pk)
        
        return Response(image.dato, content_type=image.tipo, status=status.HTTP_200_OK)