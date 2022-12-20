from users.models import User
from mensa.models import UserDishRating, Dish


def save_quiz_ratings(user: User, ratings: list[dict]):
    """Save quiz ratings for a user

    Parameters
    ----------
    user : User
        User object
    ratings : list
        List of ratings in the format {id: int, rating: int}
    """

    for rating in ratings:
        if 'id' in rating and 'rating' in rating:

            if rating['rating'] > 1 or rating['rating'] < 0:
                print("Rating in invalid range")
            else:
                try:
                    dish = Dish.objects.get(id=rating['id'])
                except:
                    dish = None

                if dish:
                    UserDishRating(
                        user=user, dish=dish,
                        rating=rating['rating']).save()
