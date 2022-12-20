from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.source.authentication.manual_jwt import get_tokens_for_user
from django.contrib.auth import authenticate

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from mensa_recommend.source.computations.decryption import decrypt
from mensa_recommend.source.data_collection.learnweb import (LearnWebCollector,
                                                             run)
from mensa_recommend.source.data_collection.klarna import KlarnaCollector

from mensa.models import Category, UserCategory, Allergy, UserAllergy, UserDishRating, Dish

from mensa_recommend.serializers import UserSerializer


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
            "username": str,
            "password": str,
            "categories": [],
            "allergies": [],
            "card_id": int,
            "ratings": [{
                "id": int,
                "rating": int
            }]
        }

        Output
        -------
        If the credentials are valid:
            {
                "refresh": str
                "access": str
            }
        If the user already exists:
            406 NOT ACCEPTABLE
        If the credentials are wrong:
            401 UNAUTHORIZED
        If not all fields were provided:
                406 NOT ACCEPTABLE
    """

    # check if request parameters were provided
    if 'username' in request.data and 'password' in request.data and \
            'categories' in request.data and 'allergies' in request.data and \
            'card_id' in request.data and 'ratings' in request.data:

        # get request parameters
        ziv_id = request.data['username']
        ziv_password = request.data['password']
        ziv_password = decrypt(ziv_password)
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
                    current_balance = KlarnaCollector().get_current_balance(
                        card_id)
                else:
                    current_balance = 1

                # if card if correct current_balance is not None
                if current_balance is not None:
                    user = User.objects.create_user(ziv_id, ziv_password)

                    # If the card_id is -1 no card id was provided by the user.
                    # Therefore no card_is has to be saved
                    if card_id != -1:
                        user.card_id = card_id
                        user.save()

                    # Save categories
                    if len(categories) == 0:
                        categorie_objects = Category.objects.all()
                    else:
                        categorie_objects = []
                        for category in categories:
                            try:
                                category_object = Category.objects.get(
                                    name=category)

                                categorie_objects.append(category_object)
                            except:
                                pass

                    for co in categorie_objects:
                        UserCategory(user=user, category=co).save()

                    # Save allergies
                    allergies_objects = []
                    for allergy in allergies:
                        try:
                            allergy_object = Allergy.objects.get(name=allergy)
                            allergies_objects.append(allergy_object)
                        except:
                            pass

                    for ao in allergies_objects:
                        UserAllergy(user=user, allergy=ao).save()

                    # Save ratings
                    for rating in ratings:
                        if 'id' in rating and 'rating' in rating:

                            if rating['rating'] > 1 or rating['rating'] < 0:
                                print("Rating in invalid range")
                            else:
                                try:
                                    dish = Dish.objects.get(id=rating['id'])
                                except:
                                    dish = None

                                if dish:
                                    UserDishRating(
                                        user=user, dish=dish,
                                        rating=rating['rating']).save()

                    # Id data is correct then crawling can be started
                    run.delay(ziv_id, ziv_password, user.id)

                    # create token for the registered user
                    token = get_tokens_for_user(user)

                    return Response(token, status=status.HTTP_200_OK)
                else:
                    return Response("Card ID wrong",
                                    status=status.HTTP_404_NOT_FOUND)

            else:
                # If data is not correct send user feedback
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response("User already exists",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response("Not all fields provided",
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    """Login a user.

        Route: api/v1/user/register
        Authorization: Any
        Methods: POST

        Input
        ------
        {
            "username": str,
            "password": str,
        }

        Output
        -------
        If the credentials are valid:
            {
                "refresh": str
                "access": str
            }
        If the credentials are wrong:
            401 UNAUTHORIZED
        If not all fields were provided:
            406 NOT ACCEPTABLE
        If something in the login process fails:
            400 BAD REQUEST
    """
    try:
        if 'username' in request.data and 'password' in request.data:
            username = request.data["username"]
            password = decrypt(request.data["password"])

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Not all fields provided",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def delete_account(request):
    """Delete a user account

        Route: api/v1/user/delete
        Authorization: IsAuthenticated
        Methods: POST

        Output
        -------
        If the user is successfully delete: 202
        If error occured while deleteing: 400
        If unauthenticated: 401
    """
    user = request.user

    try:
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        When it is wrong a 404 will be returned.
        If not all fields were provided: 406
    """

    if 'card_id' in request.data:
        card_id = request.data['card_id']

        current_balance = KlarnaCollector().get_current_balance(card_id)

        if current_balance:
            return Response(current_balance, status=status.HTTP_200_OK)
        else:
            return Response("Card ID wrong", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Not all fields provided",
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_balance(request):
    """Get the current card balance

        Route: api/v1/user/get_balance
        Authorization: Authenticated
        Methods: GET

        Output
        -------
        If card is not None:
            balance with 200
        If card is None:
            404 Not found
    """
    user = request.user

    if user.card_id is not None:
        balance = KlarnaCollector().get_current_balance(user.card_id)
        return Response(balance, status=status.HTTP_200_OK)
    else:
        return Response("No card_id in user profile",
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_user_data(request):
    """Get infos about the user

        Route: api/v1/user/get_user_data
        Authorization: Authenticated
        Methods: GET

        Output
        -------
        {
            "username": str,
            "card_id": int
        }
    """
    user = request.user

    return Response(UserSerializer(user).data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def update_card_id(request):
    """Update the card ID of the user

        Route: api/v1/user/update_card_id
        Authorization: Authenticated
        Methods: POST

        Input
        ------
        {
            "card_id": int
        }

        Output
        -------
        If card id is valid: 200
        If card id is wrong: 404
        If card id not provided: 406
    """
    if 'card_id' in request.data:
        card_id = request.data['card_id']

        # Check card_id

        current_balance = KlarnaCollector().get_current_balance(
            card_id)

        if current_balance is not None:
            user = request.user
            user.card_id = card_id
            user.save()

            return Response("Card Id updated successfully",
                            status=status.HTTP_200_OK)
        else:
            return Response("Card ID wrong", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("Not all fields provided",
                        status=status.HTTP_406_NOT_ACCEPTABLE)
