from rest_framework.serializers import ModelSerializer
from .models import Post, Like

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_at', 'likes_count')

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post', 'user')

    
