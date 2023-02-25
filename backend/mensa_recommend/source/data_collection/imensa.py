from datetime import datetime, date, timedelta
from typing import List, Tuple

from celery import shared_task
from bs4 import BeautifulSoup, Tag
from django.db import IntegrityError
import requests
import json
import re
import time
import os
import threading
from tqdm import tqdm
from google_images_search import GoogleImagesSearch

import global_data
from mensa.models import Category, Allergy, Additive, Dish, DishCategory, \
    DishAllergy, DishAdditive, DishPlan, Mensa, \
    ExtDishRating
from mensa_recommend.source.computations.lsh import DishLSH
from . import static_data
from . import utils
from .utils import NoAuthURLCollector


def _get_dish(name: str, main_meal: bool) -> Dish:
    """Load a dish by a given name or create one if absent. Can later be used
    to implement some sort of name matching in order to get rid of duplicated
    dishes.

    Parameters
    ----------
    name : str
        The name of a dish.
    main_meal : bool
        Whether the dish is a main or side meal.

    Return
    ------
    dish : dish
        The loaded dish.
    """
    try:
        return Dish.objects.get(name=name)
    except Dish.DoesNotExist:
        d = Dish(name=name, main=main_meal)

        # Ignore duplicate errors and just return the dish. Issue only occurs
        # in multithreading context. Using the created instead of the database
        # instance does not change much. The data is the same.
        try:
            # Get an image for the dish from google
            # gis = GoogleImagesSearch(
            #     os.environ.get("GOOGLE_API_KEY"),
            #     os.environ.get("GOOGLE_PROJECT_CX"))
            # image_url = _get_image_url(name, gis)
            # image_url = _get_image_url(name)
            # d.image_url = image_url
            d.save()
        except IntegrityError:
            pass

        return d


@shared_task(name='post_processing')
def post_processing():
    """Get all dishes from database and update with image url
    Translate all dishes to english

    """

    # Get all dishes
    dishes = Dish.objects.all()

    # Get duplicate dishes and fuse them
    dish_lsh = DishLSH(queryset=dishes)
    duplicates = dish_lsh.get_duplicates()
    dish_lsh.fuse_duplicates(duplicates)

    # Iteratate over each dish
    for dish in tqdm(dishes):

        # Only dishes without a dish url has to be concidered
        if dish.url is None:
            # Get the image url
            image_url = _get_image_url(dish.name)

            # Set new image url and save the updated dish
            dish.url = image_url
            dish.save()

            # One have to wait 0.2 seconds to not get a 403
            time.sleep(0.2)

        # DeepL api access
        if dish.translation is None:
            translated_text = _get_translation(dish.name)

            if translated_text is not None:
                dish.translation = translated_text

                try:
                    dish.save()
                except Exception:
                    pass


def _get_translation(name: str) -> str:
    """ Get the english translation for the dish

    Parameters
    ----------
    name : str
        The name of a dish.

    Return
    ------
    translation : str
        Translated dish name
    """

    deepl_base_url = "https://api-free.deepl.com/v2/translate"

    params = {
        "auth_key": os.getenv("DEEPL_KEY", "test"),
        "source_lang": "DE",
        "target_lang": "EN",
        "text": name
    }

    try:
        res = requests.get(deepl_base_url, params=params,
                           proxies=global_data.proxies)

        return res.json()["translations"][0]["text"]
    except:
        return None


def _get_image_url(name: str) -> str:
    """ Get the image url from duckduckgo

    Parameters
    ----------
    name : str
        The name of a dish.

    Return
    ------
    image_url : str
        Image url for the dish
    """

    # Search for the image url
    results = _search(name)

    image_url: str = None

    # Check if result is empty
    if results:
        # Check if result is a dict
        if type(results) is dict:
            # Check if results key is int results dict
            if 'results' in results:
                # Iterate over each result and check width and height
                for result in results['results']:
                    # The first image that fulfills requirement will be chosen
                    if result['height'] < result['width']:
                        image_url = result['image']
                        break
    return image_url


def _search(keywords: str) -> List[dict]:
    """ Get the image url from duckduckgo

    Parameters
    ----------
    keyword : str
        search keyword

    Return
    ------
    data : List[dict]
        List of dicts of image objects including the image_url
        Example object:
        {
            'height': 240,
            'image': 'https://img.chefkoch-cdn.de/rezepte/3088441461567943/bilder/950797/crop-360x240/thunfischteilchen-mit-tzatziki.jpg',
            'image_token': '860193bc9c375156c2ba03211e930fb3a14d12be60957097ff057bef907f31c3',
            'source': 'Bing',
            'thumbnail': 'https://tse4.mm.bing.net/th?id=OIP.moTqpt22cMfaoGoOkgEMrgAAAA&pid=Api',
            'thumbnail_token': 'cc3306afebc3adfdde31678d31cda61f9cd95a22b2da04284dd8ee3c3ccda6fd',
            'title': 'Thunfischteilchen mit Tzatziki von sii63 | Chefkoch',
            'url': 'https://www.chefkoch.de/rezepte/3088441461567943/Thunfischteilchen-mit-Tzatziki.html',
            'width': 360
        }
    """

    url = 'https://duckduckgo.com/'

    # A special 'vqd' token has to be parsed from duckduckgo to be able to receive
    # responses in upcoming requests
    res = requests.post(url, data={'q': keywords})
    search_res = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not search_res:
        return -1

    # Required headers
    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */* q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,enq=0.9',
    }

    # Define search parameters
    params = (
        ('l', 'de-de'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', search_res.group(1)),
        ('f', ',,,,layaout:Wide,license:Share'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    # Build request url
    base_image_url = url + "i.js"

    # make request to duckduckgo
    data = None
    try:
        res = requests.get(base_image_url, headers=headers,
                           params=params, proxies=global_data.proxies)
        data = json.loads(res.text)
    except:
        pass

    return data


def _get_google_image_url(self, name: str, gis: GoogleImagesSearch) -> str:
    search_params = static_data.search_params
    search_params["q"] = name

    result = gis.search(search_params=search_params)

    if len(result) > 0:
        image_url = result[0].url
    else:
        image_url = None

    return image_url


class IMensaCollector(NoAuthURLCollector):
    def __init__(self):
        self.url = "https://www.imensa.de/{city}/{mensa}/{day}.html"
        self.cities = {
            "muenster": [
                # "bistro-friesenring",  # does not exist anymore?
                "mensa-da-vinci", "bistro-denkpause",
                "bistro-katholische-hochschule",
                "bistro-durchblick", "bistro-frieden", "bistro-kabu",
                "bistro-oeconomicum", "hier-und-jetzt",
                "mensa-am-aasee",
                "mensa-am-ring", "mensa-bispinghof"
            ]
        }
        self.days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

    def run(self) -> None:
        # Make use of threading to improve performance of simultaneous URL requests
        threads = []
        for url, options in self._build_urls():
            t = threading.Thread(
                target=self._run, args=(url,), kwargs=options)
            threads.append(t)
            t.start()

        # Wait until every thread performed its task
        for t in threads:
            t.join()

        # Get image urls
        post_processing.delay()

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
            category_name: str = div.find(class_="aw-meal-category-name")\
                .text.lower()
            side_meal = category_name.startswith(
                "beilage") or category_name.startswith("dessert")

            # go to every meal in that meal category
            for meal in div.find_all(class_="aw-meal row no-margin-xs"):
                # Some "meals" entries are used to display information of the
                # mensa.
                # Therefore, check if a price is available.
                no_meal = meal.find(title="Preis für Studierende") is None
                if no_meal:
                    break

                # get meal information
                name, price, groups, rating = self.__scrape_meal(
                    meal, mensa, day)

                # either gets an existing dish or creates one
                d = _get_dish(name, not side_meal)

                # save additional meal data to database
                self.__save_groups(d, groups)
                self.__save_price(d, mensa, dish_plan_date, price)
                self.__save_rating(d, mensa, dish_plan_date, rating)

    def __save_groups(self, dish: Dish,
                      groups: Tuple[list, list, list]) -> None:
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

    def __save_price(self, dish: Dish, mensa: Mensa, dish_plan_date: date,
                     price: Tuple[float, float]) -> None:
        price_for_students, price_for_non_students = price
        utils.save_without_integrity(
            DishPlan(dish=dish, mensa=mensa, date=dish_plan_date,
                     priceStudent=price_for_students,
                     priceEmployee=price_for_non_students))

    def __save_rating(self, dish: Dish, mensa: Mensa, dish_plan_date: date,
                      rating: Tuple[int, float]) -> None:
        ratings_count, ratings_avg = rating
        utils.save_without_integrity(
            ExtDishRating(mensa=mensa, dish=dish, date=dish_plan_date,
                          rating_avg=ratings_avg,
                          rating_count=ratings_count))

    def __scrape_meal(self, meal: Tag, mensa: Mensa, day: str) -> Tuple[
            str, Tuple[float, float], Tuple[list, list, list], Tuple[int, float]]:
        # load data of actual meal
        name = meal.find(class_="aw-meal-description").text

        # The price for employees is not available on http://imensa.de but can
        # be easily calculated at the moment.
        price_for_students = utils.to_float(
            meal.find(title="Preis für Studierende").text[:-2])
        price_for_non_students = price_for_students * 1.5
        price = (price_for_students, price_for_non_students)

        attributes = []
        att_obj = meal.find(class_="small aw-meal-attributes")
        if att_obj is not None:
            attributes = att_obj.span.text.replace("\xa0", "").split(" ")

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

        return name, price, groups, rating

    def _build_urls(self) -> List[Tuple[str, dict]]:
        urls = []

        for city in self.cities.keys():
            m = self.cities[city]
            for mensa in m:
                mensa_db = Mensa.objects.get(name_id=mensa)

                for day in self.days:
                    urls.append(
                        (self.url.format(city=city, mensa=mensa, day=day),
                         {"mensa": mensa_db, "date": self.__day_to_date(day),
                          "day": day}))
        return urls

    def __day_to_date(self, day: str) -> date:
        weekday = self.days.index(day)
        now = datetime.now().date()
        diff = weekday - now.weekday()
        return now + timedelta(days=diff)
