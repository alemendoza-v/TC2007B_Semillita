from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import PlantaViewSet
from app.models import Planta, Uso, Imagen

from django.contrib.auth.models import User
import json
from django.core.files.uploadedfile import SimpleUploadedFile
class TestPlantaViewSet(APITestCase):
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
        self.uri = '/api/plantas/'
        self.view = PlantaViewSet.as_view( {'get': 'list', 'post': 'create', 'delete': 'destroy'} )
        self.data = {
            'username': 'Test',
            'password': 'Test',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_list(self):
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
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
        request = self.factory.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
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
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
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
        planta.save()
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.pk,
        )
        request = self.factory.delete(self.uri + str(planta.id), HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))
        print("Planta delete test passed")
    
    def test_update(self):
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
        planta.save()
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        planta.Pimagenes.add(Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        ))
        data = {
            'id' : planta.id,
            'nombre_cientifico': 'Test2',
            'nombre_tradicional': 'Test2',
            'especie': 'Test2',
            'origen': 'Test2',
            'temporada': 'Test2',
            'estatus': True,
            'descripcion': 'Test2',
            'fertilizante': 'Test2',
            'riego': 'Test2',
            'iluminacion': 'Test2',
            'usos': ['1'],
        }
        request = self.factory.put(self.uri + str(planta.id) + "/", data, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request, pk=planta.pk)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Planta update test passed")