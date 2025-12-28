from rest_framework import viewsets, permissions
from .models import Link
from .serializers import LinkSerializer

class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'short_code' 

    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)