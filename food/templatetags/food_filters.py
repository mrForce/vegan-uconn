from django import template
from django.template.defaultfilters import stringfilter
import emoji

register = template.Library()


@register.filter
@stringfilter
def add_emoji(value):
    # food name, emoji name
    emojis = {
        "pizza": "pizza",
        "skewer": "oden",
        "donut": "doughnut",
        "doughnut": "doughnut",
        "apple": "apple",
        "cherry": "cherries",
        "peach": "peach",
        "corn": "corn",
        "pineapple": "pineapple",
        "pine apple": "pineapple",
        "burger": "hamburger",
        "spaghetti": "spaghetti",
        "pasta": "spaghetti",
        "rotini": "spaghetti",
        "rice": "rice",
        "custard": "custard",
        " cake": "cake",  # the prefixed space is to avoid matching "pancake"
        "grape": "grapes",
        "melon": "melon",
        "sweet potato": "sweet_potato",
        "coffee": "coffee",
        "fries": "fries",
        "curry": "curry",
        "ramen": "ramen",
        "noodles": "ramen",
        "icecream": "ice_cream",
        "ice cream": "ice_cream",
        "watermelon": "watermelon",
        "water melon": "watermelon",
        "banana": "banana",
        "eggplant": "eggplant",
        "aubergine": "eggplant",
        "stew": "stew",
        "bread": "bread",
        "cookie": "cookie",
        "strawberry": "strawberry",
        "pear": "pear",
        "tomato": "tomato",
        "taco": "taco",
        "burrito": "burrito",
        "chili": "hot_pepper",
        "chilli": "hot_pepper",
        "soup": "stew"
    }

    for k in emojis.keys():
        if k in value.lower():
            value = emoji.emojize(value + " :" + emojis[k] + ":",
                                  use_aliases=True)
            break  # only take the first emoji that fits
    return value
