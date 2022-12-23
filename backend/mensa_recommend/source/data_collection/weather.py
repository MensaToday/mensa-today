import requests
import datetime


api_url = "https://api.open-meteo.com/v1/forecast" \
          "?latitude=51.96" \
          "&longitude=7.63" \
          "&hourly=temperature_2m,rain,snowfall,windspeed_10m" \
          "&daily=weathercode" \
          "&timezone=Europe%2FBerlin" \
          "&start_date={start}" \
          "&end_date={end}"


def get_score(day: datetime.datetime) -> float:
    """Request the weather at the given date from https://open-mateo.com and
    calculate a single combined score.

    Parameters
    ----------
    day : datetime.datetime
        The date that should be checked

    Return
    ------
    score : float
        A weather score that ranges from 0 to the best value 1.
    """
    formatted = day.strftime("%Y-%m-%d")
    res = requests.get(api_url.format(start=formatted, end=formatted)).json()
    hourly = res["hourly"]

    temp = hourly["temperature_2m"]
    rain = hourly["rain"]
    snowfall = hourly["snowfall"]
    wind = hourly["windspeed_10m"]

    hour = day.hour + (1 if day.minute >= 20 else 0)

    c_temp = temp[hour]
    c_rain = rain[hour]
    c_snow = snowfall[hour]
    c_wind = wind[hour]

    points = 0
    max_points = 0

    max_points += 15
    # in °C
    if c_temp < -5:
        points += 15
    elif c_temp < 0:
        points += 5
    elif c_temp < 5:
        points += 2
    elif c_temp < 10:
        points += 1

    max_points += 15
    # in mm
    if c_rain >= 30:
        points += 15
    elif c_rain >= 10:
        points += 8
    elif c_rain >= 2.5:
        points += 4
    elif c_rain >= 0:
        points += 1

    max_points += 15
    # in cm
    if c_snow >= 10:
        points += 15
    elif c_snow >= 3:
        points += 4
    elif c_snow >= 1:
        points += 2
    elif c_snow >= 0:
        points += 1

    max_points += 15
    # in km/h
    if c_wind >= 60:    # stormy wind
        points += 15
    elif c_wind >= 40:  # strong wind
        points += 9
    elif c_wind >= 30:  # fresh breeze
        points += 3
    elif c_wind >= 12:  # faint breeze
        points += 1

    # This formular seemed to work best with the given values. Currently,
    # no scientific approach was used to find a better calculation.
    return 1 - min(points ** 1.3 / max_points, 1.0)
