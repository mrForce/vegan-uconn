import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from datetime import datetime

from locations.models import Location

class Command(BaseCommand):
    help = "Updates the dining locations (but doesn't add or change existing lat/long info."

    def handle(self, *args, **kwargs):
        nutrition_overview_url = "http://dining.uconn.edu/nutrition/"
        result = requests.get(nutrition_overview_url)
        soup = BeautifulSoup(result.content, "lxml")
        rows = soup.findAll("tr")
        dining_units = rows[1].findAll("a")             # 2nd tr (row) in page
        restaurants_and_cafes = rows[3].findAll("a")    # 4th tr (row) in page
        for d in dining_units:
            Location.objects.get_or_create(name=d.text.strip(), is_dining_hall=True, url=d["href"])
        for r in restaurants_and_cafes:
            Location.objects.get_or_create(name=r.text.strip(), is_dining_hall=False, url=r["href"])
        self.stdout.write(datetime.now().isoformat() +
                          " Successfully updated locations.")
