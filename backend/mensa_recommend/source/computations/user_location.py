from datetime import datetime, date

from courses.models import UserCourse, Reservation, RoomMensaDistance
from users.models import User


def transform_week_day_to_int(week_day: str):
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


def get_user_location(user: User):
    user_courses = UserCourse.objects.filter(user=user)

    valid_reservations = []

    for user_course in user_courses:
        course = user_course.course

        reservations = Reservation.objects.filter(course=course)

        for reservation in reservations:
            timeslot = reservation.timeslot

            week_day = transform_week_day_to_int(timeslot.weekDay)
            current_date_time = datetime.today()
            current_date = date.today()
            current_week_day = current_date_time.weekday()

            if week_day != -1:
                if current_week_day == week_day:
                    if timeslot.startDate <= current_date <= timeslot.endDate:
                        valid_reservations.append(reservation)

    if len(valid_reservations) == 0:
        return {}

    min_time_before_12 = float('inf')
    min_time_after_12 = float('inf')

    min_time_before_12_reservation: Reservation
    min_time_after_12_reservation: Reservation

    noon = datetime.now().replace(
        hour=12, minute=0, second=0, microsecond=0)

    for valid_reservation in valid_reservations:
        start_time = valid_reservation.timeslot.startTime
        start_date_time = datetime.now().replace(
            hour=start_time.hour, minute=start_time.minute, second=0,
            microsecond=0)

        end_time = valid_reservation.timeslot.endTime
        end_date_time = datetime.now().replace(
            hour=end_time.hour, minute=end_time.minute, second=0,
            microsecond=0)

        if end_date_time <= noon:
            time_diff = (noon - end_date_time).seconds
            if time_diff < min_time_before_12:
                min_time_before_12 = time_diff
                min_time_before_12_reservation = valid_reservation
        else:
            time_diff = (start_date_time - noon).seconds
            if time_diff < min_time_after_12:
                min_time_after_12 = time_diff
                min_time_after_12_reservation = valid_reservation

    if min_time_before_12 <= min_time_after_12:
        relevant_reservation = min_time_before_12_reservation
    else:
        relevant_reservation = min_time_after_12_reservation

    room_distances = RoomMensaDistance.objects.filter(
        room=relevant_reservation.room)

    result = {}

    for room_distance in room_distances:
        result[room_distance.mensa.id] = room_distance.distance

    return result
