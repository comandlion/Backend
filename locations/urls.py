from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'neighborhoods', NeighborhoodViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'currencies', CurrencyViewSet)

urlpatterns = router.urls