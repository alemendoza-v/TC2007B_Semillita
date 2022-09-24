from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from app.models import Planta, Imagen, Analiticos, Uso
from app.serializers import PlantaSerializer, ImagenSerializer, UsoSerializer

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import base64

# This class is a viewset that allows us to create, retrieve, update, and delete Usos objects.
class UsosViewSet(viewsets.ModelViewSet):
    queryset = Uso.objects.all()
    serializer_class = UsoSerializer

# This class is a viewset that allows you to create, retrieve, update, and delete plants
class PlantaViewSet(viewsets.ModelViewSet):
    serializer_class = PlantaSerializer

    def get_queryset(self):
        """
        It returns a queryset of all the plants that are active (estatus=True) and ordered by id
        :return: A queryset of all the plants that are active.
        """
        queryset = Planta.objects.all().filter(estatus=True).order_by('id')
        return queryset

    def create(self, request):
        """
        It creates a new plant object with the data provided in the request, and then it adds the usos
        to the plant object.
        
        :param request: The request object
        :return: <code>{
            "nombre_cientifico": "",
            "nombre_tradicional": "",
            "especie": "",
            "origen": "",
            "temporada": "",
            "estatus": true,
            "descripcion": "",
            "fertilizante": "",
            "riego": "",
            "iluminacion": "",
        """
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
            # It's iterating through the usos array in the request data, and then it's adding each uso
            # to the plant object.
            for u in data['usos']:
                uso = Uso.objects.get(id=u)
                new_plant.usos.add(uso)
            new_plant.save()
            return HttpResponse("Planta creada", status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self):
        """
        It takes a request, and returns a response
        
        :param request: The request object
        :return: The response is a string with the name of the plant and the status of the plant.
        """
        planta = self.get_object()
        # It's changing the estatus attribute of the plant object to False.
        planta.estatus = False
        planta.save()
        return Response("Cambio el estado de la planta " + planta.nombre_cientifico + "a falso", status=status.HTTP_204_NO_CONTENT)

# This class is a viewset that allows you to create, retrieve, update, and delete images
class ImagenViewSet(viewsets.ModelViewSet):
    serializer_class = ImagenSerializer

    def get_queryset(self):
        """
        It returns a queryset of all the objects in the Imagen model.
        :return: A queryset of all the objects in the Imagen model.
        """
        queryset = Imagen.objects.all().order_by('id')
        return queryset

    def create(self, request):
        """
        I'm trying to create a new image object, and then assign it to a plant object
        
        :param request: The request object
        :return: The image is being returned as a base64 string.
        """
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

    def retrieve(self, pk=None):
        """
        It takes the image from the database and returns it as a response
        
        :param pk: The primary key of the image you want to retrieve
        :return: The image data and the content type of the image.
        """
        image = get_object_or_404(Imagen, pk=pk)
        
        return Response(image.dato, content_type=image.tipo, status=status.HTTP_200_OK)

# This class is a viewset that allows you to create, retrieve, update, and delete instances of the
# Analiticos model.
class AnaliticosViewSet(viewsets.ViewSet):

    def list(self):
        """
        I'm getting the top 3 plants with the most number of Analiticos objects associated with them
        
        :param response: The response object that will be returned to the client
        :return: A list of dictionaries.
        """
        plant_list = []

        for plant in Planta.objects.all():
            temp_plant_dict = {}
            temp_plant_dict['id'] = plant.id
            temp_plant_dict['count'] = Analiticos.objects.all().filter(planta_id=plant.id).count()
            plant_list.append(temp_plant_dict)

        # It's getting the top 3 plants with the most number of Analiticos objects associated with
        # them.
        popularPlantsSortedIDs = [plant['id'] for plant in sorted(plant_list, key=lambda x: x['count'], reverse=True)[0:3]]
        # We serualize the data and return it as a response.
        popularPlantsSerialized = [PlantaSerializer(plant).data for plant in Planta.objects.filter(id__in=popularPlantsSortedIDs)]

        return Response(popularPlantsSerialized, status=status.HTTP_200_OK)

# This class is a subclass of the APIView class, and it's purpose is to handle the user login process
class UserLogInView(APIView):
    def post(self, request):
        """
        If the user is authenticated, return the user's first name. Otherwise, return an error message
        
        :param request: The request object
        :return: The user's first name.
        """
        username = request.data[0]
        password = request.data[1]
        try:
            # It's authenticating the user.
            user = authenticate(username=username, password=password)
            if user is not None:
                return Response("Usuario autenticado", status=status.HTTP_200_OK)
        except:
            return Response("Usuario no encontrado o contraseña equivocada", status=status.HTTP_400_BAD_REQUEST)