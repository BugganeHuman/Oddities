from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .models import User
from django.utils import timezone
from datetime import timedelta


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
надо - когда юзер отправляет правельную форму, в бд меняется: status = frozen, delete_date = +week

и тоесть юзер не может зайти на свой аккаунт, он может только перейти по эндпоинту востоновления 
(он AllowAny) и там ввести юзернейм и пароль и are_you_sure : yes и тогда акк востонавливается

когда пришла дата и время delete_date = +week аккаунт удаляется

"""

@api_view(['POST'])
def delete_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    are_you_sure = request.data.get('are_you_sure')
    write_delete = request.data.get('write_delete')

    if request.user.check_password(password) and are_you_sure == 'yes' and write_delete == 'delete':
        deleting_user = None
        try:
            deleting_user = User.objects.get(username=username)
        except Exception:
            return Response({'status' : f'user {username} did not found'})
        deleting_user.is_active = 'f'
        deleting_user.delete_date = timezone.now() + timedelta(weeks=1)
        deleting_user.save()

        return Response({'status' : f'user {username} will have deleted after one week. now he is frozen. '
                                    f'for unfreeze and save from deleting go to ...'})
    return None


"""
Middleware → URL → Authentication → Permissions → View → Serializer → Database.
"""