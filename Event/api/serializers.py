from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView

from Event import models
from Event.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        write_only_fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['name', 'description', 'meeting_time', 'users']
