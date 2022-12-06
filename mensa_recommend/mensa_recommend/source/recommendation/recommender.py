import logging
from datetime import date, timedelta, datetime
from typing import List, Tuple, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from api.serializers import DishPlanSerializer
from mensa.models import UserDishRating, DishPlan, Dish, UserAllergy, \
    UserCategory
from mensa_recommend.source.computations import distance_computation as dist
from users.models import User


def date_to_str(d: date) -> str:
    return d.strftime("%Y.%m.%d")


def str_to_date(s: str) -> date:
    return datetime.strptime(s, "%Y.%m.%d")


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
        return []
    max_val = max_val[0]

    res = []

    for obj in att_list:
        part = []
        for value in range(max_val):
            part.append(1 if value in obj else 0)
        res.append(part)
    return res


class DishRecommender:
    """
        The dish recommender class is the main class for generating
        recommendations. As of right now, the approach is held very naive
        without any inbetween savings to speed up the process in any way.

        Disclaimer: This should not be used in production but rather for a
        first demo and a most viable product.
    """
    # This version of a sentence transformer was the smallest I could find.
    # Size: ~100MB
    sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def __init__(self, user: User, day: date, entire_week: bool = False):
        """
            user : User
                The user for whom recommendations should be generated. This is
                important as we use content-based filtering and therefore
                recommend dishes based on previous ratings.
            day : date
                The day that should be recommended for.
            entire_week : bool
                If true, the method predict() returns predictions for the
                entire week. Otherwise, only recommendations for the day that
                was specified before are generated.
        """
        self._user = user
        self._user_categories: List[int] = []
        self._user_allergies: List[int] = []

        if entire_week:
            self._date_start = day - timedelta(days=day.weekday())
            self._date_end = self._date_start + timedelta(days=4)
        else:
            self._date_start = day
            self._date_end = day

        self._plan: Dict[date, List[DishPlan]] = {}
        self._ratings: List[UserDishRating] = []
        self.dishes: List[Dish] = []
        self.filtered_dishes: List[Dish] = []
        self._encoded_dishes: List[Tuple[int, List[int]]] = []

    def load(self) -> None:
        """Load important data and already prepares the dishes for predicting.
        Warning: This may take up to 1-2 seconds.

        Return
        ------
        res : List[List[int]]
            The binary encoded attribute list. All items now have same
            attribute-list lengths and binary values only.
        """
        if len(self.dishes) > 0:
            raise Exception("The method load() can only be called once!")

        # load user data
        self._user_categories = [uc.category_id for uc in
                                 UserCategory.objects.filter(user=self._user)]
        self._user_allergies = [ua.allergy_id for ua in
                                UserAllergy.objects.filter(user=self._user)]

        # load data from database
        self._plan = self.__load_dish_plan()
        self._ratings = self.__load_ratings()

        # extracting dishes for further encoding
        self.dishes = self.__extract_distinct_dishes()

        if len(self.dishes) == 0:
            raise Exception(
                f"No dishes found! start={self._date_start}, "
                f"end={self._date_end}")

        self.filtered_dishes = self.__filter_dishes()

        # only 0 if hard filters are too strict
        if len(self.filtered_dishes) > 0:
            # computational overhead: calculating the sentence bert embeds
            # takes time
            self._encoded_dishes = self.__encode_dishes(self.filtered_dishes)

    def predict(self, recommendations_per_day: int = 1,
                serialize: bool = False) -> Dict[date, List[
            Tuple[DishPlan, float]]]:
        """Predicting recommendations for a user. This process is efficient and
        can be executed synchronously without any problems.

        Parameters
        ----------
        recommendations_per_day : int
            The number of recommendations per day. Must be > 0. Default is 1.
        serialize: bool
            Whether DishPlan instances should be directly serialized.

        Return
        ------
        result : Dict[date, List[Tuple[DishPlan, float]]]
            The result per day encapsulated in a dict saved by the date itself.
            The list of recommendations per day is structured by a tuple
            combining the DishPlan (with information about dish, mensa and
            date) and the prediction value (0 <= p <= 1).
        """
        # Load the data if it has not been done yet. The data will be loaded
        # synchronously in this case.
        if len(self.dishes) == 0:
            self.load()

        if recommendations_per_day <= 0:
            raise ValueError("'recommendations_per_day' must be > 0.")

        # separate dishes by day
        separated_encoded_dishes = self.__get_separated_encoded_dishes()

        result = {}
        # compute results per day
        for day in self.__days():
            dishes = separated_encoded_dishes[day]
            pred = self.__predict_dishes(recommendations_per_day, dishes)

            # map the predictions back to DishPlan instances
            mapped = []
            for dish_id, p in pred:
                dish_plan = self.__find_dish_in_plan(dish_id, day)

                if serialize:
                    dish_plan = DishPlanSerializer(dish_plan, context={
                        'user': self._user}).data

                mapped.append((dish_plan, p))

            if serialize:
                result[date_to_str(day)] = mapped
            else:
                result[day] = mapped

        return result

    def __days(self) -> List[date]:
        """Get a list of valid days within the scope for recommending.

        Return
        ------
        days : List[date]
            The dates that define our scope.
        """
        days = []
        for i in range((self._date_end - self._date_start).days + 1):
            current_date = self._date_start + timedelta(days=i)
            days.append(current_date)
        return days

    def __get_separated_encoded_dishes(self) -> Dict[
            date, List[Tuple[int, List[float]]]]:
        """Separate combined encoded dishes to access them on a daily basis.

        Return
        ------
        separated_dishes : Dict[date, List[Tuple[int, List[float]]]]
            The separated dishes combined by a dictionary with its date as key.
            Each day consists of a list of dishes that are available. Each dish
            is represented by a tuple combining the dish_id and the
            characteristics vector for content-based filtering.
        """
        separated_dishes = {}
        for day in self._plan.keys():
            ids = set()

            # select dishes out of the current dish plan
            for dp in self._plan[day]:
                ids.add(dp.dish.id)

            dishes = []

            # search for relevant dishes
            for dish_id, dish in self._encoded_dishes:
                if dish_id in ids:
                    dishes.append((dish_id, dish))

            separated_dishes[day] = dishes
        return separated_dishes

    def __find_dish_in_plan(self, dish_id: int, day: date) -> DishPlan:
        """Find a dish in the loaded plan.

        Parameters
        ----------
        dish_id : int
            The id of the searched dish.
        day : date
            The date when this dish is available to speed up the search.

        Return
        ------
        plan : DishPlan
            The DishPlan instance combining the relevant dish and its mensa
            where the dish is actually available.
        """
        for plan in self._plan[day]:
            if plan.dish.id == dish_id:
                return plan

        raise KeyError(f"Could not find dish with id={dish_id}.")

    def __predict_dishes(self, recommendations_per_day: int,
                         available_dishes: List[Tuple[int, List[float]]]) -> \
            List[Tuple[int, float]]:
        """Apply content-based filtering and select the best results. Core
        magic of the recommender class.

        Parameters
        ----------
        recommendations_per_day : int
            The number of recommendations per day. Must be > 0. Default is 1.
        available_dishes : List[Tuple[int, List[float]]]
            The dish pool structured by a list of tuples combining the dish_id
            and the dish characteristics vector.

        Return
        ------
        result : List[Tuple[int, float]]
            The predictions in a DESC order. Structured by a list of tuples
            combining the dish_id and the prediction value.
        """
        if len(available_dishes) == 0:
            return []

        # computes the user profile for the comparison
        profile = self.__compute_user_profile()

        dish_ids = []
        predictions = []

        # compute the cosine_similarity between the profile and each dish from
        # the pool.
        for dish_id, enc in available_dishes:
            dish_ids.append(dish_id)

            sim = dist.cosine_similarity(profile, enc)
            predictions.append(sim)

        # selecting the top n results
        # disclaimer: this is not the most efficient way for a selection, but
        # it also should not create any performance reasons.
        result = []
        for _ in range(recommendations_per_day):
            # get best prediction
            max_id = np.argmax(predictions)

            # insert prediction with dish_id into result list
            p = (dish_ids[max_id], predictions[max_id])
            result.append(p)

            # remove max value
            dish_ids.pop(max_id)
            predictions.pop(max_id)
        return result

    def __load_dish_plan(self) -> Dict[date, List[DishPlan]]:
        """Load the dish plan from the database.

        Return
        ------
        plan : Dict[date, List[DishPlan]]
            The dish plan for every day.
        """
        plan = {}
        for day in self.__days():
            plan[day] = DishPlan.objects.filter(date=day, dish__main=True)
        return plan

    def __load_ratings(self) -> List[UserDishRating]:
        """Load the user ratings from the database.

        Return
        ------
        result : List[UserDishRating]
            All ratings of the selected user that could be found.
        """
        return UserDishRating.objects.filter(user=self._user)

    def __extract_distinct_dishes(self) -> List[Dish]:
        """Extract all distinct dishes that were loaded by the dish plan and
        the user ratings.

        Return
        ------
        dishes : List[Dish]
            All dishes that were loaded.
        """
        dishes = set()
        for key in self._plan.keys():
            for dp in self._plan[key]:
                dishes.add(dp.dish)

        for rating in self._ratings:
            dishes.add(rating.dish)

        # important: change dishes back to list to ensure static dish order
        return list(dishes)

    def __apply_hard_filter(self, dish: Dish) -> bool:
        """Apply hard filters of the specified user. Hard filters contain
        selected food categories and allergies.

        Parameters
        ----------
        dish : Dish
            The dish the should be checked.

        Return
        ------
        result : bool
            True, if this dish is applicable. False, if this dish should be
            removed in further computations.
        """
        categories = [c.id for c in dish.categories.all()]
        for c in categories:
            if c not in self._user_categories:
                return False

        if len(self._user_allergies) > 0:
            allergies = [a.id for a in dish.allergies.all()]
            for a in allergies:
                if a in self._user_allergies:
                    return False
        return True

    def __filter_dishes(self) -> List[Dish]:
        """Filter dishes by using predefined filters.

        Return
        ------
        filtered : List[Dish]
            The filtered dishes.
        """
        filtered = []
        for d in self.dishes:
            if self.__apply_hard_filter(d):
                filtered.append(d)
        return filtered

    def __compute_user_profile(self) -> List[float]:
        """Compute the user profile by multiplying the ratings with their
        corresponding dish characteristic vectors.

        Return
        ------
        X : List[float]
            The user profile.
        """
        mapped = {dish_id: data for dish_id, data in self._encoded_dishes}

        # instantiate profile with zeros and
        data_vector_length = len(self._encoded_dishes[0][1])
        X = [0] * data_vector_length

        for rating in self._ratings:
            # consider only ratings that are not hard filtered
            if rating.dish.id in mapped:
                data = mapped[rating.dish.id]
                X += np.multiply(rating.rating, data)
        return X

    def __encode_dishes(self, dishes: List[Dish]) -> List[Tuple[int, List[float]]]:
        """Encode all available dishes. Requires them to be already loaded.

        Return
        ------
        enc : List[Tuple[int, List[float]]]
            The encoded dishes structured by a list of tuples combining the
            dish_id and the dish characteristic vector.
        """
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
        for i in range(len(dishes)):
            d = dishes[i]
            data = enc_cat[i] + enc_add[i] + enc_all[i] + list(enc_names[i])
            enc.append((d.id, data))

        return enc

    def __encode_categories(self) -> List[List[int]]:
        """Encode all given categories using binary encoding.

        Return
        ------
        categories : List[List[int]]
            The encoded categories.
        """
        categories = []

        for d in self.dishes:
            categories.append([c.id for c in d.categories.all()])

        return encode_binary(categories)

    def __encode_additives(self) -> List[List[int]]:
        """Encode all given additives using binary encoding.

        Return
        ------
        additives : List[List[int]]
            The encoded additives.
        """
        additives = []

        for d in self.dishes:
            additives.append([a.id for a in d.additives.all()])

        return encode_binary(additives)

    def __encode_allergies(self) -> List[List[int]]:
        """Encode all given allergies using binary encoding.

        Return
        ------
        allergies : List[List[int]]
            The encoded allergies.
        """
        allergies = []

        for d in self.dishes:
            allergies.append([a.id for a in d.allergies.all()])

        return encode_binary(allergies)

    def __encode_names(self) -> np.ndarray[np.ndarray[float]]:
        """Encode all given names using sentence bert. This may take a bit and
        requires more computational power with an increasing dish pool.

        Return
        ------
        embdes : numpy.ndarray[numpy.ndarray[float]]
            The encoded categories.
        """
        names = [d.name for d in self.dishes]
        return self.sentence_transformer.encode(names)
