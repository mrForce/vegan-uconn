from datetime import datetime

from django.shortcuts import render_to_response

from locations.models import Location
from food.models import Food
from core.utils import current_meal_type, next_meal_type

def index(request):
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
    current_meal = current_meal_type()
    next_meal = next_meal_type()

    locations_list = []
    for l in Location.objects.filter(is_dining_hall=True):
        foods = Food.objects.filter(date=datetime.today())\
                            .filter(meal=current_meal)\
                            .filter(is_vegan=True)\
                            .filter(location=l)
        if foods.count() > 0:
            categories = foods.values_list("category", flat=True).distinct()
            categories_list = [l.name]  # 1st entry here is the location name

            for category in categories:
                # 1st entry here is the category name
                foods_list = [category] + [f for f in foods.filter(category=category)]
                categories_list.append(foods_list)
            locations_list.append(categories_list)

    return render_to_response("index.html", {"locations_list": locations_list,
                                             "current_meal": current_meal,
                                             "next_meal": next_meal,
                                             "now": datetime.now(),
                                             "categories": categories})
