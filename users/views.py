from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CorrectTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


"""
Middleware → URL → Authentication → Permissions → View → Serializer → Database.
"""