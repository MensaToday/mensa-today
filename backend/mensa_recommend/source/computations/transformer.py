from typing import Union


def transform_rating(rating: int) -> Union[float, None]:
    """Transform a rating of the form 1-5 to a float of the form 0-1

        Parameters
        ----------
        rating: int
            A rating between 1-5


        Return
        ------
        rating: float, None
            If the rating is not between 1-5 a None will be returned.
            Otherwise a rating between 0-1 will be the output.

    """
    if rating > 0 and rating <= 5:
        return rating/5
    else:
        return None


def transform_week_day_to_int(week_day: str) -> int:
    """Transform a week day (string) into an integer between 0 (Monday) and 5 (Sunday)

        Parameters
        ----------
        week_day: str
            A weekday as string (Mon.-Sun.)


        Return
        ------
        week_day: int
            A weekday as integer (0-5)
            If the string is not valid then a -1 will be returned

    """

    if week_day == 'Mon.':
        return 0
    elif week_day == 'Tue.':
        return 1
    elif week_day == 'Wed.':
        return 2
    elif week_day == 'Thu.':
        return 3
    elif week_day == 'Fri.':
        return 4
    elif week_day == 'Sat.':
        return 4
    elif week_day == 'Sun.':
        return 5
    else:
        return -1
