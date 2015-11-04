import requests

from django.core.management.base import BaseCommand
from datetime import time, datetime

from locations.models import Location, OpeningHours


class Command(BaseCommand):
    help = "."

    def handle(self, *args, **kwargs):
        dininghalls = Location.objects.filter(is_dining_hall=True)
        for d in dininghalls:
            for i in range(1, 6):  # 1 to 5, monday to friday
                OpeningHours.objects.create(location=d,
                                            weekday=i,
                                            breakfast_from=time(7),
                                            breakfast_to=time(10, 45),
                                            lunch_from=time(11),
                                            lunch_to=time(14, 15),
                                            dinner_from=time(16, 15),
                                            dinner_to=time(19, 15))
            for i in range(6, 8):
                OpeningHours.objects.create(location=d,
                                            weekday=i,
                                            lunch_from=time(10, 30),
                                            lunch_to=time(14, 00),
                                            dinner_from=time(16, 30),
                                            dinner_to=time(19, 15))
            # late night
            if (d.name == "Whitney Dining Hall") or \
               (d.name == "McMahon Dining Hall") or \
               (d.name == "Northwest Marketplace"):
                for i in [1, 2, 3, 4, 7]:  # not fri or sat
                    OpeningHours.objects.update_or_create(location=d,
                                                          weekday=i,
                                                          defaults={
                                                            "late_night_from": time(19, 15),
                                                            "late_night_to": time(22)})
            if (d.name == "South Campus Marketplace"):
                OpeningHours.objects.update_or_create(location=d,
                                                      weekday=6,
                                                      defaults={
                                                        "breakfast_from": time(7),
                                                        "breakfast_to": time(9, 30)})
                OpeningHours.objects.update_or_create(location=d,
                                                      weekday=7,
                                                      defaults={
                                                        "breakfast_from": time(7),
                                                        "breakfast_to": time(9, 30)})

        self.stdout.write(datetime.now().isoformat() +
                          " Successfully updated opening hours.")
