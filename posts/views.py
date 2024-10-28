from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Like
from users.models import Follow
from django.db.models import Subquery
from .serializer import PostSerializer, LikeSerializer
from django.shortcuts import get_object_or_404


# Create your views here.

class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.none()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        
        following_subquery = Follow.objects.filter(follower=user).values('following')
        queryset = Post.objects.filter(author__in=Subquery(following_subquery)).exclude(author=user).order_by('created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class LikeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.none()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.data.get('post'))
        user = request.user

        like, created =  Like.objects.get_or_create(post=post, user=user)

        if not created:
            return Response({'message': "you already had liked post"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'post liked successfull'}, status=status.HTTP_201_CREATED)
        
    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.data.get('post'))
        user = request.user

        like = get_object_or_404(Like, post=post, user=user)
        like.delete()

        return Response({"message": 'post disliked sucessfull'}, status=status.HTTP_204_NO_CONTENT)

        

