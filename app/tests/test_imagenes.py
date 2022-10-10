from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Planta, Uso

from django.contrib.auth.models import User

import json
import os
class TestImagenViewSet(APITestCase):
    def setUp(self):
        # GIVEN
        # Create a user.
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        self.uri = '/api/imagenes/'
        self.data = {
            'username': 'Goldie',
            'password': 'testing1928',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_create_01(self):
        # GIVEN
        planta = Planta.objects.create(
            nombre_cientifico = 'Planta de prueba',
            nombre_tradicional = 'Plantita',
            especie = 'Arbusto',
            origen = 'Mexico',
            temporada = 'Invierno',
            descripcion = 'Buena planta',
            fertilizante = 'No necesita',
            riego = '100 ml diarios',
            iluminacion = 'Sombra parcial',
        )
        planta.usos.add(Uso.objects.create(nombre='Medicinal'))
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        data = {
            'dato': image,
            'tipo': 'image/jpg',
            'planta_id': planta.id,
        }
        # WHEN
        response = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Imagen create test 01 passed")

    def test_create_02(self):
        # GIVEN
        planta = Planta.objects.create(
            nombre_cientifico = 'Planta de prueba',
            nombre_tradicional = 'Plantita',
            especie = 'Arbusto',
            origen = 'Mexico',
            temporada = 'Invierno',
            descripcion = 'Buena planta',
            fertilizante = 'No necesita',
            riego = '100 ml diarios',
            iluminacion = 'Sombra parcial',
        )
        planta.usos.add(Uso.objects.create(nombre='Medicinal'))
        image = SimpleUploadedFile('planta.png', content=b'file_content', content_type='image/png')
        data = {
            'dato': image,
            'tipo': 'image/png',
            'planta_id': planta.id,
        }
        # WHEN
        response = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Imagen create test 02 passed")

    def test_create_03(self):
        # GIVEN
        planta = Planta.objects.create(
            nombre_cientifico = 'Planta de prueba',
            nombre_tradicional = 'Plantita',
            especie = 'Arbusto',
            origen = 'Mexico',
            temporada = 'Invierno',
            descripcion = 'Buena planta',
            fertilizante = 'No necesita',
            riego = '100 ml diarios',
            iluminacion = 'Sombra parcial',
        )
        planta.usos.add(Uso.objects.create(nombre='Medicinal'))
        image = SimpleUploadedFile('planta.png', content=b'file_content', content_type='image/png')
        data = {
            'dato': image,
            'tipo': 'image/png',
            'planta_id': planta.id + 10,
        }
        # WHEN
        response = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(response.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(response.status_code))
        print("Imagen create test 03 passed")
