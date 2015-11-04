from datetime import time, datetime

from locations.models import OpeningHours

def current_meal_type():
    now = datetime.now().time()
    weekday = datetime.now().isoweekday()
    hours = OpeningHours.objects.filter(weekday=weekday)
    for entry in hours:
        if entry.breakfast_from and entry.breakfast_to and \
            (entry.breakfast_from < now < entry.breakfast_to):
            return "Br"
        elif entry.lunch_from and entry.lunch_to and \
            (entry.lunch_from < now < entry.lunch_to):
            return "Lu"
        elif entry.dinner_from and entry.dinner_to and \
            (entry.dinner_from < now < entry.dinner_to):
            return "Di"
        elif entry.late_night_from and entry.late_night_to and \
            (entry.late_night_from < now < entry.late_night_to):
            return "LN"
    return "No"

def next_meal_type():
    now = datetime.now().time()
    weekday = datetime.now().isoweekday()
    if weekday in [1, 2, 3, 4]:  # Monday - Thursday
        if now < time(7, 15):
            return "Br"
        elif now < time(11):
            return "Lu"
        elif now < time(16, 15):
            return "Di"
        elif now < time(19, 15):
            return "LN"
        else:
            return "Br"
    if weekday == 5:  # Friday (breakfast, but no late night)
        if now < time(7, 15):
            return "Br"
        elif now < time(11):
            return "Lu"
        elif now < time(16, 15):
            return "Di"
        else:
            return "Br"
    if weekday == 6:  # Saturday (only breakfast at south from 7)
        if now < time(7):
            return "Br"
        elif now < time(10, 30):
            return "Lu"
        elif now < time(16, 30):
            return "Di"
        else:
            return "Br"
    if weekday == 7:  # Sunday (breakfast at south from 8, but also LN)
        if now < time(8):
            return "Br"
        elif now < time(10, 30):
            return "Lu"
        elif now < time(16, 30):
            return "Di"
        elif now < time(19, 15):
            return "LN"
        else:
            return "Br"
