from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/titles/", include("core.urls")),
    path("api/watchlist/", include("watchlist.urls")),
    path("api/users/", include("users.urls")),
]
