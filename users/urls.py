from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RregisterAPIView.as_view()),
    path('authorize/', AuthorizeAPIView.as_view())
]