from django.urls import path
from .views import LinkListView, LinkCreateView, LinkRedirectView

urlpatterns = [
    path('', LinkListView.as_view(), name='link-list'),
    path('create/', LinkCreateView.as_view(), name='link-create'),
    path('go/<slug:short_code>/', LinkRedirectView.as_view(), name='link-redirect'),
]