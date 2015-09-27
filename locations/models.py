from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    is_dining_hall = models.BooleanField(blank=False, default=False)
    # 4 decimal places = ~10m accuracy at the equator (worst case)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    url = models.URLField(max_length=300)

class OpeningHours(models.Model):
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday")
    ]
    location = models.ForeignKey(Location)
    date = models.DateField(blank=True, null=True)      # only fill this for special days, e.g. holidays
    weekday = models.IntegerField(choices=WEEKDAYS)     # used on normal days
    breakfast_from  = models.TimeField(blank=True, null=True)
    breakfast_to    = models.TimeField(blank=True, null=True)
    lunch_from      = models.TimeField(blank=True, null=True)
    lunch_to        = models.TimeField(blank=True, null=True)
    dinner_from     = models.TimeField(blank=True, null=True)
    dinner_to       = models.TimeField(blank=True, null=True)
    late_night_from = models.TimeField(blank=True, null=True)
    late_night_to   = models.TimeField(blank=True, null=True)
