from django.urls import path, include
from rest_framework.routers import DefaultRouter
from message.views import MessageViewSet, AttachmentViewSet
from room.views import RoomViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")

messages_router = NestedDefaultRouter(router, r'rooms', lookup='room')
messages_router.register(r'messages', MessageViewSet, basename='room-messages')

attachments_router = NestedDefaultRouter(messages_router, r'messages', lookup='message')
attachments_router.register(r'attachments', AttachmentViewSet, basename='message-attachments')


urlpatterns = [
    path("api/", include(messages_router.urls)),
    path("api/", include(attachments_router.urls)),
]
