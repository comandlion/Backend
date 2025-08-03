from django.contrib import admin
from .models import Offer, Transaction

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'amount', 'status', 'offer_date', 'expiration_date')
    list_filter = ('status', 'offer_date')
    search_fields = ('buyer__username', 'property__title')
    readonly_fields = ('offer_date',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'seller', 'agent', 'sale_price', 'status', 'transaction_date', 'closing_date')
    list_filter = ('status', 'transaction_date', 'closing_date')
    search_fields = ('buyer__username', 'seller__username', 'property__title')
    readonly_fields = ('transaction_date',)
