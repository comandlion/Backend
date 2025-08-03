from django.db import models
from django.contrib.auth.models import User
from properties.models import Property

# Create your models here.

class Offer(models.Model):
    OFFER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('countered', 'Countered'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    offer_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='pending')
    terms = models.TextField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)


class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='brokered_transactions')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='pending')
    contract = models.URLField(blank=True, null=True)