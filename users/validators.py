from rest_framework import serializers


def validate_tg_username(tg_username):
    if tg_username and tg_username[0] != "@":
        raise serializers.ValidationError("The telegram username should start with @.")
