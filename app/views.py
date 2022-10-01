from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app.models import Planta, Imagen, Analiticos, Uso
from app.serializers import PlantaSerializer, ImagenSerializer, UsoSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.urls import reverse

import os
import smtplib
from email.message import EmailMessage
import base64
import qrcode
from io import BytesIO

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# This class is a viewset that allows us to create, retrieve, update, and delete Usos objects.
class UsosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Uso.objects.all().order_by('nombre')
    serializer_class = UsoSerializer

# This class is a viewset that allows you to create, retrieve, update, and delete plants
class PlantaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        It returns a queryset of all the plants that are active (estatus=True) and ordered by id
        :return: A queryset of all the plants that are active.
        """
        queryset = Planta.objects.all().filter(estatus=True).order_by('id')
        return queryset

    def create(self, request):
        """
        It creates a new plant.
        
        :param request: The request plant object
        :return: The created plant object.
        """
        data = request.data
        try:
            # It's creating a new plant object.
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
            # It's adding the usos to the plant object.
            for u in data['usos']:
                uso = Uso.objects.get(id=u)
                new_plant.usos.add(uso)
            new_plant.save()
            # It's serializing the new_plant object and returning it as a response.
            context = {
                'request': request,
            }
            serializer = PlantaSerializer(new_plant, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        It's changing the estatus attribute of the plant object to False
        
        :param request: The request plant object id
        :return: It's returning a Response object with the status code 204.
        """
        try:
            planta = get_object_or_404(Planta, pk=kwargs['id'])
            # It's changing the estatus attribute of the plant object to False.
            planta.estatus = False
            planta.save()
            return Response("Cambio el estado de la planta " + planta.nombre_cientifico + "a falso", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        It takes a request, and returns a response
        
        :param request: The request plant object
        :return: The retrieved plant object.
        """
        try:
            planta = get_object_or_404(Planta, pk=kwargs['id'])
            context = {
                'request': request,
            }
            serializer = PlantaSerializer(planta, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            plant = get_object_or_404(Planta, pk=kwargs['id'])
            plant.nombre_cientifico = data['nombre_cientifico']
            plant.nombre_tradicional = data['nombre_tradicional']
            plant.especie = data['especie']
            plant.origen = data['origen']
            plant.temporada = data['temporada']
            plant.descripcion = data['descripcion']
            plant.fertilizante = data['fertilizante']
            plant.riego = data['riego']
            plant.iluminacion = data['iluminacion']
            plant.usos.clear()
            for u in data['usos']:
                uso = Uso.objects.get(id=u)
                plant.usos.add(uso)
            plant.save()
            imgs = Imagen.objects.all().filter(planta_id=kwargs['id'])
            if imgs.exists():
                imgs.delete()
            context = {
                'request': request,
            }
            serializer = PlantaSerializer(plant, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
# This class is a viewset that allows you to create, retrieve, update, and delete images
class ImagenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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
        
        :param request: The request image object
        :return: The created image object
        """
        try:
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
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, pk=None):
        """
        It takes the image from the database and returns it as a response
        
        :param pk: The primary key of the image you want to retrieve
        :return: The image data and the content type of the image.
        """
        try:
            image = get_object_or_404(Imagen, pk=pk)
            
            return Response(image.dato, content_type=image.tipo, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# This class is a viewset that allows you to create, retrieve, update, and delete instances of the
# Analiticos model.
class AnaliticosViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        """
        I'm getting the top 3 plants with the most number of Analiticos objects associated with them
        
        :param response: The response object that will be returned to the client
        :return: A list of dictionaries.
        """
        if Analiticos.objects.all().count() > 0: # If there are any Analiticos objects in the database
            try:
                plant_list = []

                for plant in Planta.objects.all().filter(estatus=True):
                    temp_plant_dict = {}
                    temp_plant_dict['id'] = plant.id
                    temp_plant_dict['name'] = plant.nombre_tradicional
                    temp_plant_dict['count'] = Analiticos.objects.all().filter(planta_id=plant.id).count()
                    plant_list.append(temp_plant_dict)

                y_pos = np.arange(len(plant_list))
                names = [dic["name"] for dic in plant_list]
                performance = [dic["count"] for dic in plant_list]

                plt.bar(y_pos, performance, align='center', alpha=0.5)
                plt.xticks(y_pos, names)
                plt.ylabel('Visitas')
                plt.title('Visitas por planta') 

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)                

                # It's getting the top 3 plants with the most number of Analiticos objects associated with
                # them.
                popularPlantsSortedIDs = [plant['id'] for plant in sorted(plant_list, key=lambda x: x['count'], reverse=True)[0:3]]
                # We serualize the data and return it as a response.
                popularPlantsSerialized = [PlantaSerializer(plant).data for plant in Planta.objects.filter(id__in=popularPlantsSortedIDs)]

                response = {
                    'popularPlants': popularPlantsSerialized,
                    'graph': base64.b64encode(buffer.read()).decode('ascii')
                } 

                return Response(response, status=status.HTTP_200_OK)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else: # If there are no Analiticos objects in the database
            return Response(status=status.HTTP_204_NO_CONTENT)

# This class is used to create qr codes
class CreateQR(APIView):
    permission_classes = [IsAuthenticated]
    # It takes a plant id, creates a QR code with the url of the plant detail page, and returns the QR
    # code as a base64 encoded string
    def get(self, request):
        try:
            data = request.GET['planta_id']
            plant = get_object_or_404(Planta, pk=data)
            qrData = "https://tc2007b-semillita.herokuapp.com" + reverse('planta_detail', args=[plant.id])
            img = qrcode.make(qrData)

            with BytesIO() as f:
                img.save(f, format='PNG')
                img_decoded = base64.b64encode(f.getvalue()).decode('ascii')
                return Response(img_decoded, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
            image = request.FILES.get('dato').read()

            sender_email = os.getenv('EMAIL_USER')
            receiver_email = User.objects.get(first_name= 'Alejandro').email
            subject = "Codigo QR para la planta " + request.data['nombre_tradicional']

            new_email = EmailMessage()
            new_email['Subject'] = subject
            new_email['From'] = sender_email
            new_email['To'] = receiver_email

            new_email.add_attachment(image, maintype='image', subtype='png', filename=request.data['nombre_tradicional'] + '.png')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
                smtp.send_message(new_email)
                
            return Response("QR Enviado Exitosamente", status=status.HTTP_200_OK)

        except:
            return Response("QR No Enviado", status=status.HTTP_400_BAD_REQUEST)

# This class is used to send information to the plant detail page
class PlantaDetailView(DetailView):
    model = Planta
    """
    It takes the context data from the parent class, adds the usos and imagen data to it, and returns
    the new context data
    :return: The context is a dictionary that contains the data that is used to render the template.
    """
    exclude = ['id', 'created_at', 'updated_at']
    template_name = 'planta_detail.html'

    def get_context_data(self, **kwargs):
        # Create analiticos registry
        registry = Analiticos.objects.create(planta_id=kwargs['object'].id)
        registry.save()
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        context['usos'] = list(context['object'].usos.all())
        context['imagen'] = str(context['object'].Pimagenes.all()[0].dato)
        return context

# This class is used to get data of a single plant using its traditional name
class PlantaGetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        """
        It gets the plant with the name passed in the url, and if it exists, it returns the plant's data in
        JSON format
        
        :param request: The request object
        :return: The plant object in JSON format
        """
        try:
            plant = Planta.objects.all().filter(nombre_tradicional=kwargs['nombre_tradicional']).filter(estatus=True)[0]
            serializer = PlantaSerializer(plant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)