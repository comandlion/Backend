from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'listing_type', 'price', 'status', 'date_listed', 'expiration_date')
    list_filter = ('listing_type', 'status', 'date_listed')
    search_fields = ('property__title', 'status')
    readonly_fields = ('date_listed', 'date_updated')
