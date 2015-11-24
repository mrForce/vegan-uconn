from datetime import time, datetime
import math
from decimal import *

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


def current_or_next_meal():
    return current_meal_type() if (current_meal_type() is not "No") \
        else next_meal_type()


def full_meal_name(meal):
    return {
        "Br": "Breakfast",
        "Lu": "Lunch",
        "Di": "Dinner",
        "LN": "Late Night Grill",
        "LD": "Lunch & Dinner",
        "TM": "Today's Menu",
    }.get(meal, "No current meal")


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = Decimal(math.pi)/Decimal(180.0)

    # phi = 90 - latitude
    phi1 = (Decimal(90.0) - lat1)*degrees_to_radians
    phi2 = (Decimal(90.0) - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #  sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc * 3960  # Miles
