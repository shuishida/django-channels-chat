from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from chat import settings
from core.serializers import MessageSerializer, UserSerializer
from core.models import Message, ChatGroup


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def get_group(self):
        user = self.request.user
        contact_name = self.kwargs.get('contact')
        try:
            group = ChatGroup.objects.filter(members=user).filter(members__username=contact_name).get()
        except ChatGroup.DoesNotExist:
            contact = get_object_or_404(User, username=contact_name)
            group = ChatGroup()
            group.save()
            group.members.add(user, contact)
        return group

    def get_queryset(self):
        group = self.get_group()
        return group.messages.all()

    def perform_create(self, serializer):
        group = self.get_group()
        serializer.save(group=group, sender=self.request.user)


class MemberList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
