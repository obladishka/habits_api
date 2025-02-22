from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("users/register", UserCreateAPIView.as_view(), name="create_user"),
    path("users/login", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="user_login"),
    path("users/token/refresh", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="user_token_refresh"),
]
