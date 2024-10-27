from django.urls import path
from .views import UserViewSet, FollowViewSet

app_name = 'users'

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create', 'get': 'list'}), name='user'),
    path('follows/', FollowViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='follow'),
    # path('follows/delete', FollowViewSet.as_view({'delete': 'destroy'}), name='follow')
]