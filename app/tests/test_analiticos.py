from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import AnaliticosViewSet
from app.models import Planta, Uso, Analiticos

from django.contrib.auth.models import User
import json
class TestAnaliticosViewSet(APITestCase):
    def setUp(self):
        # Create a user.
        self.user = User.objects.create_user(
            username='Test',
            password='Test',
            email='Test',
            first_name='Test',
            last_name='Test',
        )
        self.user.save()
        self.factory = APIRequestFactory()
        self.uri = '/api/analiticos/'
        self.view = AnaliticosViewSet.as_view( {'get': 'list'} )
        self.data = {
            'username': 'Test',
            'password': 'Test',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_list(self):
        planta = Planta.objects.create(
            nombre_cientifico='Test',
            nombre_tradicional='Test',
            especie='Test',
            origen='Test',
            temporada='Test',
            estatus=True,
            descripcion='Test',
            fertilizante='Test',
            riego='Test',
            iluminacion='Test',
        )
        planta.usos.add(Uso.objects.create(nombre='Test'))
        Analiticos.objects.create(
            planta=planta
        )
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Analiticos list test passed")