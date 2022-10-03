from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import UsosViewSet
from app.models import Uso

from django.contrib.auth.models import User
import json
class TestUsoViewSet(APITestCase):
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
        self.uri = '/api/usos/'
        self.view = UsosViewSet.as_view( {'get': 'list', 'post': 'create', 'delete': 'destroy'} )
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
        print("Uso list test passed")

    def test_create(self):
        data = {
            'nombre': 'Test',
        }
        request = self.factory.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        print("Uso create test passed")

    def test_retrieve(self):
        uso = Uso.objects.create(nombre='Test')
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request, pk=uso.pk)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("Uso retrieve test passed")

    def test_delete(self):
        uso = Uso.objects.create(nombre='Test')
        request = self.factory.delete(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.view(request, pk=uso.pk)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))
        print("Uso delete test passed")