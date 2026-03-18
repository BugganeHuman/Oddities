from celery import shared_task
from .models import User

@shared_task
def hard_delete_user(user_id):
    print("----in hard_delete_user")
    try:
        user_for_delete = User.objects.get(id=user_id)
        user_for_delete.delete()
        print("---------in hard_delete_user DELETED")
    except User.DoesNotExist:
        pass