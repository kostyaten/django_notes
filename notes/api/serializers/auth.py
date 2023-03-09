from typing import TypedDict

from django.contrib.auth import authenticate
from rest_framework import fields
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class ValidatedData(TypedDict):
    username: str
    password: str


class AuthSerializer(serializers.Serializer):
    username = fields.CharField()
    password = fields.CharField()

    @staticmethod
    def create(validated_data: ValidatedData) -> str:
        user = authenticate(username=validated_data.get('username'), password=validated_data.get('password'))
        if user is None:
            raise AuthenticationFailed(detail='Username or password is not correct')

        token, _ = Token.objects.get_or_create(user=user)
        return token.key


class AuthResponseSerializer(serializers.Serializer):
    access_token = fields.CharField()


class AuthDestroySerializer(serializers.Serializer):
    username = fields.CharField()
