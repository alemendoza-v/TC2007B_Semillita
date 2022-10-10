from rest_framework.test import APITestCase

from app.models import Planta, Uso, Analiticos

from django.contrib.auth.models import User

import json
import os
class TestAnaliticosViewSet(APITestCase):
    def setUp(self):
        # GIVEN
        # Create a user.
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        self.uri = '/api/analiticos/'
        self.data = {
            'username': 'Goldie',
            'password': 'testing1928',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_list(self):
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
        Analiticos.objects.create(
            planta=planta
        )
        # WHEN
        response = self.client.get(self.uri, HTTP_AUTHORIZATION='Bearer ' + self.token)
        # THEN
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Analiticos list test passed")