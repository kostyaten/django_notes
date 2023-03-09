from typing import TypedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework import fields


class ValidatedData(TypedDict):
    password: str


class UserSerializer(serializers.ModelSerializer):
    password = fields.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'last_name', 'first_name', 'email', 'password')

    def create(self, validated_data: ValidatedData):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data=validated_data)
