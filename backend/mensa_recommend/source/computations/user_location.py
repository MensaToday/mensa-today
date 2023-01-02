from datetime import datetime, date
from mensa_recommend.source.computations.transformer import transform_week_day_to_int

from courses.models import UserCourse, Reservation, RoomMensaDistance
from users.models import User
from django.db.models.manager import BaseManager


def get_user_location(user: User) -> dict[int, float]:
    """Get the distance fromt he current user location to every mensa

        Parameters
        ----------
        user: User
            A user where the distance should be returned


        Return
        ------
        distances: dict
            A dict with distances to every mensa in the following format:
            {
                mensa_id: distance
            }
            If there are no valid reservations an empty dict will be returned

        TODO add a possibility to enter a custom date
    """

    # Get all courses of a user
    user_courses = UserCourse.objects.filter(user=user)

    valid_reservations = get_relevant_reservations(user_courses)

    # If there are no valid reservations an empty dict will be returned
    if len(valid_reservations) == 0:
        return {}

    relevant_reservation = choose_relevant_reservation(valid_reservations)

    # Get the distance between the room of the rervation and every mensa
    room_distances = RoomMensaDistance.objects.filter(
        room=relevant_reservation.room)

    # Transform the distances to the output format s.o.
    result = {}
    for room_distance in room_distances:
        result[room_distance.mensa.id] = room_distance.distance

    return result


def get_relevant_reservations(user_courses: BaseManager[UserCourse]) -> list[Reservation]:
    """Iterate over each course to get the relevant courses for that day.
        A course is relevant/valid if it belongs to the current day. All relevant
        reservations will be returned

        Parameters
        ----------
        user_courses: BaseManager[UserCourse]
            all courses of a user


        Return
        ------
        valid_reservations: List[Reservation]
            all valid reservations
    """

    valid_reservations = []

    for user_course in user_courses:

        # Get all reservations for this course
        reservations = Reservation.objects.filter(course=user_course.course)

        # Iterate over each reservation to check the timeslot of each reservation
        for reservation in reservations:

            timeslot = reservation.timeslot

            # Get and transform week day of the timeslot
            week_day = transform_week_day_to_int(timeslot.weekDay)

            # Get the current date time, date and weekday
            current_date_time = datetime.today()
            current_date = date.today()
            current_week_day = current_date_time.weekday()

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


def choose_relevant_reservation(valid_reservations: list[Reservation]):
    """ Choose of all reservations the reservation with the smallest 
    time difference to noon. All reservations in the list have to be on the same day

        Parameters
        ----------
        valid_reservations: list[Reservation]
            All valid reservations on the same day


        Return
        ------
        relevant_reservation: Reservation
            Reservation with the smallest time difference to noon
    """

    # Initialize variables to keep track of current minimum
    min_time_before_12 = float('inf')
    min_time_after_12 = float('inf')

    min_time_before_12_reservation: Reservation
    min_time_after_12_reservation: Reservation

    # Initialize date with a time of 12:00:00 (noon)
    noon = datetime.now().replace(
        hour=12, minute=0, second=0, microsecond=0)

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

        # Check if the end date time is smaller or equals to noon (first case)
        if end_date_time <= noon:

            # calculate the time difference between noon and end date time
            time_diff = (noon - end_date_time).seconds

            # If the difference is smaller than the current minimum before 12,
            # update the minimun and the reservation
            if time_diff < min_time_before_12:
                min_time_before_12 = time_diff
                min_time_before_12_reservation = valid_reservation
        else:
            # end date time is greater than noon (second case)

            # calculate the time difference between noon and end date time
            time_diff = (start_date_time - noon).seconds

            # If the difference is smaller than the current minimum after 12,
            # update the minimun and the reservation
            if time_diff < min_time_after_12:
                min_time_after_12 = time_diff
                min_time_after_12_reservation = valid_reservation

    # Get the reservation with the smallest time of before and after 12
    if min_time_before_12 <= min_time_after_12:
        relevant_reservation = min_time_before_12_reservation
    else:
        relevant_reservation = min_time_after_12_reservation

    return relevant_reservation
