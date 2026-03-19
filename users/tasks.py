from celery import shared_task
from .models import User

@shared_task
def hard_delete_user(user_id):

    try:
        user_for_delete = User.objects.get(id=user_id)
        if not user_for_delete.is_active:
            user_for_delete.delete()

    except User.DoesNotExist:
        pass