from datetime import time, datetime, timedelta
from decimal import *

from django.shortcuts import render_to_response
from django.utils import timezone

from locations.models import Location
from food.models import Food
import core.utils

def index(request):
    # TODO: make sure entrees are always first
    # create a list of lists of lists in the format
    # [                                                 locations_list
    #   [
    #     ["Place name 1", rank]                        categories_list
    #       ["Entrees", entree_1, ..., entree_n],       foods_list
    #       ["Sides", side_1, ..., side_n]              foods_list
    #     ],
    #   [
    #     ["Place name 2", rank]                        categories_list
    #       ["Entrees", entree_1, ..., entree_n],       foods_list
    #       ["Desserts", dessert_1, ..., dessert_n]     foods_list
    #     ],
    #   etc.
    # ]
    locations_list = []
    categories = []

    # Get GET requests
    hide_nuts = True if request.GET.get('hide_nuts', '') else False
    hide_gluten = True if request.GET.get('hide_gluten', '') else False
    location_type = request.GET.get('location_type', '')
    pos = request.GET.get('pos', '')
    if pos and not request.GET.get('sort', '') == "num":
        sort = "distance"
    else:
        sort = "num"
    if sort == "distance":
        location = request.GET.get('pos', '').split("and")
        latitude = Decimal(location[0])
        longitude = Decimal(location[1])
    meal = request.GET.get('meal', '')
    if not meal:
        meal = core.utils.current_or_next_meal()  # If no meal is specified

    # If we passed today's meal, show tomorrow's
    weekday = datetime.now().isoweekday()
    date = datetime.today()
    tomorrow = date + timedelta(days=1)
    now = datetime.now().time()
    if weekday == [1, 2, 3, 4]:  # Monday - Thursday
        if (meal == "Br" and now > time(10, 45)) or \
           (meal == "Lu" and now > time(14, 15)) or \
           (meal == "Di" and now > time(19, 15)) or \
           (meal == "LN" and now > time(22, 00)):
            date = tomorrow
    elif weekday == 5:  # Friday
        if (meal == "Br" and now > time(10, 45)) or \
           (meal == "Lu" and now > time(14, 15)) or \
           (meal == "Di" and now > time(19, 15)) or \
           (meal == "LN" and now > time(19, 15)):  # No late night
            date = tomorrow
    elif weekday == 6:  # Saturday
        if (meal == "Br" and now > time(9, 30)) or \
           (meal == "Lu" and now > time(16, 15)) or \
           (meal == "Di" and now > time(19, 15)) or \
           (meal == "LN" and now > time(19, 15)):  # No late night
            date = tomorrow
    else:  # Sunday
        if (meal == "Br" and now > time(9, 30)) or \
           (meal == "Lu" and now > time(16, 15)) or \
           (meal == "Di" and now > time(19, 15)) or \
           (meal == "LN" and now > time(22, 00)):
            date = tomorrow

    # Get the Location query
    if location_type == "cafes_restaurants":
        ls = Location.objects.filter(is_dining_hall=False)
        meal = "TM"
    else:
        ls = Location.objects.filter(is_dining_hall=True)
        location_type = "dining_halls"

    # Get foods from relevant Locations
    for l in ls:
        foods = Food.objects.filter(date=date)\
                            .filter(is_vegan=True)\
                            .filter(location=l)
        if location_type == "dining_halls":
            foods = foods.filter(meal=meal)
            # if the user requested cafes and restaurants, we don't filter
            # by meal - because they don't have one, they sell the same
            # things all day
        if hide_nuts:
            foods = foods.filter(contains_nuts=False)
        if hide_gluten:
            foods = foods.filter(is_gluten_free=True)
        if foods.count() > 0:
            categories = foods.values_list("category", flat=True).distinct()
            # 1st entry here is a list of the location name and, depending
            # on sorting, either its rating (number of vegan options) or its
            # distance from the user
            categories_list = [[l.name, 0]]

            for category in categories:
                # 1st entry here is the category name
                foods_list = [category] + \
                             [f for f in foods.filter(category=category)]
                categories_list.append(foods_list)
                if sort == "num":
                    categories_list[0][1] += (len(foods_list) - 1)

            if sort == "distance":
                categories_list[0][1] = \
                    round(core.utils.distance_on_unit_sphere(
                        l.latitude, l.longitude, latitude, longitude
                    ), 2)
            locations_list.append(categories_list)

    locations_list.sort(key=lambda x: x[0][1])
    if sort == "num":
        locations_list.reverse()
        # Freshens tends to have a lot of smoothie options, which gets it
        # listed first. However, since they're smoothies and not actual dishes,
        # it makes more sense to list it last - this is a better UX.
        for l in locations_list:
            if l[0][0] == 'Freshens':
                locations_list.remove(l)
                locations_list.append(l)
                break

    return render_to_response("index.html",
                              {"locations_list": locations_list,
                               "meal_name": core.utils.full_meal_name(meal),
                               "date": date.date(),
                               "hide_nuts": hide_nuts,
                               "hide_gluten": hide_gluten,
                               "meal": meal,
                               "location_type": location_type,
                               "sort": sort
                               })
