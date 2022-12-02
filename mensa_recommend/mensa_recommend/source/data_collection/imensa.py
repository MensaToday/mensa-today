from datetime import datetime, date, timedelta
from typing import List, Tuple

from bs4 import BeautifulSoup, Tag
from django.db import IntegrityError
import requests
import json
import re

from mensa.models import Category, Allergy, Additive, Dish, DishCategory, DishAllergy, DishAdditive, DishPlan, Mensa, \
    ExtDishRating
from . import static_data
from . import utils
from .utils import NoAuthURLCollector


def _get_dish(name: str, main_meal: bool, image_url: str) -> Dish:
    """Load a dish by a given name or create one if absent. Can later be used to implement some sort of name matching in
    order to get rid of duplicated dishes.

    Parameters
    ----------
    name : str
        The name of a dish.
    main_meal : bool
        Whether the dish is a main or side meal.
    image_url : str
        URL of the image for the dish

    Return
    ------
    dish : dish
        The loaded dish.
    """
    try:
        return Dish.objects.get(name=name)
    except Dish.DoesNotExist:
        d = Dish(name=name, main=main_meal, url=image_url)

        # Ignore duplicate errors and just return the dish. Issue only occurs in multithreading context.
        # Using the created instead of the database instance does not change much. The data is the same.
        try:
            d.save()
        except IntegrityError:
            pass

        return d


class IMensaCollector(NoAuthURLCollector):
    def __init__(self):
        self.url = "https://www.imensa.de/{city}/{mensa}/{day}.html"
        self.cities = {
            "muenster": [
                # "bistro-friesenring",  # does not exist anymore?
                "mensa-da-vinci", "bistro-denkpause",
                "bistro-katholische-hochschule",
                "bistro-durchblick", "bistro-frieden", "bistro-kabu", "bistro-oeconomicum", "hier-und-jetzt",
                "mensa-am-aasee",
                "mensa-am-ring", "mensa-bispinghof"
            ]
        }
        self.days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

    def prepare(self) -> None:
        # insert static categories, additives and allergies
        for c in static_data.categories:
            utils.save_without_integrity(Category(name=c))
        for a in static_data.additives:
            utils.save_without_integrity(Additive(name=a))
        for a in static_data.allergies:
            utils.save_without_integrity(Allergy(name=a))

        # insert mensa information
        for m in static_data.canteens:
            utils.save_without_integrity(m)

    def _scrape(self, document: BeautifulSoup, **options) -> None:
        mensa: Mensa = options["mensa"]
        dish_plan_date: date = options["date"]
        day: str = options["day"]

        # find every meal category on the page
        for div in document.find_all(class_="aw-meal-category"):
            category_name: str = div.find(class_="aw-meal-category-name").text
            side_meal = category_name.lower().startswith("beilage")

            # go to every meal in that meal category
            for meal in div.find_all(class_="aw-meal row no-margin-xs"):
                # Some "meals" entries are used to display information of the mensa.
                # Therefore, check if a price is available.
                no_meal = meal.find(title="Preis für Studierende") is None
                if no_meal:
                    break

                # get meal information
                name, price, groups, rating, image_url = self.__scrape_meal(
                    meal, mensa, day)

                # either gets an existing dish or creates one
                d = _get_dish(name, not side_meal, image_url)

                # save additional meal data to database
                self.__save_groups(d, groups)
                self.__save_price(d, mensa, dish_plan_date, price)
                self.__save_rating(d, mensa, dish_plan_date, rating)

    def __save_groups(self, dish: Dish, groups: Tuple[list, list, list]) -> None:
        categories, additives, allergies = groups
        for c in categories:
            category = Category.objects.get(name=c)
            utils.save_without_integrity(
                DishCategory(dish=dish, category=category))
        for a in additives:
            additive = Additive.objects.get(name=a)
            utils.save_without_integrity(
                DishAdditive(dish=dish, additive=additive))
        for a in allergies:
            allergy = Allergy.objects.get(name=a)
            utils.save_without_integrity(
                DishAllergy(dish=dish, allergy=allergy))

    def __save_price(self, dish: Dish, mensa: Mensa, dish_plan_date: date, price: Tuple[float, float]) -> None:
        price_for_students, price_for_non_students = price
        utils.save_without_integrity(
            DishPlan(dish=dish, mensa=mensa, date=dish_plan_date, priceStudent=price_for_students,
                     priceEmployee=price_for_non_students))

    def __save_rating(self, dish: Dish, mensa: Mensa, dish_plan_date: date, rating: Tuple[int, float]) -> None:
        ratings_count, ratings_avg = rating
        utils.save_without_integrity(
            ExtDishRating(mensa=mensa, dish=dish, date=dish_plan_date, rating_avg=ratings_avg,
                          rating_count=ratings_count))

    def __scrape_meal(self, meal: Tag, mensa: Mensa, day: str) -> Tuple[
            str, Tuple[float, float], Tuple[list, list, list], Tuple[int, float]]:
        # load data of actual meal
        name = meal.find(class_="aw-meal-description").text

        # Get an image for the dish from duckduckgo
        image_url = self.__get_image_url(name)

        # The price for employees is not available on http://imensa.de but can be easily calculated at the
        # moment.
        price_for_students = utils.to_float(
            meal.find(title="Preis für Studierende").text[:-2])
        price_for_non_students = price_for_students * 1.5
        price = (price_for_non_students, price_for_students)

        attributes = meal.find(
            class_="small aw-meal-attributes").span.text.replace("\xa0", "").split(" ")

        att_type = 0
        categories = []
        additives = []
        allergies = []

        # Attributes of a meal are displayed in German and must be translated.
        for att in attributes:
            # check attribute type first
            if att == "ZUSATZ":
                att_type = 1
            elif att == "ALLERGEN":
                att_type = 2
            elif att == "ZULETZT":
                att_type = -1
            elif att_type >= 0:
                # translate attribute and add it to its corresponding list
                replacement = utils.translate(att, mensa=mensa.name, day=day)
                if att_type == 0:
                    categories.append(replacement)
                elif att_type == 1:
                    additives.append(replacement)
                elif att_type == 2:
                    allergies.append(replacement)
        groups = (categories, additives, allergies)

        # Find rating count and average. Might not be available.
        ratings_count_tag = meal.find(class_="aw-meal-histogram-count")
        ratings_count = 0
        if ratings_count_tag:
            ratings_count = utils.to_int(ratings_count_tag.text)

        ratings_avg_tag = meal.find(class_="aw-meal-histogram-average")
        ratings_avg = 0
        if ratings_avg_tag:
            ratings_avg = utils.to_float(ratings_avg_tag.text)

        rating = (ratings_count, ratings_avg)

        return name, price, groups, rating, image_url

    def _build_urls(self) -> List[Tuple[str, dict]]:
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
        return now + timedelta(days=diff)

    def __get_image_url(self, name: str) -> str:
        results = self.__search(name)
        image_url: str = None

        if results:
            if type(results) is dict:
                if 'results' in results:
                    for result in results['results']:
                        if result['height'] < result['width']:
                            image_url = result['image']
                            break

        return image_url

    def __search(self, keywords: str, max_results=None):
        url = 'https://duckduckgo.com/'
        params = {
            'q': keywords
        }

        #   First make a request to above URL, and parse out the 'vqd'
        #   This is a special token, which should be used in the subsequent request
        res = requests.post(url, data=params)
        searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

        if not searchObj:
            return -1

        headers = {
            'authority': 'duckduckgo.com',
            'accept': 'application/json, text/javascript, */* q=0.01',
            'sec-fetch-dest': 'empty',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://duckduckgo.com/',
            'accept-language': 'en-US,enq=0.9',
        }

        params = (
            ('l', 'de-de'),
            ('o', 'json'),
            ('q', keywords),
            ('vqd', searchObj.group(1)),
            ('f', ',,,,layaout:Wide,license:Share'),
            ('p', '1'),
            ('v7exp', 'a'),
        )

        requestUrl = url + "i.js"

        data = None
        try:
            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)
        except:
            print("Failure: ", res.status_code, keywords)

        return data
