from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('properties', PropertyViewSet)
router.register('property-images', PropertyImageViewSet)
router.register('property-videos', PropertyVideoViewSet)
router.register('virtual-tours', VirtualTourViewSet)
router.register('features', PropertyFeatureViewSet)
router.register('feature-junctions', PropertyFeatureJunctionViewSet)

urlpatterns = router.urls
