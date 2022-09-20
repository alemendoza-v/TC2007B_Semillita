from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


from app.models import Planta
from app.serializers import PlantaSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    serializer_class = PlantaSerializer

    def get_queryset(self):
        queryset = Planta.objects.all().filter(estatus=True).order_by('id')
        return queryset

    #@action(detail=False, methods=['post'], url_path='create')
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
        