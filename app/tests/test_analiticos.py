from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import AnaliticosViewSet
from app.models import Planta, Uso, Analiticos

class TestAnaliticosViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.uri = '/api/analiticos/'
        self.view = AnaliticosViewSet.as_view( {'get': 'list'} )

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
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Analiticos list test passed")