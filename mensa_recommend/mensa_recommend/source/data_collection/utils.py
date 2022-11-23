import json
import re
import threading
from abc import ABC, abstractmethod
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.db.models import Model

__non_digit__ = re.compile('[^0-9,.]')

# load translation dictionary
with open("translate.json", "r") as file:
    __translations__ = json.load(file)


def translate(key: str, **context) -> str:
    """
        Translates the given key or, if unknown, raises an exception.
    """
    key = key.lower()
    if key in __translations__:
        return __translations__[key]
    else:
        raise TranslationKeyNotFound(key, **context)


class TranslationKeyNotFound(Exception):
    def __init__(self, key: str, **context) -> None:
        super().__init__(f"Could not find '{key}' in translate.json! Context: {context}")


def _remove_non_digit(s: str) -> str:
    """Remove non-digit characters from a string using regex.

    Parameters
    ----------
    s : str
        The text that should be processed.

    Return
    ------
    s : str
        The transformed string which now contains digits only.
    """
    return __non_digit__.sub("", s)


def to_float(s: str) -> float:
    """Transform a string into a float supporting German strings containing not only digits.

    Parameters
    ----------
    s : str
        The text that should be processed.

    Return
    ------
    f : float
        The processed float.
    """
    return float(_remove_non_digit(s).replace(",", "."))


def to_int(s: str) -> float:
    """Transform a string into an int supporting German strings containing not only digits.

    Parameters
    ----------
    s : str
        The text that should be processed.

    Return
    ------
    i : int
        The processed int.
    """
    return int(to_float(s))


def response_to_soup(res: requests.Response) -> BeautifulSoup:
    """Create a soup object by a given HTML response.

    Parameters
    ----------
    res : request response
        The response of the performed request.

    Return
    ------
    soup : BeautifulSoup
        The created soup document.
    """
    document: str = res.text
    return BeautifulSoup(document, "lxml")


def url_to_soup(url: str, headers: dict = None) -> BeautifulSoup:
    return response_to_soup(requests.get(url, headers=headers))


def save_without_integrity(model_instance: Model) -> None:
    """Save database models and catch integrity errors silently. Can be used to ignore duplicated entries in a compact
    way.

    Parameters
    ----------
    model_instance : database model
        The database model that should be saved.
    """
    try:
        model_instance.save()
    except IntegrityError:
        pass


class Collector(ABC):
    @abstractmethod
    def run(self) -> None:
        """
            Main "run" method to invoke any type of data collection.
            Can be executed by running `python manage.py collect -s <source>` if registered in the corresponding
            `collect.py` file.
        """
        pass

    def prepare(self) -> None:
        """
            A prepare method that can be invoked by `python manage.py collect -s <source> -p` if registered in the
            corresponding `collect.py` file.

            Can be used to prepare static database changes in order to automatically run the data collector.
        """
        pass


class NoAuthURLCollector(Collector):
    def run(self) -> None:
        # Make use of threading to improve performance of simultaneous URL requests
        threads = []
        for url, options in self._build_urls():
            t = threading.Thread(target=self.__run, args=(url,), kwargs=options)
            threads.append(t)
            t.start()

        # Wait until every thread performed its task
        for t in threads:
            t.join()

    def __run(self, url: str, **options) -> None:
        # Create soup document; This is the part with the blocking URL request
        soup = url_to_soup(url)

        # Perform main scrape process
        self._scrape(soup, **options)

    @abstractmethod
    def _build_urls(self) -> List[Tuple[str, dict]]:
        """Abstract method to register URLs.

        Return
        ------
        urls : (url, options-dict)
            The urls that should be scraped including options per url to pass custom values to the final scrape method.
        """
        pass

    @abstractmethod
    def _scrape(self, document: BeautifulSoup, **options) -> None:
        """Abstract method for the final scrape process.

        Parameters
        ----------
        document : soup object
            The soup object created by the response of the HTML request.
        """
        pass
