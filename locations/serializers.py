from rest_framework import serializers
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )

    class Meta:
        model = State
        fields = ['id', 'name', 'country', 'country_id', 'tax_information']


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), source='state', write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'state_id', 'population', 'description', 'average_property_price']


class NeighborhoodSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True
    )

    class Meta:
        model = Neighborhood
        fields = [
            'id', 'name', 'description', 'city', 'city_id',
            'average_price', 'crime_rate', 'school_quality', 'amenities_description'
        ]

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    neighborhood = NeighborhoodSerializer(read_only=True)
    neighborhood_id = serializers.PrimaryKeyRelatedField(
        queryset=Neighborhood.objects.all(), source='neighborhood', write_only=True, required=False
    )

    class Meta:
        model = Address
        fields = [
            'id', 'street_address', 'city', 'state_province',
            'postal_code', 'country', 'latitude', 'longitude',
            'neighborhood', 'neighborhood_id'
        ]
