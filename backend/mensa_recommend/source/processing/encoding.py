from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from mensa.models import Dish


def encode_binary(att_list: List[List[int]]) -> List[List[int]]:
    """Encode an attribute list containing lists of integers for each item to
    binary attributes. Every item (dim=0) may contain a different number of
    attributes.

    Parameters
    ----------
    att_list : list
        The list of attribute-lists.

    Return
    ------
    res : List[List[int]]
        The binary encoded attribute list. All items now have same
        attribute-list lengths and binary values only.
    """
    if len(att_list) == 0:
        return []

    max_val = max(att_list)
    if len(max_val) == 0:
        # Return 'att_list' since we must remain the size
        # even if all entries are empty.
        return att_list
    max_val = max_val[0]

    res = []

    for obj in att_list:
        part = []
        for value in range(max_val):
            part.append(1 if value in obj else 0)
        res.append(part)
    return res


class DishEncoder:
    # This version of a sentence transformer was the smallest I could find.
    # Size: ~100MB
    sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def __init__(self):
        self.dishes: List[Dish] = []

    def encode(self) -> List[Tuple[int, List[float]]]:
        """Encode all available dishes. Requires them to be already loaded.

                Return
                ------
                enc : List[Tuple[int, List[float]]]
                    The encoded dishes structured by a list of tuples combining
                    the dish_id and the dish characteristic vector.
                """
        self.__update_dishes()

        enc = []

        # encode all attributes
        enc_cat = self.__encode_categories()
        enc_add = self.__encode_additives()
        enc_all = self.__encode_allergies()

        # Sentence bert creates a numpy.ndarray as result. Therefore, we have
        # to convert them to lists at a later point to concatenate all
        # different values.
        enc_names = self.__encode_names()

        # combine all encodings
        for i in range(len(self.dishes)):
            d = self.dishes[i]
            data = enc_cat[i] + enc_add[i] + enc_all[i] + list(enc_names[i])
            enc.append((d.id, data))

        return enc

    def __update_dishes(self) -> None:
        self.dishes = Dish.objects.all()

    def __encode_categories(self) -> List[List[int]]:
        """Encode all given categories using binary encoding.

        Return
        ------
        categories : List[List[int]]
            The encoded categories.
        """
        categories = [[a.id for a in d.categories.all()] for d in self.dishes]

        return encode_binary(categories)

    def __encode_additives(self) -> List[List[int]]:
        """Encode all given additives using binary encoding.

        Return
        ------
        additives : List[List[int]]
            The encoded additives.
        """
        additives = [[a.id for a in d.additives.all()] for d in self.dishes]

        return encode_binary(additives)

    def __encode_allergies(self) -> List[List[int]]:
        """Encode all given allergies using binary encoding.

        Return
        ------
        allergies : List[List[int]]
            The encoded allergies.
        """
        allergies = [[a.id for a in d.allergies.all()] for d in self.dishes]

        return encode_binary(allergies)

    def __encode_names(self) -> np.ndarray[np.ndarray[float]]:
        """Encode all given names using sentence bert. This may take a bit and
        requires more computational power with an increasing dish pool.

        Return
        ------
        embeds : numpy.ndarray[numpy.ndarray[float]]
            The encoded categories.
        """
        names = [d.name for d in self.dishes]
        return self.sentence_transformer.encode(names)
