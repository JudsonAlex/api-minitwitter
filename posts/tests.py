from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Post, Like
from users.models import User, Follow

class PostTestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse('api:token_obtain_pair')  
        self.post_url = reverse('api:posts:posts') 
        self.like_url = reverse('api:posts:like-create')  
        self.dislike_url = reverse('api:posts:like-delete')  

      
        self.author = User.objects.create_user(username='author', password='123456', email='author@example.com')
        self.follower = User.objects.create_user(username='follower', password='123456', email='follower@example.com')
        self.author2 = User.objects.create_user(username='author2', password='123456', email='author2@example.com')

        login_data = {'username': 'follower', 'password': '123456'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']  
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

       
        Follow.objects.create(follower=self.follower, following=self.author)

    def test_create_post(self):
        
        
        data = {'content': 'Meu primeiro post!', 'author': self.author.id}
        response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_list_posts_from_following(self):
        
        
        Post.objects.create(content='Meu primeiro post!', author=self.author)
        Post.objects.create(content='Meu segundo post!', author=self.author)
        Post.objects.create(content='Meu post author 2!', author=self.author2)

        
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        

        Follow.objects.create(follower=self.follower, following=self.author2)
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)



    def test_like_post(self):
        
        post = Post.objects.create(content='Meu primeiro post!', author=self.author)

        
        data = {'post': post.id}
        response = self.client.post(self.like_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post=post, user=self.follower).exists())

    def test_unlike_post(self):
        
        post = Post.objects.create(content='Meu primeiro post!', author=self.author)
        Like.objects.create(post=post, user=self.follower)

        
        data = {'post': post.id}
        response = self.client.post(self.dislike_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(post=post, user=self.follower).exists())

    def test_like_post_already_liked(self):
        
        post = Post.objects.create(content='Meu primeiro post!', author=self.author)
        Like.objects.create(post=post, user=self.follower)

        
        data = {'post': post.id}
        response = self.client.post(self.like_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
