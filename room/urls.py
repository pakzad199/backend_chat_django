from django.urls import path, include
from rest_framework.routers import DefaultRouter
from room.views import RoomViewSet

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")

urlpatterns = [
    path("api/", include(router.urls)),
]
