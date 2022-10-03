from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.views import ImagenViewSet
from app.models import Imagen, Planta, Uso

from django.contrib.auth.models import User
import json
class TestImagenViewSet(APITestCase):
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
        self.uri = '/api/imagenes/'
        self.view = ImagenViewSet.as_view( {'get': 'list', 'post': 'create', 'delete': 'destroy'} )
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
        print("Imagen list test passed")

    def test_create(self):
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        data = {
            'dato': image,
            'tipo': 'image/jpg',
            'planta_id': planta.pk,
        }
        request = self.factory.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Imagen create test passed")

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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        imagen = Imagen.objects.create(
            dato=image,
            tipo='image/jpg',
            planta_id=planta.pk,
        )
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request, pk=imagen.pk)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Imagen retrieve test passed")

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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        imagen = Imagen.objects.create(
            dato=image,
            tipo='image/jpg',
            planta_id=planta.pk,
        )
        request = self.factory.delete(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request, pk=imagen.pk)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))
        print("Imagen delete test passed")