from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import UsosViewSet
from app.models import Uso

class TestUsoViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.uri = '/api/usos/'
        self.view = UsosViewSet.as_view( {'get': 'list', 'post': 'create', 'delete': 'destroy'} )

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Uso list test passed")

    def test_create(self):
        data = {
            'nombre': 'Test',
        }
        request = self.factory.post(self.uri, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Uso create test passed")

    def test_retrieve(self):
        uso = Uso.objects.create(nombre='Test')
        request = self.factory.get(self.uri)
        response = self.view(request, pk=uso.pk)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Uso retrieve test passed")

    def test_delete(self):
        uso = Uso.objects.create(nombre='Test')
        request = self.factory.delete(self.uri)
        response = self.view(request, pk=uso.pk)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))
        print("Uso delete test passed")