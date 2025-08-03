from django.db import models
from django.contrib.auth.models import User
from Auth.models import *
from locations.models import Address
from PIL import Image
from locations.models import Currency

# Create your models here.
class Property(models.Model):
    CATEGORY_CHOICES = [
        ('real_estate', 'Real Estate'),
        ('land', 'Land'),
    ]
    REAL_ESTATE_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('loft', 'Loft'),
        ('penthouse', 'Penthouse'),
        ('commercial', 'Commercial'),
    ]
    LAND_TYPES = [
        ('residential_land', 'Residential Land'),
        ('commercial_land', 'Commercial Land'),
        ('agricultural_land', 'Agricultural Land'),
        ('industrial_land', 'Industrial Land'),
        ('mixed_use_land', 'Mixed Use Land'),
        ('development_land', 'Development Land'),
    ]
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
        ('auction', 'Auction'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('off_market', 'Off Market'),
    ]

    # Basic Information
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    agent = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'user_type': 'agent'}, related_name='listed_properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True,)
    real_estate_type = models.CharField(max_length=20, choices=REAL_ESTATE_TYPES, null=True, blank=True)
    land_type = models.CharField(max_length=20, choices=LAND_TYPES, null=True, blank=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, null=True,)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True,)

    # Location and Geography
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    # Dimensions and Details
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # in acres
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    floors = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)

    # Financial Information
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Land-specific fields
    zoning = models.CharField(max_length=100, null=True, blank=True)
    soil_type = models.CharField(max_length=100, null=True, blank=True)
    topography = models.CharField(max_length=50, null=True, blank=True)
    utilities_available = models.JSONField(default=list)
    buildable = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    favorites = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    premium_listing = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def days_on_market(self):
        from django.utils import timezone
        return (timezone.now().date() - self.created_at.date()).days

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')  # Or use URLField if hosting elsewhere
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            try:
                img_path = self.image.path
                with Image.open(img_path) as img:
                    if img.height > 384 or img.width > 512:
                        img.thumbnail((512, 384), Image.Resampling.LANCZOS)
                        img.save(img_path)
            except Exception as e:
                print("Error resizing image:", e)

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, related_name='amenities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)  # Icon name for frontend

class VirtualTour(models.Model):
    TOUR_TECHNOLOGY = [
        ('3d', '3D Tour'),
        ('360', '360° Tour'),
        ('video', 'Video Tour'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='virtual_tours')
    tour_url = models.URLField()
    technology = models.CharField(max_length=10, choices=TOUR_TECHNOLOGY)
    upload_date = models.DateTimeField(auto_now_add=True)

class PropertyFeature(models.Model):
    FEATURE_CATEGORIES = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('community', 'Community'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=FEATURE_CATEGORIES)
    icon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class PropertyFeatureJunction(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    feature = models.ForeignKey(PropertyFeature, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('property', 'feature')

    def __str__(self):
        return self.description