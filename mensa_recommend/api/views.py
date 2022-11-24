from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from mensa_recommend.source.data_collection.learnweb import LearnWebCollector, run
from mensa_recommend.source.data_collection.klarna import KlarnaCollector
from rest_framework import status
from users.models import User
from users.source.authentication.manual_jwt import get_tokens_for_user


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    """Register a new user.

        Route: api/v1/user/register
        Authorization: Any
        Methods: POST

        Input
        ------
        {
            "card_id": int
        }

        Output
        -------
        If the credentials are valid:
            {
                "refresh": str
                "access": str
            }
        If the user already exists:
            409 CONFLICT
        If the credentials are wrong:
            401 UNAUTHORIZED
    """

    # check if request parameters were provided
    if 'username' in request.data and 'password' in request.data and \
        'categories' in request.data and 'allergies' in request.data and \
            'card_id' in request.data and 'ratings' in request.data:

        # get request parameters
        ziv_id = request.data['username']
        ziv_password = request.data['password']
        categories = request.data['categories']
        allergies = request.data['allergies']
        card_id = request.data['card_id']
        ratings = request.data['ratings']

        # Get user to check if the user is already registered
        try:
            user = User.objects.get(username=ziv_id)
        except:
            user = None

        if not user:
            # Check if provided login data is correct
            session_id = LearnWebCollector(
                ziv_id, ziv_password).get_session_id()

            # Check if credentials are correct
            if session_id:

                # Check card_id
                if card_id != -1:
                    current_balance = KlarnaCollector().get_current_balance(card_id)
                else:
                    current_balance = 1

                # if card if correct current_balance is not None
                if current_balance:
                    user = User.objects.create_user(ziv_id, ziv_password)

                    # If the card_id is -1 no card id was provided by the user.
                    # Therefore no card_is has to be saved
                    if card_id != -1:
                        user.card_id = card_id
                        user.save()

                    # TODO save categories, allergies and ratings

                    # Id data is correct then crawling can be started
                    run.delay(ziv_id, ziv_password, user.id)

                    # create token for the registered user
                    token = get_tokens_for_user(user)

                    return Response(token, status=status.HTTP_200_OK)
                else:
                    return Response("Card ID wrong", status=status.HTTP_404_NOT_FOUND)

            else:
                # If data is not correct send user feedback
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response("User already exists", status=status.HTTP_409_CONFLICT)

    else:
        return Response("Not all fields provided", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def check_card_id(request):
    """Check if the card_id is valid

        Route: api/v1/user/check_card_id
        Authorization: Any
        Methods: POST

        Input
        ------
        {
            "card_id": int
        }

        Output
        -------
        If the card_id is valid the balance will be returned.
        When it is wrong an 404 will be returned.
    """

    if 'card_id' in request.data:
        card_id = request.data['card_id']

        current_balance = KlarnaCollector().get_current_balance(card_id)

        if current_balance:
            return Response(current_balance, status=status.HTTP_200_OK)
        else:
            return Response("Card ID wrong", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Not all fields provided", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    if request.version == 'v1':
        return Response("Hello World v1")
    else:
        return Response("Hello World v2")
