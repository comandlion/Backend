from django.db import models

from properties.models import Property
from django.contrib.auth.models import User

# Create your models here.

class Listing(models.Model):
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('auction', 'Auction'),
    ]

    LISTING_STATUS = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('rented', 'Rented'),
    ]
    title = models.CharField(max_length=255, default='Listing')
    content = models.TextField(null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='listings')
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_listed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    expiration_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=LISTING_STATUS, default='active')

    def __str__(self):
        return self.title