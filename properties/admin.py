from django.contrib import admin
from .models import *

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1

class VirtualTourInline(admin.TabularInline):
    model = VirtualTour
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'agent', 'real_estate_type', 'price', 'status', 'created_at', 'featured')
    list_filter = ('status', 'real_estate_type', 'featured', 'created_at')
    search_fields = ('title', 'owner__username', 'agent__username', 'address__city')
    readonly_fields = ('created_at', 'updated_at', 'views')
    inlines = [PropertyImageInline, PropertyVideoInline, VirtualTourInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_primary', 'upload_date', 'order')
    list_filter = ('is_primary',)
    search_fields = ('property__title',)


@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('property', 'video_url', 'duration', 'upload_date')
    search_fields = ('property__title',)


@admin.register(VirtualTour)
class VirtualTourAdmin(admin.ModelAdmin):
    list_display = ('property', 'technology', 'upload_date')
    list_filter = ('technology',)
    search_fields = ('property__title',)


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(PropertyFeatureJunction)
class PropertyFeatureJunctionAdmin(admin.ModelAdmin):
    list_display = ('property', 'feature')
    search_fields = ('property__title', 'feature__name')
