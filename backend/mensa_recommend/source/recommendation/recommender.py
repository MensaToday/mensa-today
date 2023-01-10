import logging
from datetime import date, timedelta, datetime, time
from typing import List, Tuple, Dict, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from mensa.models import UserDishRating, DishPlan, Dish, UserAllergy, \
    UserCategory, Mensa
from mensa_recommend.serializers import DishPlanSerializer
from mensa_recommend.source.computations import distance_computation, \
    user_location
from mensa_recommend.source.data_collection import weather
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


def multiply(f: float, factors: List[Optional[float]],
             min_value: float = 0.1, max_value: float = 1.0) -> float:
    """Multiply a float f with a list of factors but consider minimum and
    maximum bounds.

    Parameters
    ----------
    f : float
        The float that should be multiplied.
    factors : List[Optional[float]]
        The list of factors. Can contain None values.
    min_value : float
        The minimum value that a factor is allowed to be.
    max_value : float
        The maximum value that a factor is allowed to be.

    Return
    ------
    f : float
        The result.
    """
    for factor in factors:
        if factor is not None:
            bounded = min(max(factor, min_value), max_value)
            f *= bounded
    return f


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

        # TODO: The time when the user wants to eat. This is currently static
        #  but might be changed in the future.
        self._daytime: time = time(hour=12)
        # TODO: Max number of kilometers the user would drive at most.
        #  In the future this might be an option the user can configure.
        #  Must be > 0.
        self._flexibility = 3
        self._mensa_distances = self.__compute_mensa_distance_scores()

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
            logging.debug(
                f"Recommender: No dishes found! start={self._date_start}, "
                f"end={self._date_end}")
            return

        self.filtered_dishes = self.__filter_dishes()

        # only 0 if hard filters are too strict
        if len(self.filtered_dishes) > 0:
            # computational overhead: calculating the sentence bert embeds
            # takes time
            self._encoded_dishes = self.__encode_dishes(self.filtered_dishes)

    def predict(self, recommendations_per_day: int = 1,
                serialize: bool = False) -> Dict[date, List[
            Tuple[DishPlan, float]]]:
        """Predicting recommendations for a user. This process is efficient
        and can be executed synchronously without any problems.

        Parameters
        ----------
        recommendations_per_day : int
            The number of recommendations per day. Must be > 0. Default is 1.
        serialize: bool
            Whether DishPlan instances should be directly serialized.

        Return
        ------
        result : Dict[date, List[Tuple[DishPlan, float]]]
            The result per day encapsulated in a dict saved by the date
            itself. The list of recommendations per day is structured by a
            tuple combining the DishPlan (with information about dish, mensa
            and date) and the prediction value (0 <= p <= 1).
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
            pred = self.__predict_dishes(day, recommendations_per_day, dishes)

            # map the predictions back to DishPlan instances
            mapped = []
            for dish_id, dish_plan, _, p in pred:
                if serialize:
                    dish_plan = DishPlanSerializer(dish_plan, context={
                        'user': self._user, 'include_sides': True}).data

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
            The separated dishes combined by a dictionary with its date as
            key. Each day consists of a list of dishes that are available.
            Each dish is represented by a tuple combining the dish_id and the
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

    def __find_dish_in_plan(self, dish_id: int, day: date) \
            -> Tuple[DishPlan, Mensa]:
        """Find a dish in the loaded plan.

        Parameters
        ----------
        dish_id : int
            The id of the searched dish.
        day : date
            The date when this dish is available to speed up the search.

        Return
        ------
        location : Tuple[DishPlan, Mensa]
            The location.
        """
        location = None
        distance_score = -1

        for plan in self._plan[day]:
            if plan.dish.id == dish_id:
                mensa: Mensa = plan.mensa
                score = self.__dist_to_mensa(day, mensa)

                if location is None or distance_score < score:
                    location = plan, mensa
                    distance_score = score

        if location is None:
            raise KeyError(f"Could not find dish with id={dish_id}.")

        return location

    def __predict_dishes(self, day: date, recommendations_per_day: int,
                         available_dishes: List[Tuple[int, List[float]]]) -> \
            List[Tuple[int, DishPlan, Mensa, float]]:
        """Apply content-based filtering and select the best results. Core
        magic of the recommender class.

        Parameters
        ----------
        day: date
            The date of the recommendations.
        recommendations_per_day : int
            The number of recommendations per day. Must be > 0. Default is 1.
        available_dishes : List[Tuple[int, DishPlan, List[float]]]
            The dish pool structured by a list of tuples combining the
            dish_id, the dish_plan instance where this dish can be found and
            the dish characteristics vector.

        Return
        ------
        result : List[Tuple[int, DishPlan, Mensa, float]]
            The predictions in a DESC order. Structured by a list of tuples
            combining the dish_id, the location (DishPlan and Mensa) and the
            prediction value.
        """
        if len(available_dishes) == 0:
            return []

        # computes the user profile for the comparison
        profile = self.__compute_user_profile()

        predictions = []

        # compute the cosine_similarity between the profile and each dish from
        # the pool.
        for dish_id, enc in available_dishes:
            sim = distance_computation.cosine_similarity(profile, enc)

            # also load the dish_plan for position constraints
            dish_plan, mensa = self.__find_dish_in_plan(dish_id, day)
            predictions.append((dish_id, dish_plan, mensa, sim))

        # apply prediction constraints such as weather and path length
        predictions = self.__apply_pred_constraints(day, predictions)

        # selecting the top n results (sort by prediction value)
        predictions.sort(key=lambda val: val[3])
        top = predictions[:recommendations_per_day]
        return top

    def __apply_pred_constraints(self, day: date, predictions: List[Tuple[
            int, DishPlan, Mensa, float]]) \
            -> List[Tuple[int, DishPlan, Mensa, float]]:
        """Apply prediction side constraints such as weather quality or path
        length.

        Parameters
        ----------
        day: date
            The date of the recommendations.
        predictions : List[Tuple[int, DishPlan, Mensa, float]]
            The computed predictions.

        Return
        ------
        result : List[Tuple[int, DishPlan, Mensa, float]]
            The predictions considering all constraints.
        """
        weather_scores: Dict[int, float] = {}

        result = []
        for dish_id, dish_plan, mensa, p in predictions:
            # make api call to get weather score
            if mensa.zipCode not in weather_scores:
                weather_scores[mensa.zipCode] = weather.get_score(
                    datetime.combine(day, self._daytime),
                    mensa.lat,
                    mensa.lon
                )

            local_weather = weather_scores[mensa.zipCode]
            dist_score = self.__dist_to_mensa(day, mensa)

            # Do not mess up predictions if one of the constraints is 0.
            # Therefore, bound constraints to a range of 0.1-1.
            p = multiply(p, [local_weather, dist_score])

            result.append((dish_id, dish_plan, mensa, p))
        return result

    def __dist_to_mensa(self, day: date, mensa: Mensa) -> float:
        """Get the user distance to a mensa if available. Otherwise, return 0.

        Parameters
        ----------
        day: date
            The specific day that should be checked.
        mensa: Mensa
            The mensa that should be checked.

        Return
        ------
        distance : float
            The distance or 0 if no distance was found.
        """
        if day in self._mensa_distances:
            distances = self._mensa_distances[day]
            mid = mensa.id

            if mid in distances:
                return distances[mid]
        return 0

    def __compute_mensa_distance_scores(self) -> Dict[date, Dict[int, float]]:
        """Compute scores for mensa distances for every required day, so they
        can be used when combining the prediction constraints.

        Return
        ------
        distances : Dict[date, Dict[int, float]]
            The distance scores per day.
        """
        week_distances = {}

        for day in self.__days():
            distances = user_location.get_user_location(self._user,
                                                        current_date=day,
                                                        _time=self._daytime)
            for key in distances.keys():
                score = 1 - min(distances[key] / self._flexibility, 1)
                distances[key] = score

            week_distances[day] = distances
        return week_distances

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
        x = [0] * data_vector_length

        for rating in self._ratings:
            # consider only ratings that are not hard filtered
            if rating.dish.id in mapped:
                data = mapped[rating.dish.id]
                x += np.multiply(rating.rating, data)
        return x

    def __encode_dishes(self, dishes: List[Dish]) \
            -> List[Tuple[int, List[float]]]:
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
