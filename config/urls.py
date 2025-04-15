from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("habits.urls", namespace="habits")),
    path("users/", include("users.urls", namespace="users")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="docs"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
