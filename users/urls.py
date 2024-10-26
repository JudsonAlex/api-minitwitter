from django.urls import path
from .views import UserViewSet, FollowViewSet

app_name = 'users'

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create', 'get': 'list'}), name='users'),
    path('follows/', FollowViewSet.as_view({'post': 'create'}), name='follow-create'),
    path('follows/delete', FollowViewSet.as_view({'post': 'destroy'}), name='follow-delete')
]