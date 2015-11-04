from django.db import models
from locations.models import Location


class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=100)
    is_vegan = models.BooleanField(blank=False, default=False)
    is_gluten_free = models.BooleanField(blank=False, default=False)
    contains_nuts = models.BooleanField(blank=False, default=False)
    MEAL_TIME_CHOICES = (
        ('Br', 'Breakfast'),
        ('Lu', 'Lunch'),
        ('Di', 'Dinner'),
        ('LN', 'Late Night'),
        ('LD', 'Lunch & Dinner'),
        ('TM', 'Today\'s Menu'),
        ('No', 'None!')
    )
    date = models.DateField()
    meal = models.CharField(max_length=2,
                            choices=MEAL_TIME_CHOICES,
                            default="Br")
    location = models.ForeignKey(Location)
    price = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
