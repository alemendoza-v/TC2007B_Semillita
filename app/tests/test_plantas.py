from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import PlantaViewSet
from app.models import Planta, Uso

class TestPlantaViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.uri = '/api/plantas/'
        self.view = PlantaViewSet.as_view( {'get': 'list', 'post': 'create', 'delete': 'destroy'} )

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Planta list test passed")

    def test_create(self):
        Uso.objects.create(nombre='Test')
        data = {
            'nombre_cientifico': 'Test',
            'nombre_tradicional': 'Test',
            'especie': 'Test',
            'origen': 'Test',
            'temporada': 'Test',
            'estatus': True,
            'descripcion': 'Test',
            'fertilizante': 'Test',
            'riego': 'Test',
            'iluminacion': 'Test',
            'usos': ['1'],
        }
        request = self.factory.post(self.uri, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Planta create test passed")

    def test_retrieve(self):
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
        request = self.factory.get(self.uri)
        response = self.view(request, pk=planta.pk)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Planta retrieve test passed")    

    def test_delete(self):
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
        request = self.factory.delete(self.uri)
        response = self.view(request, pk=planta.pk)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))
        print("Planta delete test passed")