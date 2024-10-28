from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Follow
from .serializer import UserSerializer, FollowSerializer
from .serializer import MyTokenObtainPairSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class UserPermission(permissions.IsAuthenticated):
    
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return super().has_permission(request, view)


class UserViewSet(viewsets.ModelViewSet):
    queryset =  User.objects.all().order_by('-username')
    serializer_class = UserSerializer
    permission_classes = [UserPermission]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (UserPermission,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.none()

    def create(self, request, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(User, id=request.data.get('following'))

        if not follower.id == following.id:
            follow, created = Follow.objects.get_or_create(follower=follower, following=following)

            if not created:
                return Response({'message': "You already follow this user"}, status=status.HTTP_409_CONFLICT)
            
            return Response({'message': f'{following.username} Followed successfull'})
        
        return Response({'message': 'Is not possible to follow yourself'}, status=status.HTTP_409_CONFLICT)
    
    def destroy(self, request, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(User, id=request.data.get('following'))

        follow = get_object_or_404(Follow, follower=follower, following=following)
        follow.delete()

        return Response({"message": f'You unfollowed {following.username}'})

    
 