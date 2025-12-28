from django.urls import path
from .api_views import CurrentUserAPIView, RegisterAPIView

urlpatterns = [
    path('me/', CurrentUserAPIView.as_view(), name='user-me-api'),
    path('register/', RegisterAPIView.as_view(), name='user-register-api'),
]