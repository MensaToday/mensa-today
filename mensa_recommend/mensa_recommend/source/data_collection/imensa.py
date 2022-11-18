from datetime import datetime, date
from typing import List, Tuple

from bs4 import BeautifulSoup

from mensa.models import Category, Allergy, Additive, Dish, DishCategory, DishAllergy, DishAdditive, DishPlan, Mensa, \
    ExtDishRating
from .utils import NoAuthCollector
from . import utils

static_categories = ["Vegan", "Vegetarian", "Pork", "Beef", "Poultry", "Alcohol", "Fish"]
static_additives = ["Dyed", "Preservatives", "Antioxidants", "Flavor enhancers", "Sulphurated", "Blackened", "Waxed",
                    "Phosphate", "Sweeteners", "Phenylalanine source"]
static_allergies = ["Gluten", "Spelt", "Barley", "Oats", "Kamut", "Rye", "Wheat", "Crustaceans", "Egg", "Fish",
                    "Peanuts", "Soy", "Milk", "Nuts", "Almonds", "Hazelnuts", "Walnuts", "Cashews", "Pecans",
                    "Brazil nuts", "Pistachios", "Macadamias", "Celery", "Mustard", "Sesame", "Lupines", "Molluscs",
                    "Sulfur dioxide"]


def _get_dish(name: str) -> Dish:
    try:
        return Dish.objects.get(name=name)
    except Dish.DoesNotExist:
        d = Dish(name=name)
        d.save()
        return d


class IMensaCollector(NoAuthCollector):
    def __init__(self):
        self.url = "https://www.imensa.de/{city}/{mensa}/{day}.html"
        self.cities = {
            "muenster": [
                "mensa-da-vinci", "bistro-denkpause",  # "bistro-friesenring",  # does not exist anymore?
                "bistro-katholische-hochschule",
                "bistro-durchblick", "bistro-frieden", "bistro-kabu", "bistro-oeconomicum", "hier-und-jetzt",
                "mensa-am-aasee",
                "mensa-am-ring", "mensa-bispinghof"
            ]
        }
        self.days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

    def prepare(self) -> None:
        for c in static_categories:
            utils.save_integrity_free(Category(name=c))
        for a in static_additives:
            utils.save_integrity_free(Additive(name=a))
        for a in static_allergies:
            utils.save_integrity_free(Allergy(name=a))

        utils.save_integrity_free(
            Mensa(name_id="bistro-denkpause", name="Bistro Denkpause", street="Corrensstr.", houseNumber="25", zipCode=48149, city="Münster",
                  startTime="11:30", endTime="14:15"))
        utils.save_integrity_free(
            Mensa(name_id="mensa-da-vinci", name="Mensa Da Vinci", street="Leonardo-Campus", houseNumber="8", zipCode=48149, city="Münster",
                  startTime="11:30", endTime="14:00"))
        utils.save_integrity_free(
            Mensa(name_id="bistro-katholische-hochschule", name="Bistro Katholische Hochschule", street="Piusallee", houseNumber="89", zipCode=48147,
                  city="Münster", startTime="11:30", endTime="13:45"))
        utils.save_integrity_free(
            Mensa(name_id="bistro-durchblick", name="Bistro Durchblick", street="Fliednerstr.", houseNumber="21", zipCode=48149, city="Münster",
                  startTime="11:30", endTime="13:30"))
        utils.save_integrity_free(
            Mensa(name_id="bistro-frieden", name="Bistro Frieden", street="Scharnhorststr.", houseNumber="100", zipCode=48151, city="Münster",
                  startTime="08:00", endTime="13:45"))
        utils.save_integrity_free(
            Mensa(name_id="bistro-kabu", name="Bistro KaBu", street="Domplatz", houseNumber="21", zipCode=48143, city="Münster",
                  startTime="11:00", endTime="14:00"))
        utils.save_integrity_free(
            Mensa(name_id="bistro-oeconomicum", name="Bistro Oeconomicum", street="Universitätsstr.", houseNumber="14", zipCode=48143, city="Münster",
                  startTime="07:30", endTime="18:00"))
        utils.save_integrity_free(
            Mensa(name_id="hier-und-jetzt", name="Hier und Jetzt", street="Bismarckallee", houseNumber="11", zipCode=48151, city="Münster",
                  startTime="11:30", endTime="14:30"))  # ALSO 17:00-21:00 ._. ; we'll ignore that for now
        utils.save_integrity_free(
            Mensa(name_id="mensa-am-aasee", name="Mensa am Aasee", street="Bismarckallee", houseNumber="11", zipCode=48151, city="Münster",
                  startTime="11:45", endTime="14:30"))
        utils.save_integrity_free(
            Mensa(name_id="mensa-am-ring", name="Mensa am Ring", street="Domagkstr.", houseNumber="61", zipCode=48149, city="Münster",
                  startTime="11:30", endTime="14:00"))
        utils.save_integrity_free(
            Mensa(name_id="mensa-bispinghof", name="Mensa Bispinghof", street="Bispinghof", houseNumber="9-14", zipCode=48149, city="Münster",
                  startTime="11:00", endTime="14:30"))

    def __scrape(self, document: BeautifulSoup, **options) -> None:
        mensa: Mensa = options["mensa"]
        dish_plan_date = options["date"]

        main_meal = True
        for div in document.find_all(class_="aw-meal-category"):
            no_meal = False
            for meal in div.find_all(class_="aw-meal row no-margin-xs"):
                no_meal = meal.find(title="Preis für Studierende") is None
                if no_meal:
                    break

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

                ratings_count_tag = meal.find(class_="aw-meal-histogram-count")
                ratings_count = 0
                if ratings_count_tag:
                    ratings_count = utils.to_int(ratings_count_tag.text)

                ratings_avg_tag = meal.find(class_="aw-meal-histogram-average")
                ratings_avg = 0
                if ratings_avg_tag:
                    ratings_avg = utils.to_float(ratings_avg_tag.text)

                d = _get_dish(name)
                for c in categories:
                    category = Category.objects.get(name=c)
                    utils.save_integrity_free(DishCategory(dish=d, category=category))

                for a in allergies:
                    allergy = Allergy.objects.get(name=a)
                    utils.save_integrity_free(DishAllergy(dish=d, allergy=allergy))

                for a in additives:
                    additive = Additive.objects.get(name=a)
                    utils.save_integrity_free(DishAdditive(dish=d, additive=additive))

                utils.save_integrity_free(
                    DishPlan(dish=d, mensa=mensa, date=dish_plan_date, priceStudent=price_for_students,
                             priceEmployee=price_for_non_students))

                utils.save_integrity_free(
                    ExtDishRating(mensa=mensa, dish=d, date=dish_plan_date, rating_avg=ratings_avg,
                                  rating_count=ratings_count))

            if not no_meal:
                main_meal = False
            break  # Do not save side meals

    def __build_urls(self) -> List[Tuple[str, dict]]:
        urls = []

        for city in self.cities.keys():
            m = self.cities[city]
            for mensa in m:
                mensa_db = Mensa.objects.get(name_id=mensa)

                for day in self.days:
                    urls.append((self.url.format(city=city, mensa=mensa, day=day),
                                 {"mensa": mensa_db, "date": self.__day_to_date(day), "day": day}))
        return urls

    def __day_to_date(self, day: str) -> date:
        weekday = self.days.index(day)
        now = datetime.now().date()
        diff = weekday - now.weekday()
        return date(now.year, now.month, now.day + diff)
