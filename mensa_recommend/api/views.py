from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from mensa_recommend.source.data_collection.learnweb import LearnWebCollector, run
from rest_framework import status
from users.models import User
from users.source.authentication.manual_jwt import get_tokens_for_user


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):

    # check if request parameters were provided
    if 'username' in request.POST and 'password' in request.POST:

        # get request parameters
        ziv_id = request.POST['username']
        ziv_password = request.POST['password']

        # Get user to check if the user is already registered
        user = User.objects.get(username=ziv_id)

        if not user:
            # Check if provided login data is correct
            session_id = LearnWebCollector(
                ziv_id, ziv_password).get_session_id()

            if session_id == False:

                # If data is not correct send user feedback
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:

                user = User.objects.create_user(ziv_id, ziv_password)
                user.save()
                # Id data is correct then crawling can be started
                run.delay(ziv_id, ziv_password, user.id)

                # create token for the registered user
                token = get_tokens_for_user(user)

                return Response(token, status=status.HTTP_200_OK)
        else:
            return Response("User already exists", status=status.HTTP_409_CONFLICT)

    else:
        return Response("Not all fields provided", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    if request.version == 'v1':
        return Response("Hello World v1")
    else:
        return Response("Hello World v2")
