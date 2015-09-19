from django.db import models
from locations.models import Location

class Food(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    is_vegan = models.BooleanField(blank=False, default=False)
    is_gluten_free = models.BooleanField(blank=False, default=False)
    contains_nuts = models.BooleanField(blank=False, default=False)
    MEAL_TIME_CHOICES = (
        ('Br', 'Breakfast'),
        ('Lu', 'Lunch'),
        ('Di', 'Dinner'),
        ('LN', 'Late Night'),
    )
    date = models.DateField()
    meal = models.CharField(max_length=2, choices=MEAL_TIME_CHOICES, default="Br")
    location = models.ForeignKey(Location)
