from django.urls import path

from core import consumers

websocket_urlpatterns = [
    path('ws/chat', consumers.ChatConsumer),
]
