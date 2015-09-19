from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    is_dining_hall = models.BooleanField(blank=False, default=False)
    latitude = models.DecimalField(decimal_places=4)    # 4 decimal places = ~10m accuracy at the equator (worst case)
    longitude = models.DecimalField(decimal_places=4)