from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class BotAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        bot_key = request.META.get('HTTP_X_BOT_KEY')
        tg_id = request.META.get('HTTP_X_TELEGRAM_ID')


        """
        # Прямо перед try: user = User.objects.get(...)
        all_users = User.objects.all().values('username', 'telegram_id')
        print(f"DEBUG: Список всех юзеров в БД: {list(all_users)}")
        print(f"DEBUG: Я ищу юзера с ID: {tg_id} (тип: {type(tg_id)})")
        """



        print(f"--- DEBUG BOT AUTH ---")
        print(f"KEY FROM BOT: {bot_key}")
        print(f"ID FROM BOT: {tg_id}")
        print(f"MASTER KEY IN SETTINGS: {settings.BOT_MASTER_KEY}")

        if not bot_key or bot_key != settings.BOT_MASTER_KEY:
            print(11111)
            return None

        try:
            user = User.objects.get(telegram_id=int(tg_id))
            return (user, None)
        except User.DoesNotExist:
            print(33333)
            raise exceptions.AuthenticationFailed('User not found')