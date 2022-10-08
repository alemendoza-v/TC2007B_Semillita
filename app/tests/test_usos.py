from rest_framework.test import APITestCase

from django.contrib.auth.models import User

import json
import os
class TestUsoViewSet(APITestCase):
    def setUp(self):
        # GIVEN
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        self.uri = '/api/usos/'
        self.data = {
            'username': 'Goldie',
            'password': 'testing1928',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_list(self):
        # WHEN
        request = self.client.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Uso list test passed")