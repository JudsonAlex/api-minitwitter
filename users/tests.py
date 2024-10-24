from django.test import TestCase
from .models import User
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class AuthenticationTestCase(TestCase):
    def setUp(self) -> None:
        self.user =  User.objects.create_user(username="judson", email='judson@email.com', password='123456')
        self.token_url = reverse('api:token_obtain_pair')

    def test_login_and_auth_jwt(self):
        response = self.client.post(self.token_url, {'username': 'judson', 'email': 'judson@email.com', 'password': '123456'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        token = response.data['access']

        protected_url = '/api/users/'
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        protected_response = self.client.get(protected_url, **headers)

        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)


