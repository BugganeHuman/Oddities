from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import WatchlistItemSerializer
from .models import WatchlistItem

class WatchlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistItemSerializer
    queryset = WatchlistItem.objects.all()
    authentication_classes = [JWTAuthentication]