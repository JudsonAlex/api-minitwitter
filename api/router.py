from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from users import urls as users_urls
# from posts import urls as posts_urls
from users.serializer import MyTokenObtainPairView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

api_urlpatterns = [
    path('users/', include(users_urls), name='users'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair')
    

]

app_name = "api"
urlpatterns = router.urls
urlpatterns += api_urlpatterns