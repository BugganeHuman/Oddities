from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import WatchlistItemSerializer
from .models import WatchlistItem

class WatchlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistItemSerializer
    queryset = WatchlistItem.objects.all()
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save (owner = self.request.user)

    def get_queryset(self):
        return WatchlistItem.objects.filter(owner= self.request.user)