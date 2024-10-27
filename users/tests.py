from .models import User, Follow
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class AuthenticationTestCase(APITestCase):
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


class FollowTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('api:token_obtain_pair')  # URL de login para obter o token
        self.follow_url = reverse('api:users:follow')  # Ajuste conforme o nome da sua URL de seguir

        # Criação dos usuários
        self.follower = User.objects.create_user(username='follower', password='123456', email='follower@example.com')
        self.following = User.objects.create_user(username='following', password='123456', email='following@example.com')

        # Fazer login e obter o token JWT
        login_data = {
            'username': 'follower',
            'password': '123456'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']  # Armazena o token de acesso JWT

        # Configura o cabeçalho de autorização com o token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_follow_user(self):
        data = {'following': self.following.id}
        response = self.client.post(self.follow_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Follow.objects.filter(follower=self.follower, following=self.following).exists())

    def test_follow_yourself(self):
        data = {'following': self.follower.id}
        response = self.client.post(self.follow_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_unfollow_user(self):
        # Primeiro, seguir o usuário
        Follow.objects.create(follower=self.follower, following=self.following)
        data = {'following': self.following.id}
        response = self.client.delete(self.follow_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(follower=self.follower, following=self.following).exists())