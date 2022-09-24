from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from app.views import UserLogInView
from django.contrib.auth.models import User

class TestUserLogInView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.uri = '/api/login/'
        self.view = UserLogInView.as_view()

    def test_login(self):
        user = User.objects.create_user(
            username='Test',
            password='Test',
            email='Test',
            first_name='Test',
            last_name='Test',
        )
        data = {
            'username': 'Test',
            'password': 'Test',
        }
        request = self.factory.post(self.uri, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        print("User login test passed")