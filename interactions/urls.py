from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'savedsearches', SavedSearchViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'propertyviews', PropertyViewViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls