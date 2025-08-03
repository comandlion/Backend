from django.db import models
from django.contrib.auth.models import User
from properties.models import Property
from listings.models import Listing
from properties.models import Property

# Create your models here.

class SavedSearch(models.Model):
    NOTIFICATION_FREQUENCIES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('none', 'None'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    search_name = models.CharField(max_length=100)
    search_parameters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField(blank=True, null=True)
    notification_frequency = models.CharField(
        max_length=10,
        choices=NOTIFICATION_FREQUENCIES,
        default='none'
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "property"], name="unique_property_favorite"),
            models.UniqueConstraint(fields=["user", "listing"], name="unique_listing_favorite")
        ]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='liked_by', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='liked_by', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "property"], name="unique_property_like"),
            models.UniqueConstraint(fields=["user", "listing"], name="unique_listing_like")
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='commented_by', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='commented_by', null=True, blank=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class PropertyView(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_views")
    view_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)