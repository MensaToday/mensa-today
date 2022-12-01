from datetime import date, timedelta
from typing import List, Tuple, Dict

import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

from mensa.models import UserDishRating, DishPlan, Dish
from users.models import User


def cosine_similarity(l1: List[float], l2: List[float]) -> float:
    cos_sim = dot(l1, l2) / (norm(l1) * norm(l2))
    return cos_sim


def encode_binary(att_list: List[List[int]]) -> List[List[int]]:
    max_val = max(att_list)[0]
    res = []

    for obj in att_list:
        part = []
        for value in range(max_val):
            part.append(1 if value in obj else 0)
        res.append(part)
    return res


class DishRecommender:
    sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def __init__(self, user: User, day: date, entire_week: bool = False):
        self._user = user

        if entire_week:
            self._date_start = day - timedelta(days=day.weekday())
            self._date_end = day + timedelta(days=6 - day.weekday())
        else:
            self._date_start = day
            self._date_end = day

        self._plan: Dict[date, List[DishPlan]] = {}
        self._ratings: List[UserDishRating] = []
        self._dishes: List[Dish] = []
        self._encoded_dishes: List[Tuple[int, List[int]]] = []

    def load(self) -> None:
        if len(self._dishes) > 0:
            raise Exception("The method load() can only be called once!")

        self._plan = self.__load_dish_plan()
        self._ratings = self.__load_ratings()
        self._dishes = self.__extract_distinct_dishes()
        self._encoded_dishes = self.__encode_dishes()

    def predict(self, recommendations_per_day: int = 1) -> Dict[date, List[
            Tuple[DishPlan, float]]]:
        if len(self._dishes) == 0:
            raise Exception("Dishes not loaded! Run load() before.")

        if recommendations_per_day <= 0:
            raise ValueError("'recommendations_per_day' must be > 0.")

        separated_encoded_dishes = self.__get_separated_encoded_dishes()
        result = {}
        for day in self.__days():
            dishes = separated_encoded_dishes[day]
            pred = self.__predict_dishes(recommendations_per_day, dishes)

            mapped = []
            for dish_id, p in pred:
                mapped.append((self.__find_dish_in_plan(dish_id, day), p))
            result[day] = mapped

        return result

    def __days(self) -> List[date]:
        days = []
        for i in range((self._date_end - self._date_start).days + 1):
            current_date = self._date_start + timedelta(days=i)
            days.append(current_date)
        return days

    def __get_separated_encoded_dishes(self) -> Dict[
            date, List[Tuple[int, List[float]]]]:
        separated_dishes = {}
        for day in self._plan.keys():
            ids = set()
            for dp in self._plan[day]:
                ids.add(dp.dish.id)

            dishes = []
            for dish_id, dish in self._encoded_dishes:
                if dish_id in ids:
                    dishes.append((dish_id, dish))

            separated_dishes[day] = dishes
        return separated_dishes

    def __find_dish_in_plan(self, dish_id: int, day: date) -> DishPlan:
        for plan in self._plan[day]:
            if plan.dish.id == dish_id:
                return plan

        raise KeyError(f"Could not find dish with id={dish_id}.")

    def __predict_dishes(self, recommendations_per_day: int,
                         available_dishes: List[Tuple[int, List[float]]]) -> \
            List[Tuple[int, float]]:
        profile = self.__compute_user_profile(available_dishes)

        dish_ids = []
        predictions = []
        for dish_id, enc in available_dishes:
            dish_ids.append(dish_id)

            sim = cosine_similarity(profile, enc)
            predictions.append(sim)

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
        plan = {}
        for day in self.__days():
            plan[day] = DishPlan.objects.filter(date=day, dish__main=True)
        return plan

    def __load_ratings(self) -> List[UserDishRating]:
        return UserDishRating.objects.filter(user=self._user.id)

    def __extract_distinct_dishes(self) -> List[Dish]:
        dishes = set()
        for key in self._plan.keys():
            for dp in self._plan[key]:
                dishes.add(dp.dish)

        for rating in self._ratings:
            dishes.add(rating.dish)

        # important: change dishes back to list to ensure static dish order
        return list(dishes)

    def __compute_user_profile(self, encoded_dishes: List[
            Tuple[int, List[float]]]) -> List[float]:
        X = []
        for rating in self._ratings:
            X += np.multiply(rating.rating,
                             encoded_dishes[rating.dish.id])
        return X

    def __encode_dishes(self) -> List[Tuple[int, List[float]]]:
        enc = []

        enc_cat = self.__encode_categories()
        enc_add = self.__encode_additives()
        enc_all = self.__encode_allergies()
        enc_names = self.__encode_names()

        for i in range(len(self._dishes)):
            d = self._dishes[i]
            data = enc_cat[i] + enc_add[i] + enc_all[i] + list(enc_names[i])
            enc.append((d.id, data))

        return enc

    def __encode_categories(self) -> List[List[int]]:
        categories = []

        for d in self._dishes:
            categories.extend([c.id for c in d.categories])

        return encode_binary(categories)

    def __encode_additives(self) -> List[List[int]]:
        additives = []

        for d in self._dishes:
            additives.extend([a.id for a in d.additives])

        return encode_binary(additives)

    def __encode_allergies(self) -> List[List[int]]:
        allergies = []

        for d in self._dishes:
            allergies.extend([a.id for a in d.allergies])

        return encode_binary(allergies)

    def __encode_names(self) -> np.ndarray:
        names = [d.name for d in self._dishes]
        return self.sentence_transformer.encode(names)
