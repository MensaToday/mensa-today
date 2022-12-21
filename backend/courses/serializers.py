from rest_framework import serializers
import courses.models as course_model


class TimeslotSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["weekDay", "startTime", "endTime",
                  "startDate", "endDate", "rythm"]
        model = course_model.Timeslot


class ReservationSerializer(serializers.ModelSerializer):

    timeslot = TimeslotSerializer(read_only=True)

    class Meta:
        fields = ["timeslot"]
        model = course_model.Reservation


class CourseSerializer(serializers.ModelSerializer):

    reservation = serializers.ListSerializer(
        child=ReservationSerializer(read_only=True), source='reservation_set')

    class Meta:
        fields = ["publishId", "name", "learnweb_abbr", "reservation"]
        model = course_model.Course


class UserCourseSerializer(serializers.ModelSerializer):

    course = CourseSerializer(read_only=True)

    class Meta:
        fields = ["course"]
        model = course_model.UserCourse
