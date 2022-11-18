import re
from abc import ABC, abstractmethod
from typing import List, Tuple
import json

import requests
from bs4 import BeautifulSoup

__non_digit__ = re.compile('[^0-9,.]')

from django.db import IntegrityError

from django.db.models import Model

with open("translate.json", "r") as file:
    __translations__ = json.load(file)


def translate(key: str) -> str:
    """
        Translates the given key or, if unknown, returns the key itself.
    """
    key = key.lower()
    if key in __translations__:
        return __translations__[key]
    else:
        return key


def _remove_non_digit(s: str) -> str:
    return __non_digit__.sub("", s)


def to_float(s: str) -> float:
    return float(_remove_non_digit(s).replace(",", "."))


def to_int(s: str) -> float:
    return int(to_float(s))


def response_to_soup(res: requests.Response) -> BeautifulSoup:
    document: str = res.text
    return BeautifulSoup(document, "lxml")


def url_to_soup(url: str) -> BeautifulSoup:
    return response_to_soup(requests.get(url))


def save_integrity_free(model_instance: Model) -> None:
    try:
        model_instance.save()
    except IntegrityError:
        pass


class Collector(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    def prepare(self) -> None:
        pass


class NoAuthCollector(Collector):
    def run(self) -> None:
        for url, options in self.__build_urls():
            # TODO: Run calls in parallel
            soup = url_to_soup(url)
            self.__scrape(soup, **options)

    @abstractmethod
    def __build_urls(self) -> List[Tuple[str, dict]]:
        pass

    @abstractmethod
    def __scrape(self, document: BeautifulSoup, **options) -> None:
        pass
