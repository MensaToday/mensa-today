import django.db.models as Model
from mensa.models import Dish, DishPlan
from django.db.models.query import QuerySet
from datasketch import MinHash, MinHashLSH
from abc import ABC, abstractmethod

from typing import Tuple


class LSH(ABC):
    """Class to search for duplicates in a database queryset and 
    optionally remove the duplicate entries
    """

    def __init__(self, queryset: QuerySet = None, num_perm: int = 128, threshold: float = 0.7):
        """Constructor

        Parameters
        ----------
        queryset : QuerySet (optional)
            A django Queryset Object. If it is None only the remove function can be used
            which is based on the ids to be deleted and the model object
        num_perm : int
            Number of min hash permuatations (default = 128)
        threshold: float
            Threshold at which a tuple is seen as similar
        """

        self.num_perm = num_perm
        self.threshold = threshold
        self.queryset = queryset

        if self.queryset is not None:
            self.set_list = self._create_sets()
            self.min_hashes, self.lsh = self._initialize_lsh()

    def get_duplicates(self) -> set[Tuple[int]]:
        """Searches for duplicates based on minhashes

        Return
        ------
        duplicates : set[Tuple[int]]
            A set of tuples with duplicate values. A set was chosen as the return type,
            since only one duplicate tuple should be returned for every unique duplicate
            detection. The integers represent the ids.
        """

        if (self.queryset is None):
            raise ("To use this function a queryset has to be defined.")

        duplicates = []

        # Iterate over each min hash and find duplicate values
        for hash in self.min_hashes:
            neighbors = self.lsh.query(hash[1])
            duplicates.append(neighbors)

        return set(tuple(i) for i in duplicates if len(i) > 1)

    @abstractmethod
    def _create_sets(self) -> list[Tuple[int, set[str]]]:
        """Abstract method to generate a list of sets over the search strings/documents.
        Because this process is unique for every queryset this function has to be overwritten
        by the concrete implementation.

        Return
        ------
        return : list[Tuple[int, set[str]]]
            A list of tuples. Each tuple consists of a tuple id and the set of an input string/document.
        """
        pass

    @abstractmethod
    def fuse_duplicates(self, duplicates: set[Tuple[int]]):
        """Abstract method to fuse objects together based on a set of duplicate tuples with ids.
        Because the fuse process is handle individually for each database table this method has to be
        overwritten.

        Parameters
        ----------
        duplicates : set[Tuple[int]]
            A set of tuples with the ids of duplicate objects
        """
        pass

    def _initialize_lsh(self) -> Tuple[list[MinHash], MinHashLSH]:
        """Create a list of minhashes for each input set and also initalize the lsh object.

        Return
        ------
        return : Tuple[list[MinHash], MinHashLSH]
            A list of minhashes and a lsh object
        """

        if self.set_list is None:
            raise ("method _create_sets has to be executed first")

        # Create LSH index
        lsh = MinHashLSH(threshold=0.7, num_perm=self.num_perm)

        min_hashes = []
        for id, string_set in self.set_list:

            m = MinHash(num_perm=self.num_perm)

            for d in string_set:
                m.update(d.encode("utf8"))

            min_hashes.append((id, m))

            lsh.insert(id, m)

        return (min_hashes, lsh)


class DishLSH(LSH):

    def _create_sets(self) -> list[Tuple[int, set[str]]]:

        set_list = []

        for dish in self.queryset:
            string_set = set(dish.name.split())

            set_list.append((dish.id, string_set))

        return set_list

    def fuse_duplicates(self, duplicates: set[Tuple[int]]):
        # This function only replaces the ids in the dishplan but does not delete the dishes
        # in the Dish table
        for duplicate in duplicates:

            # When only one element is in the tuple jump to next element
            if len(duplicate) == 1:
                continue

            reference_index = duplicate[0]
            dish = Dish.objects.get(id=reference_index)

            for i in range(1, len(duplicate)):
                dishplans = DishPlan.objects.filter(dish=duplicate[i]).all()

                for dishplan in dishplans:
                    dishplan.dish = dish
                    dishplan.save()
