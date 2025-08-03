from django.contrib import admin
from .models import SavedSearch, Favorite, Like, Comment, PropertyView, Review

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('search_name', 'user', 'notification_frequency', 'created_at')
    search_fields = ('search_name', 'user__username')
    list_filter = ('notification_frequency',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'listing', 'date_added', 'id')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('date_added',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'listing', 'date_added', 'id')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('date_added',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'property_id', 'listing', 'content', 'date_added')
    search_fields = ('user__username', 'listing__title', 'content')
    list_filter = ('date_added',)

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'view_date', 'ip_address')
    search_fields = ('user__username', 'property__title', 'ip_address')
    list_filter = ('view_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'property', 'rating', 'review_date')
    search_fields = ('reviewer__username', 'reviewee__username', 'property__title')
    list_filter = ('rating', 'review_date')
