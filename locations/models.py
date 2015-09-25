from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    is_dining_hall = models.BooleanField(blank=False, default=False)
    # 4 decimal places = ~10m accuracy at the equator (worst case)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    url = models.URLField(max_length=300)

# class OpeningHours(models.Model):
#     WEEKDAYS = [
#         (1, _("Monday")),
#         (2, _("Tuesday")),
#         (3, _("Wednesday")),
#         (4, _("Thursday")),
#         (5, _("Friday")),
#         (6, _("Saturday")),
#         (7, _("Sunday")),
#     ]
#     location = models.ForeignKey(Location)
#     date = models.DateField(blank=True)                 # only fill this for special days, e.g. holidays
#     weekday = models.IntegerField(choices=WEEKDAYS)     # used on normal days
#     breakfast_from  = models.TimeField()
#     breakfast_to    = models.TimeField()
#     lunch_from      = models.TimeField()
#     lunch_to        = models.TimeField()
#     dinner_from     = models.TimeField()
#     dinner_to       = models.TimeField()
#     late_night_from = models.TimeField()
#     late_night_to   = models.TimeField()
