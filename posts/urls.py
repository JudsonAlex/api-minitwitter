from django.urls import path
from .views import PostViewSet, LikeViewSet

app_name = 'posts'

urlpatterns = [
    path('', PostViewSet.as_view({'post': 'create', 'get': 'list'}), name='posts'),
    path('like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('like/delete/', LikeViewSet.as_view({'post': 'destroy'}), name='like-delete'),
]