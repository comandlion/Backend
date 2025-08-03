from rest_framework import serializers
from .models import SavedSearch, Favorite, Like, Comment, PropertyView, Review
from properties.models import Property
from listings.models import Listing

class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False, allow_null=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']  # user is not expected from frontend


class LikeSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False, allow_null=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user']  # user is not expected from frontend

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'date_added', 'username', 'property', 'listing']
        read_only_fields = ['user']

class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyView
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
