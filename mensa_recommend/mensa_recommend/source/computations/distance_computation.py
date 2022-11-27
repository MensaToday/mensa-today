
from math import radians, cos, sin, asin, sqrt


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)

        Parameters
        ----------
        lon1 : float
            Longitude of the first element
        lat1 : float
            Latitude of the first element
        lon2 : float
            Longitude of the second element
        lat2 : float
            Latitude of the second element


        Return
        ------
        distance : float
            Distance between two points based on Longitude and Latitude

    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 6371

    distance = c * r

    return distance