from django.contrib import admin
from .models import *

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'language')
    search_fields = ('name', 'currency', 'language')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Now a tuple with comma
    search_fields = ('name',)  # Now a tuple with comma

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'population', 'average_property_price')
    search_fields = ('name', 'state__name')
    list_filter = ('state',)

@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'average_price', 'crime_rate', 'school_quality')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'city', 'state_province', 'postal_code', 'country', 'neighborhood')
    search_fields = ('street_address', 'city', 'state_province', 'postal_code', 'country')
    list_filter = ('neighborhood',)
