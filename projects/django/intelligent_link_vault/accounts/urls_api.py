from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from .api_views import CurrentUserAPIView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', obtain_auth_token, name='api-login'),
    path('me/', CurrentUserAPIView.as_view(), name='api-me'),
]