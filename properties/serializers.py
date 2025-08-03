from rest_framework import serializers
from .models import *
from locations.serializers import AddressSerializer  # Assuming you have this serializer
from Auth.serializers import UserProfileSerializer

class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PropertyImage
        fields = '__all__'

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = ['name', 'icon']

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = '__all__'

class VirtualTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = '__all__'


class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = '__all__'

class PropertyFeatureJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeatureJunction
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    agent = UserProfileSerializer(read_only=True)
    days_on_market = serializers.ReadOnlyField()
    coordinates = serializers.SerializerMethodField()
    dimensions = serializers.SerializerMethodField()

    videos = PropertyVideoSerializer(many=True, read_only=True)
    virtual_tours = VirtualTourSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Property._meta.get_field('address').related_model.objects.all(),
        write_only=True, source='address'
    )

    class Meta:
        model = Property
        fields = '__all__'

    def get_coordinates(self, obj):
        return {
            'lat': float(obj.latitude),
            'lng': float(obj.longitude)
        }

    def get_dimensions(self, obj):
        return obj.dimensions_3d or {}

class PropertyDetailSerializer(PropertySerializer):
    similar_properties = serializers.SerializerMethodField()

    def get_similar_properties(self, obj):
        similar = Property.objects.filter(
            category=obj.category,
            city=obj.city
        ).exclude(id=obj.id)[:3]
        return PropertySerializer(similar, many=True, context=self.context).data
