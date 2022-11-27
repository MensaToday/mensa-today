from typing import Union

def transform_rating(rating: int) -> Union[float, None]:

    if rating >= 0 and rating <= 5:
        return rating/5
    else:
        return None