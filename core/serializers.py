from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import Message
from rest_framework.serializers import ModelSerializer, CharField


class MessageSerializer(ModelSerializer):
    sender = CharField(source='sender.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = Message(recipient=recipient,
                      body=validated_data['body'],
                      sender=user)
        msg.save()
        return msg

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'timestamp', 'body')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
