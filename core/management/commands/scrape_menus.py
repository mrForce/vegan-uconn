import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from datetime import datetime

from locations.models import Location
from food.models import Food


class Command(BaseCommand):
    help = "Scrapes the UConn dining website for menu information."

    @staticmethod
    def convert_meal_format(self, meal):
        return {
            "Breakfast": "Br",
            "Lunch": "Lu",
            "Dinner": "Di",
            "Lunch & Dinner": "LD",
            "Today's Menu": "TM",
            "TODAY'S MENU": "TM"
        }.get(meal, "No")

    @staticmethod
    def update_tables(self, soup, location):
        date = datetime.today()
        # first, find the meals of the day
        meals = soup.find_all("div", class_="shortmenumeals")
        meals = [m.find_parent("table").find_parent("table") for m in meals]
        for m in meals:
            # a meal is a list of dishes (e.g. for breakfast, lunch, etc)
            meal_name = m.find_all("div", class_="shortmenumeals")[0].string
            meal_name = self.convert_meal_format(self, meal_name)
            # the menu is the 2nd tr in the meal table
            menu = m.find_all("tr")[0].find_next_sibling("tr").find("table")\
                .find_all("tr", recursive=False)
            category = ""
            for dish in menu:
                if dish.find_all("div", class_="shortmenucats"):
                    # not a dish, it's the category of the following dishes
                    category = dish.find_all("div", class_="shortmenucats")[0]\
                        .string.strip("- ").title()
                    # Late night is stored under Dinner,
                    # making things a bit more difficult!
                    if (category == "Late Night Grill") or \
                       (category == "Late Night"):
                        meal_name = "LN"
                elif dish.find_all("div", class_="shortmenuproddesc"):
                    # this tr is a description of the previous dish
                    # use join() because some descriptions are lines with
                    # <br>s between them.
                    description = " ".join(dish.find_all("div",
                                           class_="shortmenuproddesc")[0]
                                           .find_all(text=True))
                    # don't save descriptions about nutrition info
                    if ("nutrition" not in description and
                            "portion" not in description):
                        latest = Food.objects.latest("id")
                        latest.description = description
                        if "vegan" in description:
                            latest.is_vegan = True
                        latest.save()
                else:
                    dish_name = dish.find_all("div",
                                              class_="shortmenurecipes")[0]\
                                              .string
                    # it's a dish, so check if it's vegan & check for allergens
                    is_vegan = False
                    is_gluten_free = False
                    contains_nuts = False
                    try:
                        price = dish.find("div",
                                          class_="shortmenuprices")\
                                          .find("span").string.strip("$")
                    except:
                        price = ""
                    if dish.find_all("img", {"src": "LegendImages/vegan.gif"}):
                        is_vegan = True
                    if dish.find_all("img",
                                     {"src": "LegendImages/glutenfree.gif"}):
                        is_gluten_free = True
                    if dish.find_all("img", {"src": "LegendImages/nuts.gif"}):
                        contains_nuts = True
                    Food.objects.create(name=dish_name,
                                        category=category,
                                        is_vegan=is_vegan,
                                        is_gluten_free=is_gluten_free,
                                        contains_nuts=contains_nuts,
                                        date=date,
                                        meal=meal_name,
                                        location=location,
                                        price=price)

    def handle(self, *args, **kwargs):
        for location in Location.objects.all():
            result = requests.get(location.url)
            soup = BeautifulSoup(result.content, "lxml")
            self.update_tables(self, soup, location)
            self.stdout.write("Updated menu for " + location.name + ".")

        self.stdout.write(datetime.now().isoformat() +
                          " Successfully collected menus.")
