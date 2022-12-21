from mensa_recommend.source.data_collection.learnweb import (LearnWebCollector,
                                                             run)
from mensa_recommend.source.computations.decryption import decrypt

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from courses.models import UserCourse
from courses.serializers import UserCourseSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def recrawl_courses(request):
    """Recrawl the learnweb courses

        Route: api/v1/course/recrawl
        Authorization: IsAuthenticated
        Methods: POST

        Input
        ------
        {
            "username": str,
            "password": str
        }

        Output
        -------
        If the credentials are wrong:
            401 UNAUTHORIZED
        If not all fields were provided:
            406 NOT ACCEPTABLE
        Otherwise:
            200 OK
    """

    ziv_id = request.data['username']
    ziv_password = request.data['password']
    ziv_password = decrypt(ziv_password)

    user = request.user

    if 'username' in request.data and 'password' in request.data:

        # Check if provided login data is correct
        session_id = LearnWebCollector(ziv_id, ziv_password).get_session_id()

        # Check if credentials are correct
        if session_id:
            run.delay(ziv_id, ziv_password, user.id, True)

            return Response("Courses updated",
                            status=status.HTTP_200_OK)
        else:
            # If data is not correct send user feedback
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response("Not all fields provided",
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_courses(request):
    """Get all course information of a user

        Route: api/v1/course/get_courses
        Authorization: IsAuthenticated
        Methods: GET

        Output
        -------
        [
            {
                "course": {
                    "publishId": 363967,
                    "name": "Data Analytics 1 WiSe 2022/23, Heike Trautmann, Raphael Prager",
                    "learnweb_abbr": "DA1-2022_2",
                    "reservation": [
                        {
                            "timeslot": {
                                "weekDay": "Thu.",
                                "startTime": "10:00:00",
                                "endTime": "12:00:00",
                                "startDate": "2022-10-13",
                                "endDate": "2023-02-02",
                                "rythm": "weekly"
                            }
                        },
                        {
                            "timeslot": {
                                "weekDay": "Fri.",
                                "startTime": "10:00:00",
                                "endTime": "12:00:00",
                                "startDate": "2022-10-14",
                                "endDate": "2023-02-03",
                                "rythm": "weekly"
                            }
                        }
                    ]
                }
            },
        ]

        If not logged in:
            401 UNAUTHORIZED

    """

    return Response(UserCourseSerializer(UserCourse.objects.filter(user=request.user),
                                         many=True).data)
