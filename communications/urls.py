from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, MessageViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = router.urls