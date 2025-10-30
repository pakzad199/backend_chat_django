from django.urls import path, include
from rest_framework.routers import DefaultRouter
from message.views import MessageViewSet
from room.views import RoomViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
messages_router = NestedDefaultRouter(router, r'rooms', lookup='room')
messages_router.register(r'messages', MessageViewSet, basename='room-messages')


urlpatterns = [
    path("api/", include(messages_router.urls)),
]
