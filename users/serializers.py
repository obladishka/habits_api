from rest_framework import serializers

from users.models import User
from users.validators import validate_tg_username


class UserSerializer(serializers.ModelSerializer):
    tg_username = serializers.CharField(validators=[validate_tg_username], required=False)

    class Meta:
        model = User
        fields = "__all__"
