from datetime import datetime

from django.shortcuts import render_to_response

from locations.models import Location
from food.models import Food
from core.utils import current_meal_type, next_meal_type

def index(request):
    # TODO: add ability to show non-dining-hall places (cafes etc)
    # TODO: add ability to sort by distance
    # create a list of lists of lists in the format
    # [
    #   ["Place name 1",
    #      ["Entrees", entree_1, ..., entree_n],
    #       ["Sides", side_1, ..., side_n]
    #   ],
    #   ["Place name 2",
    #       ["Entrees", entree_1, ..., entree_n],
    #       ["Desserts", dessert_1, ..., dessert_n]
    #   ],
    #   etc.
    # ]
    current_meal = current_meal_type()
    next_meal = next_meal_type()

    locations_dict = {}
    for l in Location.objects.filter(is_dining_hall=True):
        foods = Food.objects.filter(date=datetime.today())\
                            .filter(meal=current_meal)\
                            .filter(is_vegan=True)\
                            .filter(location=l)
        if foods.count() > 0:
            categories = foods.values_list("category", flat=True).distinct()
            categories_dict = {}

            for category in categories:
                foods_list = foods.filter(category=category)
                categories_dict[category] = foods_list
                locations_dict[l.name] = categories_dict

    return render_to_response("index.html", {"locations_dict": locations_dict,
                                             "current_meal": current_meal,
                                             "next_meal": next_meal,
                                             "now": datetime.now(),
                                             "categories": categories})
