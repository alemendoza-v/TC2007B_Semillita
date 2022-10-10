from rest_framework.test import APITestCase

from django.contrib.auth.models import User

import json
import os

class TestLogin(APITestCase):
    def setUp(self):
        # GIVEN
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        self.token_uri = '/api/token/'
        self.token_refresh_uri = '/api/token/refresh/'

    def test_login_01(self):
        # WHEN
        response = self.client.post(
            self.token_uri,
            data=json.dumps({
                'username': 'Goldie',
                'password': 'testing1928',
            }),
            content_type='application/json',
        )
        # THEN
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print('Login test 01 passed')
    
    def test_login_02(self):
        # WHEN
        response = self.client.post(
            self.token_uri,
            data=json.dumps({
                'username': 'Goldie',
                'password': 'incorrect',
            }),
            content_type='application/json',
        )
        # THEN
        self.assertEqual(response.status_code, 401, 'Expected Response Code 401, received {0} instead.'.format(response.status_code))
        print('Login test 02 passed')

    def test_login_03(self):
        # WHEN
        response = self.client.post(
            self.token_uri,
            data=json.dumps({
                'username': 'incorrect',
                'password': 'testing1928',
            }),
            content_type='application/json',
        )
        # THEN
        self.assertEqual(response.status_code, 401, 'Expected Response Code 401, received {0} instead.'.format(response.status_code))
        print('Login test 03 passed')
    
    def test_refresh(self):
        # WHEN
        response = self.client.post(
            self.token_uri,
            data=json.dumps({
                'username': 'Goldie',
                'password': 'testing1928',
            }),
            content_type='application/json',
        )
        refresh = response.data['refresh']
        response = self.client.post(
            self.token_refresh_uri,
            data=json.dumps({
                'refresh': refresh,
            }),
            content_type='application/json',
        )
        # THEN
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print('Refresh test passed')