from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Planta, Uso

from django.contrib.auth.models import User

import json
import os

class TestQrAPI(APITestCase):
    def setUp(self) -> None:
        # GIVEN
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        self.uri = '/api/qr/'
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
        request = self.client.get(self.uri + "?planta_id=" + str(planta.id), HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Qr get test 01 passed")

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
        request = self.client.get(self.uri + "?planta_id=" + str(planta.id + 10), HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Qr get test 02 passed")

    def test_post_01(self):
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
        image = SimpleUploadedFile("qr.png", b"file_content", content_type="image/png")
        data = {
            'dato': image,
            'nombre_tradicional': planta.nombre_tradicional,
        }
        # WHEN
        request = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Qr post test 01 passed")