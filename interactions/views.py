from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from properties.models import Property
from listings.models import Listing
from .models import *
from .serializers import *

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of a comment to edit/delete it."""
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.user == request.user

class SavedSearchViewSet(viewsets.ModelViewSet):
    queryset = SavedSearch.objects.all()
    serializer_class = SavedSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='remove-favorite')
    def remove_favorite(self, request):
        user = request.user
        property_id = request.data.get('property')
        listing_id = request.data.get('listing')

        if property_id:
            favorite = Favorite.objects.filter(user=user, property_id=property_id).first()
        elif listing_id:
            favorite = Favorite.objects.filter(user=user, listing_id=listing_id).first()
        else:
            return Response({"detail": "Property or listing ID required"}, status=status.HTTP_400_BAD_REQUEST)

        if favorite:
            favorite.delete()
            return Response({"detail": "Favorite removed"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='remove-like')
    def remove_like(self, request):
        user = request.user
        property_id = request.data.get('property')
        listing_id = request.data.get('listing')

        if property_id:
            like = Like.objects.filter(user=user, property_id=property_id).first()
        elif listing_id:
            like = Like.objects.filter(user=user, listing_id=listing_id).first()
        else:
            return Response({"detail": "Property or listing ID required"}, status=status.HTTP_400_BAD_REQUEST)

        if like:
            like.delete()
            return Response({"detail": "Like removed"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # Filter comments by either property or listing from query params
    #     property_id = self.request.query_params.get('property')
    #     listing_id = self.request.query_params.get('listing')
    #
    #     queryset = Comment.objects.all()
    #     if property_id:
    #         queryset = queryset.filter(property_id=property_id)
    #     elif listing_id:
    #         queryset = queryset.filter(listing_id=listing_id)
    #     else:
    #         # Optionally, raise error if neither provided
    #         raise ValidationError("property or listing query parameter required.")
    #
    #     return queryset

    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        listing_id = self.request.data.get('listing')

        if not (property_id or listing_id):
            raise ValidationError("Either 'property' or 'listing' must be provided.")

        if property_id and listing_id:
            raise ValidationError("Only one of 'property' or 'listing' should be provided.")

        serializer.save(user=self.request.user)


class PropertyViewViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = PropertyViewSerializer
    queryset = PropertyView.objects.all()

    def create(self, request, *args, **kwargs):
        property_id = request.data.get('property')
        if not property_id:
            return Response(
                {"error": "property is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        property = get_object_or_404(Property, id=property_id)

        # Record the view
        PropertyView.objects.create(
            user=request.user if request.user.is_authenticated else None,
            property=property,
            ip_address=self.get_client_ip(request),
            session_id=request.session.session_key
        )

        # Update view count on property
        property.views_count += 1
        property.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        reviewee_id = request.data.get('reviewee')
        property_id = request.data.get('property')
        rating = request.data.get('rating')

        if not all([reviewee_id, property_id, rating]):
            return Response(
                {"error": "reviewee, property and rating are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user has already reviewed this property/reviewee
        existing = Review.objects.filter(
            reviewer=request.user,
            reviewee_id=reviewee_id,
            property_id=property_id
        ).exists()

        if existing:
            return Response(
                {"error": "You've already reviewed this property/agent"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)