from django.db import models
# Create your models here.

class Currency(models.Model):
    CURRENCY = [
        ('XAF', 'XAF'),
        ('USD', 'USD'),
        ('Naira', 'Naira'),
        ('Euros', 'Euros'),
    ]
    name = models.CharField(max_length=15, choices=CURRENCY, unique=True)  # Add this field

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, max_length=10, default=0, null=True)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    tax_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    population = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    average_property_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Neighborhood(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    average_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    crime_rate = models.CharField(max_length=50, blank=True, null=True)
    school_quality = models.CharField(max_length=50, blank=True, null=True)
    amenities_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default='Yaounde')
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Cameroon')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.street
