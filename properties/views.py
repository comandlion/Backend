from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from interactions.serializers import *

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'real_estate_type', 'land_type', 'listing_type', 'city', 'state']
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'created_at', 'total_area']
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PropertyDetailSerializer
        return PropertySerializer

    def perform_create(self, serializer):
        prop_instance = serializer.save(owner=self.request.user)

        images = self.request.FILES.getlist('images')
        for image_file in images:
            PropertyImage.objects.create(property=prop_instance, image=image_file)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        property = self.get_object()
        property.views += 1
        property.save()
        return Response({'views': property.views})

    @action(detail=False)
    def featured(self, request):
        featured_properties = Property.objects.filter(featured=True)
        serializer = self.get_serializer(featured_properties, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def map_data(self, request):
        properties = self.filter_queryset(self.get_queryset())
        map_data = []
        for prop in properties:
            map_data.append({
                'id': prop.id,
                'title': prop.title,
                'location': f"{prop.city}, {prop.state}",
                'price': str(prop.price),
                'lat': float(prop.latitude),
                'lng': float(prop.longitude),
                'type': prop.category,
                'propertyType': prop.real_estate_type or prop.land_type,
                'image': prop.images.filter(is_primary=True).first().image.url if prop.images.filter(
                    is_primary=True).exists() else None
            })
        return Response(map_data)

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        prop = self.get_object()
        images = prop.images.all()
        serializer = PropertyImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        prop = self.get_object()
        comments = prop.commented_by.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        prop = self.get_object()
        likes = prop.liked_by.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        prop = self.get_object()
        favorites = prop.favorited_by.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        prop = self.get_object()
        reviews = prop.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        prop = self.get_object()
        user = request.user

        data = {
            'is_liked': Like.objects.filter(user=user, property=prop).exists(),
            'is_favorite': Favorite.objects.filter(user=user, property=prop).exists(),
            'like_count': prop.liked_by.count(),
            'favorite_count': prop.favorited_by.count(),
        }
        return Response(data)

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer

class PropertyVideoViewSet(viewsets.ModelViewSet):
    queryset = PropertyVideo.objects.all()
    serializer_class = PropertyVideoSerializer

class VirtualTourViewSet(viewsets.ModelViewSet):
    queryset = VirtualTour.objects.all()
    serializer_class = VirtualTourSerializer

class PropertyFeatureViewSet(viewsets.ModelViewSet):
    queryset = PropertyFeature.objects.all()
    serializer_class = PropertyFeatureSerializer

class PropertyFeatureJunctionViewSet(viewsets.ModelViewSet):
    queryset = PropertyFeatureJunction.objects.all()
    serializer_class = PropertyFeatureJunctionSerializer

class PropertySearchView(APIView):
    def post(self, request):
        # Advanced search with multiple filters
        filters = request.data
        queryset = Property.objects.all()

        if 'category' in filters:
            queryset = queryset.filter(category=filters['category'])

        if 'price_range' in filters:
            min_price = filters['price_range'].get('min', 0)
            max_price = filters['price_range'].get('max', 999999999)
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        if 'location' in filters:
            location = filters['location']
            if 'coordinates' in location and 'radius' in location:
                # Implement radius-based search using GeoDjango
                pass

        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)