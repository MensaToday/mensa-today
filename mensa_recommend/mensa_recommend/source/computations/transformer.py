from typing import Union

def transform_rating(rating: Union[int]) -> Union[float, None]:
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

    if rating >= 1 and rating <= 5:
        return rating/5
    else:
        return None