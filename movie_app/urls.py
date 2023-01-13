from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

ROUTER = SimpleRouter()
ROUTER.register('movies', MovieViewSet)
ROUTER.register('directors', DirectorViewSet)
ROUTER.register('reviews', ReviewViewSet)
urlpatterns = [
    path('', include(ROUTER.urls))
]