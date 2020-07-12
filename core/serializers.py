from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from core.models import Message, ChatGroup
from rest_framework.serializers import ModelSerializer, CharField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ChatGroupSerializer(ModelSerializer):
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = ChatGroup
        fields = ('id', 'name', 'members')


class MessageSerializer(ModelSerializer):
    sender = CharField(source='sender.username', read_only=True)
    group = ChatGroupSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'group', 'timestamp', 'body')


