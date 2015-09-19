from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    is_dining_hall = models.BooleanField(blank=False, default=False)
    latitude = models.DecimalField(decimal_places=4)    # 4 decimal places = ~10m accuracy at the equator (worst case)
    longitude = models.DecimalField(decimal_places=4)

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
#     brunch_from     = models.TimeField()
#     brunch_to       = models.TimeField()
#     lunch_from      = models.TimeField()
#     lunch_to        = models.TimeField()
#     dinner_from     = models.TimeField()
#     dinner_to       = models.TimeField()
#     late_night_from = models.TimeField()
#     late_night_to   = models.TimeField()
