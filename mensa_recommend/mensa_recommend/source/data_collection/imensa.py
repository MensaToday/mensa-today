from datetime import datetime, date
from typing import List, Tuple

from bs4 import BeautifulSoup, Tag

from mensa.models import Category, Allergy, Additive, Dish, DishCategory, DishAllergy, DishAdditive, DishPlan, Mensa, \
    ExtDishRating
from . import utils
from . import static_data
from .utils import NoAuthURLCollector


def _get_dish(name: str, main_meal: bool) -> Dish:
    """Load a dish by a given name or create one if absent. Can later be used to implement some sort of name matching in
    order to get rid of duplicated dishes.

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
        d.save()
        return d


class IMensaCollector(NoAuthURLCollector):
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
        # insert static categories, additives and allergies
        for c in static_data.categories:
            utils.save_integrity_free(Category(name=c))
        for a in static_data.additives:
            utils.save_integrity_free(Additive(name=a))
        for a in static_data.allergies:
            utils.save_integrity_free(Allergy(name=a))

        # insert mensa information
        for m in static_data.canteens:
            utils.save_integrity_free(m)

    def _scrape(self, document: BeautifulSoup, **options) -> None:
        mensa: Mensa = options["mensa"]
        dish_plan_date: date = options["date"]
        day: str = options["day"]

        # find every meal category on the page
        for div in document.find_all(class_="aw-meal-category"):
            category_name: str = div.find(class_="aw-meal-category-name").text
            side_meal = category_name.lower().startswith("beilage")

            no_meal = False
            # go to every meal in that meal category
            for meal in div.find_all(class_="aw-meal row no-margin-xs"):
                # Some "meals" entries are used to display information of the mensa.
                # Therefore, check if a price is available.
                no_meal = meal.find(title="Preis für Studierende") is None
                if no_meal:
                    break

                # get meal information
                name, price, groups, rating = self.__scrape_meal(meal, mensa, day)

                # either gets an existing dish or creates one
                d = _get_dish(name, not side_meal)

                # save additional meal data to database
                self.__save_groups(d, groups)
                self.__save_price(d, mensa, dish_plan_date, price)
                self.__save_rating(d, mensa, dish_plan_date, rating)

    def __save_groups(self, dish: Dish, groups: Tuple[list, list, list]) -> None:
        categories, additives, allergies = groups
        for c in categories:
            category = Category.objects.get(name=c)
            utils.save_without_integrity(DishCategory(dish=dish, category=category))
        for a in additives:
            additive = Additive.objects.get(name=a)
            utils.save_without_integrity(DishAdditive(dish=dish, additive=additive))
        for a in allergies:
            allergy = Allergy.objects.get(name=a)
            utils.save_without_integrity(DishAllergy(dish=dish, allergy=allergy))

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

        # The price for employees is not available on http://imensa.de but can be easily calculated at the
        # moment.
        price_for_students = utils.to_float(meal.find(title="Preis für Studierende").text[:-2])
        price_for_non_students = price_for_students * 1.5
        price = (price_for_non_students, price_for_students)

        attributes = meal.find(class_="small aw-meal-attributes").span.text.replace("\xa0", "").split(" ")

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
                    urls.append((self.url.format(city=city, mensa=mensa, day=day),
                                 {"mensa": mensa_db, "date": self.__day_to_date(day), "day": day}))
        return urls

    def __day_to_date(self, day: str) -> date:
        weekday = self.days.index(day)
        now = datetime.now().date()
        diff = weekday - now.weekday()
        return date(now.year, now.month, now.day + diff)
