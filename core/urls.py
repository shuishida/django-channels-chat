from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageViewSet, MemberList

router = DefaultRouter()
router.register('', MessageViewSet, basename='message-api')

urlpatterns = [
    path("api/v1/user/", MemberList.as_view()),
    path(r'api/v1/message/<str:contact>/', include(router.urls)),
    path('', login_required(
        TemplateView.as_view(template_name='core/chat.html')), name='home'),
]
