from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, CorrectTokenObtainPairView,
    soft_delete_user, toggle_visibility, get_user_records, get_me, reactivate_user)
urlpatterns = [
    path("auth/login/", CorrectTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path('delete_user/', soft_delete_user, name='delete_user'),
    path('toggle_visibility/', toggle_visibility, name='toggle_visibility'),
    path('get/', get_user_records, name="get_user_records"),
    path("me/", get_me, name="get_me"),
    path("reactivate_user/", reactivate_user, name="reactivate_user")

]

