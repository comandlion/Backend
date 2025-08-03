# from rest_framework import viewsets
# from .models import Listing
# from .serializers import ListingSerializer
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from interactions.models import Like, Favorite, Comment
#
#
# class ListingViewSet(viewsets.ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def like(self, request, pk=None):
#         listing = self.get_object()
#         like, created = Like.objects.get_or_create(user=request.user, listing=listing)
#         if not created:
#             return Response({'detail': 'You already liked this listing.'}, status=400)
#         return Response({'detail': 'Liked successfully.'}, status=201)
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def favorite(self, request, pk=None):
#         listing = self.get_object()
#         favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
#         if not created:
#             return Response({'detail': 'Already favorited.'}, status=400)
#         return Response({'detail': 'Added to favorites.'}, status=201)
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def comment(self, request, pk=None):
#         listing = self.get_object()
#         content = request.data.get('content')
#         if not content:
#             return Response({'detail': 'Comment cannot be empty.'}, status=400)
#         comment = Comment.objects.create(user=request.user, listing=listing, content=content)
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data, status=201)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Listing
from .serializers import ListingSerializer
from interactions.serializers import *
from properties.serializers import *


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        listing = self.get_object()
        comments = listing.commented_by.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        listing = self.get_object()
        likes = listing.liked_by.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        listing = self.get_object()
        favorites = listing.favorited_by.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def property_details(self, request, pk=None):
        listing = self.get_object()
        property = listing.property
        serializer = PropertySerializer(property)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        listing = self.get_object()
        user = request.user

        data = {
            'is_liked': Like.objects.filter(
                user=user,
                listing=listing
            ).exists(),
            'is_favorite': Favorite.objects.filter(
                user=user,
                listing=listing
            ).exists(),
            'like_count': listing.liked_by.count(),
            'favorite_count': listing.favorited_by.count(),
        }
        return Response(data)