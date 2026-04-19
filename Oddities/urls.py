from django.contrib import admin
from django.urls import path, include
from users.views import ping, backup
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/titles/", include("titles.urls")),
    path("api/watchlist/", include("watchlist.urls")),
    path("api/users/", include("users.urls")),
    path('api/ping/', ping),
    path('api/backup/', backup)
]
