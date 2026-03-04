from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CorrectTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    return Response ({'status' : 'ok'})


"""
Middleware → URL → Authentication → Permissions → View → Serializer → Database.
"""