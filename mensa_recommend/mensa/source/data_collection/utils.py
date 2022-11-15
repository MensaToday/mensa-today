from bs4 import BeautifulSoup
import requests
import re

non_digit = re.compile('[^0-9,.]')

attribute_replacement = {
    "vegan": "Vegan",
    "vegetarisch": "Vegetarian",
    "schwein": "Pork",
    "rind": "Beef",
    "geflügel": "Poultry",

    "farbstoff": "Dyed",
    "konservierungsstoffe": "Preservatives",
    "antioxidationsmittel": "Antioxidants",
    "geschmacksverstärker": "Flavor enhancers",
    "geschwefelt": "sulphurated",
    "geschwärzt": "blackened",
    "gewachst": "waxed",
    "phosphat": "Phosphate",
    "süßungsmittel": "Sweeteners",
    "phenylalaninquelle": "Phenylalanine source",

    "gluten": "Gluten",
    "dinkel": "Spelt",
    "gerste": "Barley",
    "hafer": "Oats",
    "kamut": "Kamut",
    "roggen": "Rye",
    "weizen": "Wheat",

    "krebstiere": "Crustaceans",
    "ei": "Egg",
    "fisch": "Fish",
    "erdnüsse": "Peanuts",
    "soja": "Soy",
    "milch": "Milk",

    "schalenfrüchte": "Nuts",
    "mandeln": "Almonds",
    "haselnüsse": "Hazelnuts",
    "walnüsse": "Walnuts",
    "cashewkerne": "Cashews",
    "pecannüsse": "Pecans",
    "paranüsse": "Brazil nuts",
    "pistazien": "Pistachios",
    "macadamianüsse": "Macadamias",

    "sellerie": "Celery",
    "senf": "Mustard",
    "sesam": "Sesame",
    "lupinen": "Lupines",
    "weichtiere": "Molluscs",
    "schwefeldioxid": "Sulfur dioxide",
}


def get_soup(url: str) -> BeautifulSoup:
    document: str = requests.get(url).text
    return BeautifulSoup(document, "lxml")


def __remove_non_digit__(s: str) -> str:
    return non_digit.sub("", s)


def to_float(s: str) -> float:
    return float(__remove_non_digit__(s).replace(",", "."))


def to_int(s: str) -> float:
    return int(__remove_non_digit__(s))


class Collector:
    def __init__(self):
        pass

    def run(self):
        raise Exception("Run method is not overwritten.")
