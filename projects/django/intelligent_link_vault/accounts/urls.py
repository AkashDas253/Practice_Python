from django.urls import path
from .views import register_view
from rest_framework.authtoken.views import obtain_auth_token 
from .api_views import CurrentUserAPIView, RegisterAPIView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('me/', CurrentUserAPIView.as_view(), name='api_me'),
]