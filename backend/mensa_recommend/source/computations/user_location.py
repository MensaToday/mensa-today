from datetime import datetime, date, time
from typing import Optional, List, Dict

from django.db.models.manager import BaseManager

from courses.models import UserCourse, Reservation, RoomMensaDistance
from mensa_recommend.source.computations.transformer import \
    transform_week_day_to_int
from users.models import User


def get_user_location(user: User, current_date: Optional[date] = None,
                      _time: Optional[time] = None) -> Dict[int, float]:
    """Get the distance from the current user location to every mensa

        Parameters
        ----------
        user: User
            A user where the distance should be returned
        current_date: Optional[date]
            The date where the position of the user should be returned.
            If None the current date will be picked
        _time: Optional[time]
            Time of noon (Default = None)


        Return
        ------
        distances: dict
            A dict with distances to every mensa in the following format:
            {
                mensa_id: distance
            }
            If there are no valid reservations an empty dict will be returned

    """

    # Get all courses of a user
    user_courses = UserCourse.objects.filter(user=user)

    # Get the current date and weekday
    if current_date is None:
        current_date = date.today()
    elif not isinstance(current_date, date):
        raise ValueError("current_date is not of the type datetime.date but "
                         f"of type: {type(current_date)}")

    valid_reservations = get_relevant_reservations(user_courses, current_date)

    # If there are no valid reservations an empty dict will be returned
    if len(valid_reservations) == 0:
        return {}

    relevant_reservation = choose_relevant_reservation(
        valid_reservations, current_date, _time)

    # Get the distance between the room of the reservation and every mensa
    room_distances = RoomMensaDistance.objects.filter(
        room=relevant_reservation.room)

    # Transform the distances to the output format s.o.
    result = {}
    for room_distance in room_distances:
        result[room_distance.mensa.id] = room_distance.distance

    return result


def get_relevant_reservations(user_courses: BaseManager[UserCourse],
                              current_date: date) -> List[Reservation]:
    """Iterate over each course to get the relevant courses for that day.
        A course is relevant/valid if it belongs to the current day. All
        relevant reservations will be returned

        Parameters
        ----------
        user_courses: BaseManager[UserCourse]
            All courses of a user
        current_date: date
            The date of the reservations

        Return
        ------
        valid_reservations: List[Reservation]
            All valid reservations
    """

    valid_reservations = []

    for user_course in user_courses:

        # Get all reservations for this course
        reservations = Reservation.objects.filter(course=user_course.course)

        # Iterate over each reservation to check the timeslot
        for reservation in reservations:
            timeslot = reservation.timeslot

            # Get and transform week day of the timeslot
            week_day = transform_week_day_to_int(timeslot.weekDay)#
            current_week_day = current_date.weekday()

            if week_day != -1:

                # Check if the week day of the current day is equal
                # to the week day of the course
                if current_week_day == week_day:

                    # Check if the current date falls in between the
                    # start and end date of the course
                    if timeslot.startDate <= current_date <= timeslot.endDate:

                        # If all requirements are met, the reservation can be
                        # added to the valid reservations list
                        valid_reservations.append(reservation)

    return valid_reservations


def choose_relevant_reservation(valid_reservations: List[Reservation],
                                current_date: date,
                                _time: Optional[time] = None) -> Reservation:
    """ Choose of all reservations the reservation with the smallest 
    time difference to noon. All reservations in the list have to be on the
    same day.

        Parameters
        ----------
        valid_reservations: List[Reservation]
            All valid reservations on the same day
        current_date: date
            The date of the reservations
        _time: Optional[time]
            The time that should be checked (Default = None).
            If the time is None the time will be set to 12:00:00


        Return
        ------
        relevant_reservation: Reservation
            The reservation with the smallest time difference.
    """

    # Initialize variables to keep track of current minimum
    min_time_before = float('inf')
    min_time_after = float('inf')

    min_time_before_reservation: Reservation
    min_time_after_reservation: Reservation

    if _time is None:
        _time = time(12, 0, 0)
    elif not isinstance(current_date, date):
        raise ValueError("_time is not of the type datetime.time but of type:"
                         f" {type(_time)}")

    # Initialize date with the given time
    specific_time = datetime.combine(current_date, _time)

    for valid_reservation in valid_reservations:

        # Get the start time of the reservation
        start_time = valid_reservation.timeslot.startTime

        # transform the start time into a start date time
        start_date_time = datetime.now().replace(
            hour=start_time.hour, minute=start_time.minute, second=0,
            microsecond=0)

        # Get the end time of the reservation
        end_time = valid_reservation.timeslot.endTime

        # transform the end time into a start date time
        end_date_time = datetime.now().replace(
            hour=end_time.hour, minute=end_time.minute, second=0,
            microsecond=0)

        # Check if the end date time is smaller or equal to _time (first case)
        if end_date_time <= specific_time:

            # calculate the time difference between _time and end date time
            time_diff = (specific_time - end_date_time).seconds

            # If the difference is smaller than the current minimum before
            # _time, update the minimum and the reservation
            if time_diff < min_time_before:
                min_time_before = time_diff
                min_time_before_reservation = valid_reservation
        elif start_date_time >= specific_time:
            # end date time is greater than noon (second case)

            # calculate the time difference between noon and end date time
            time_diff = (start_date_time - specific_time).seconds

            # If the difference is smaller than the current minimum after
            # _time, update the minimum and the reservation
            if time_diff < min_time_after:
                min_time_after = time_diff
                min_time_after_reservation = valid_reservation
        else:
            # start date time and end date time of the course is between noon

            # calculate the time difference between _time and end date time
            time_diff = (end_date_time - specific_time).seconds

            # If the difference is smaller than the current minimum after
            # _time, update the minimum and the reservation
            if time_diff < min_time_after:
                min_time_after = time_diff
                min_time_after_reservation = valid_reservation

    # Get the reservation with the smallest time of before and after _time
    if min_time_before <= min_time_after:
        relevant_reservation = min_time_before_reservation
    else:
        relevant_reservation = min_time_after_reservation

    return relevant_reservation
