from typing import List

from bs4 import BeautifulSoup

from mensa.models import Category, Allergy, Additive
from .utils import NoAuthCollector
from . import utils

static_categories = ["Vegan", "Vegetarian", "Pork", "Beef", "Poultry"]
static_additives = ["Dyed", "Preservatives", "Antioxidants", "Flavor enhancers", "Sulphurated", "Blackened", "Waxed",
                    "Phosphate", "Sweeteners", "Phenylalanine source"]
static_allergies = ["Gluten", "Spelt", "Barley", "Oats", "Kamut", "Rye", "Wheat", "Crustaceans", "Egg", "Fish",
                    "Peanuts", "Soy", "Milk", "Nuts", "Almonds", "Hazelnuts", "Walnuts", "Cashews", "Pecans",
                    "Brazil nuts", "Pistachios", "Macadamias", "Celery", "Mustard", "Sesame", "Lupines", "Molluscs",
                    "Sulfur dioxide"]


def __insert_static__():
    for c in static_categories:
        Category(name=c).save()
    for a in static_additives:
        Additive(name=a).save()
    for a in static_allergies:
        Allergy(name=a).save()


class IMensaCollector(NoAuthCollector):
    def __init__(self):
        self.url = "https://www.imensa.de/{city}/{mensa}/{day}.html"
        self.cities = {
            "muenster": [
                "mensa-da-vinci", "bistro-denkpause", "bistro-friesenring",
                "bistro-katholische-hochschule",
                "bistro-durchblick", "bistro-frieden", "bistro-kabu", "bistro-oeconomicum", "hier-und-jetzt",
                "mensa-am-aasee",
                "mensa-am-ring", "mensa-bispinghof"
            ]
        }
        self.days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

    def prepare(self) -> None:
        __insert_static__()

    def scrape(self, document: BeautifulSoup) -> None:
        main_meal = True
        for div in document.find_all(class_="aw-meal-category"):
            for meal in div.find_all(class_="aw-meal row no-margin-xs"):
                name = meal.find(class_="aw-meal-description").text
                price_for_students = utils.to_float(meal.find(title="Preis für Studierende").text[:-2])
                price_for_non_students = price_for_students * 1.5

                attributes = meal.find(class_="small aw-meal-attributes").span.text.replace("\xa0", "").split(" ")

                att_type = 0
                categories = []
                additives = []
                allergies = []

                for att in attributes[1:]:
                    replacement = utils.translate(att)

                    if att == "ZUSATZ":
                        att_type = 1
                    elif att == "ALLERGEN":
                        att_type = 2
                    elif att_type == 0:
                        categories.append(replacement)
                    elif att_type == 1:
                        additives.append(replacement)
                    elif att_type == 2:
                        allergies.append(replacement)

                last_occurrence = meal.find(title="Zuletzt angeboten")
                if last_occurrence:
                    last_occurrence = last_occurrence.text

                ratings_count_tag = meal.find(class_="aw-meal-histogram-count")
                ratings_count = 0
                if ratings_count_tag:
                    ratings_count = utils.to_int(ratings_count_tag.text)

                ratings_avg_tag = meal.find(class_="aw-meal-histogram-average")
                ratings_avg = 0
                if ratings_avg_tag:
                    ratings_avg = utils.to_float(ratings_avg_tag.text)

                # d = Dish(name=name)
                # d.save()
                # todo: save stuff to postgres

            main_meal = False

    def build_urls(self) -> List[str]:
        urls = []

        for city in self.cities.keys():
            m = self.cities[city]
            for mensa in m:
                for day in self.days:
                    urls.append(self.url.format(city=city, mensa=mensa, day=day))
        return urls
