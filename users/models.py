from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', through='Follow')
    followers_count = models.IntegerField(default=0)
    email = models.EmailField(unique=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set',on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set',on_delete=models.CASCADE)



