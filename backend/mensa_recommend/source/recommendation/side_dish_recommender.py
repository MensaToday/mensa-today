from typing import Optional

from django.db.models import Count

from mensa.models import DishPlan, UserSideSelection


def predict(main_dish: DishPlan) -> Optional[DishPlan]:
    """Predicting side dish recommendations. This process is efficient
    and can be executed synchronously without any problems.

    Parameters
    ----------
    main_dish : DishPlan
        The main dish for which a side dish should be predicted.

    Return
    ------
    side : Optional[DishPlan]
        The predicted side dish (if available).
    """
    popular = UserSideSelection.objects \
        .filter(main__dish__id=main_dish.dish.id) \
        .values("side__dish__id") \
        .annotate(count=Count('side__dish__id')) \
        .order_by("-count")

    for p in popular:
        side_id = p["side__dish__id"]

        # Choose the most popular side dish that is available at the same day
        # and mensa.
        try:
            side = DishPlan.objects.get(dish__id=side_id,
                                        mensa=main_dish.mensa,
                                        date=main_dish.date)

            return side
        except DishPlan.DoesNotExist:
            pass

    # No side dish found -> ignore.
    return None


