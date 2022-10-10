from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Planta, Uso

from django.contrib.auth.models import User

import json
import os

class TestPlantaGetView(APITestCase):
    def setUp(self):
        # GIVEN
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        # Plant view URI
        self.uri = '/api/planta/'
        # Getting token
        self.data = {
            'username': 'Goldie',
            'password': 'testing1928',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_get_01(self):
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
        # WHEN
        response = self.client.get(self.uri + planta.nombre_tradicional + "/", HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Planta Name Lookup get test 01 passed")

    def test_get_02(self):
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
        # WHEN
        response = self.client.get(self.uri + planta.nombre_cientifico + "/", HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(response.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(response.status_code))
        print("Planta Name Lookup get test 02 passed")