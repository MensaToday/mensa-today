import datetime


def get_last_monday() -> datetime.date:
    """Get the date of the last monday

    Return
    ------
    last_monday : date
        The date of the last monday
    """
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    return last_monday
