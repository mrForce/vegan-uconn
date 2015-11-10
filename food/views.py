from datetime import time, datetime, timedelta

from django.shortcuts import render_to_response
from django.utils import timezone

from locations.models import Location
from food.models import Food
from core.utils import current_meal_type, next_meal_type, current_or_next_meal, full_meal_name


def index(request, meal=current_or_next_meal()):
    # TODO: add ability to show non-dining-hall places (cafes etc)
    # TODO: add ability to sort by distance
    # create a list of lists of lists in the format
    # [                                                 locations_list
    #   ["Place name 1",                                categories_list
    #      ["Entrees", entree_1, ..., entree_n],        foods_list
    #      ["Sides", side_1, ..., side_n]               foods_list
    #   ],
    #   ["Place name 2",                                categories_list
    #       ["Entrees", entree_1, ..., entree_n],       foods_list
    #       ["Desserts", dessert_1, ..., dessert_n]     foods_list
    #   ],
    #   etc.
    # ]

    locations_list = []
    categories = []
    weekday = datetime.now().isoweekday()
    date = datetime.today()
    tomorrow = date + timedelta(days=1)
    now = datetime.now().time()
    # If we passed today's meal, show tomorrow's
    if weekday in [1, 2, 3, 4]:  # Monday - Thursday
        if (meal is "Br" and now > time(10, 45)) or \
           (meal is "Lu" and now > time(14, 15)) or \
           (meal is "Di" and now > time(19, 15)) or \
           (meal is "LN" and now > time(22, 00)):
            date = tomorrow
    elif weekday is 5:  # Friday
        if (meal is "Br" and now > time(10, 45)) or \
           (meal is "Lu" and now > time(14, 15)) or \
           (meal is "Di" and now > time(19, 15)) or \
           (meal is "LN" and now > time(19, 15)):  # No late night
            date = tomorrow
    elif weekday is 6:  # Saturday
        if (meal is "Br" and now > time(9, 30)) or \
           (meal is "Lu" and now > time(16, 15)) or \
           (meal is "Di" and now > time(19, 15)) or \
           (meal is "LN" and now > time(19, 15)):  # No late night
            date = tomorrow
    else:  # Sunday
        if (meal is "Br" and now > time(9, 30)) or \
           (meal is "Lu" and now > time(16, 15)) or \
           (meal is "Di" and now > time(19, 15)) or \
           (meal is "LN" and now > time(22, 00)):
            date = tomorrow

    for l in Location.objects.filter(is_dining_hall=True):
        foods = Food.objects.filter(date=date)\
                            .filter(meal=meal)\
                            .filter(is_vegan=True)\
                            .filter(location=l)
        if foods.count() > 0:
            categories = foods.values_list("category", flat=True).distinct()
            # 1st entry here is a list of the location name and its rating
            # (how many vegan options there are where entrees count for 2)
            categories_list = [[l.name, 0]]

            for category in categories:
                # 1st entry here is the category name
                foods_list = [category] + \
                             [f for f in foods.filter(category=category)]
                categories_list.append(foods_list)
                if "entree" in category.lower():  # entrees worth 2x as much!
                    categories_list[0][1] += 2*((len(foods_list) - 1))
                else:
                    categories_list[0][1] += (len(foods_list) - 1)
            locations_list.append(categories_list)

    locations_list.sort(key=lambda x: x[0][1])
    locations_list.reverse()

    return render_to_response("index.html", {"locations_list": locations_list,
                                             "meal": meal,
                                             "meal_name": full_meal_name(meal),
                                             "date": date,
                                             "categories": categories})
