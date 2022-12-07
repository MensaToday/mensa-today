import datetime
from datetime import datetime

from mensa.models import (Allergy, Category, Dish, DishPlan, UserAllergy,
                          UserCategory, UserDishRating)
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.source.authentication.manual_jwt import get_tokens_for_user


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from mensa.models import Category, Allergy, UserAllergy, UserCategory, Dish, \
    UserDishRating, DishPlan
from mensa_recommend.source.computations.date_computations import \
    get_last_monday
from mensa_recommend.source.computations.transformer import transform_rating
from mensa_recommend.source.data_collection.klarna import KlarnaCollector
from mensa_recommend.source.data_collection.learnweb import (LearnWebCollector,
                                                             run)
from mensa_recommend.source.recommendation import recommender

from users.models import User
from users.source.authentication.manual_jwt import get_tokens_for_user
from mensa_recommend.source.computations.decryption import decrypt

from .serializers import DishPlanSerializer, UserDishRatingSerializer


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
def get_dishplan(request):
    """Get the dishplan for the next week

        Route: api/v1/user/check_card_id
        Authorization: Authenticated
        Methods: GET

        Output
        -------
        [
            {
                "dish": {
                    "id": 239,
                    "categories": [
                        {
                            "category": {
                                "id": 1,
                                "name": "Vegan"
                            }
                        }
                    ],
                    "additives": [
                        {
                            "additive": {
                                "id": 1,
                                "name": "Dyed"
                            }
                        }
                    ],
                    "allergies": [],
                    "main": true,
                    "name": "Steckrübeneintopf"
                },
                "ext_ratings": {
                    "id": 1678,
                    "rating_avg": "0.0",
                    "rating_count": 0
                },
                "user_ratings": [
                    {
                        "rating": 1.0
                    }
                ],
                "mensa": {
                    "id": 4,
                    "name": "Bistro Durchblick",
                    "city": "Münster",
                    "street": "Fliednerstr.",
                    "houseNumber": "21",
                    "zipCode": 48149,
                    "startTime": "11:30:00",
                    "endTime": "13:30:00"
                },
                "date": "2022-12-01",
                "priceStudent": "3.08",
                "priceEmployee": "2.05"
            },
        ]
    """

    last_monday = get_last_monday()

    return Response(
        DishPlanSerializer(DishPlan.objects.filter(date__gte=last_monday),
                           many=True, context={'user': request.user}).data)


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def user_ratings(request):
    """Save or get user ratings

        Route: api/v1/mensa/user_ratings
        Authorization: Authenticated
        Methods: Get, Post

        POST
        ----

        Input
        ------
        {
            "dish_id": int
            "rating": 1-5
        }

        Output
        -------
        200-OK when rating is successully stored in the database
        400 when ratings is not a number between 1-5
        404 when dish cannot be found in the database
        406 when not all fields were provided

        GET
        ---

        Output
        -------
        [
            {
                "dish": {
                    "id": int,
                    "main": bool,
                    "name": str
                },
                "rating": float between 0-1
            }
        ]
    """

    if request.method == 'POST':

        # Check if all required attributes are given
        if 'dish_id' in request.data and 'rating' in request.data:

            # Get data
            dish_id = request.data['dish_id']
            rating = request.data['rating']
            user = request.user

            # Check if dish is available
            try:
                dish = Dish.objects.get(id=dish_id)
            except:
                dish = None

            if dish:

                # Transform rating to float between 0-1
                rating = transform_rating(rating)

                # If rating is valid
                if rating:

                    # Save the rating
                    UserDishRating(dish=dish, user=user, rating=rating).save()

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(
                        "Rating not a number or not between 1 and 5",
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Dish cannot be found in the database",
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Not all fields provided",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'GET':

        user = request.user

        # Get all ratings for the user
        try:
            ratings = UserDishRating.objects.all().filter(user=user)
        except:
            ratings = []

        return Response(UserDishRatingSerializer(ratings, many=True).data,
                        status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    if request.version == 'v1':
        return Response("Hello World v1")
    else:
        return Response("Hello World v2")


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def get_week_recommendation(request):
    """Get simple week recommendation without extra information.

            Route: api/v1/mensa/get_week_recommendation
            Authorization: Authenticated
            Methods: Get

            GET
            ---

            Output
            -------
            [
                {
                    "dish": {
                        "id": 77,
                        "categories": [
                            {
                                "category": {
                                    "id": 1,
                                    "name": "Vegan"
                                }
                            }
                        ],
                        "additives": [
                            {
                                "additive": {
                                    "id": 4,
                                    "name": "Flavor enhancers"
                                }
                            }
                        ],
                        "allergies": [
                            {
                                "allergy": {
                                    "id": 23,
                                    "name": "Celery"
                                }
                            }
                        ],
                        "main": true,
                        "name": "Süßkartoffelcurry mit Paprika und Pilzen",
                        "url": "https://live.staticflickr.com/3552/3467142312_ca85ae1b27_b.jpg"
                    },
                    "ext_ratings": {
                        "id": 127,
                        "rating_avg": "3.8",
                        "rating_count": 9
                    },
                    "user_ratings": [],
                    "mensa": {
                        "id": 2,
                        "name": "Mensa Da Vinci",
                        "city": "Münster",
                        "street": "Leonardo-Campus",
                        "houseNumber": "8",
                        "zipCode": 48149,
                        "startTime": "11:30:00",
                        "endTime": "14:00:00"
                    },
                    "date": "2022-12-05",
                    "priceStudent": "3.40",
                    "priceEmployee": "5.10"
                },
                ...
            ]

            200-OK if inputs are valid
            406 when not all fields were provided or the inputs were malformed
        """
    r = recommender.DishRecommender(request.user, datetime.today(), True)
    res = r.predict(1, serialize=True)

    recommendations = [day[0][0] for day in res.values()]
    return Response(recommendations, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def get_recommendations(request):
    """Get user recommendations.

        Route: api/v1/mensa/get_recommendations
        Authorization: Authenticated
        Methods: Get

        GET
        ---

        Input
        ------
        {
            "day": "2022.12.05",
            "entire_week": "False",
            "recommendations_per_day": 1
        }

        Output
        -------
        {
            "2022.12.05": [
                [
                    {
                        "dish": {
                            "id": 85,
                            "categories": [
                                {
                                    "category": {
                                        "id": 2,
                                        "name": "Vegetarian"
                                    }
                                }
                            ],
                            "additives": [],
                            "allergies": [
                                {
                                    "allergy": {
                                        "id": 9,
                                        "name": "Egg"
                                    }
                                },
                                {
                                    "allergy": {
                                        "id": 1,
                                        "name": "Gluten"
                                    }
                                },
                                {
                                    "allergy": {
                                        "id": 13,
                                        "name": "Milk"
                                    }
                                },
                                {
                                    "allergy": {
                                        "id": 7,
                                        "name": "Wheat"
                                    }
                                }
                            ],
                            "main": true,
                            "name": "Ricotta-Spinat-Cannelloni mit Tomatensauce"
                        },
                        "ext_ratings": {
                            "id": 153,
                            "rating_avg": "5.0",
                            "rating_count": 1
                        },
                        "user_ratings": [],
                        "mensa": {
                            "id": 11,
                            "name": "Mensa Bispinghof",
                            "city": "Münster",
                            "street": "Bispinghof",
                            "houseNumber": "9-14",
                            "zipCode": 48149,
                            "startTime": "11:00:00",
                            "endTime": "14:30:00"
                        },
                        "date": "2022-12-05",
                        "priceStudent": "2.05",
                        "priceEmployee": "3.08"
                    },
                    0.7345052573194639
                ]
            ]
        }

        200-OK if inputs are valid
        406 when not all fields were provided or the inputs were malformed
    """
    if "day" not in request.data \
            or "entire_week" not in request.data:
        return Response("Not all fields provided",
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        day: datetime.date = recommender.str_to_date(request.data["day"])
    except ValueError:
        return Response("Wrong 'day' format. Use: '%Y.%m.%d'. Example: "
                        "'2022.12.06'",
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    entire_week: bool = request.data["entire_week"].lower() == "true"

    if "recommendations_per_day" in request.data:
        try:
            rec_per_day = int(request.data["recommendations_per_day"])
        except ValueError:
            return Response("Wrong 'recommendations_per_day' format. "
                            "Use integers only.",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if rec_per_day < 1:
            return Response("'recommendations_per_day' must be > 0.",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        rec_per_day = 1

    r = recommender.DishRecommender(request.user, day, entire_week)
    res = r.predict(rec_per_day, serialize=True)

    num_dishes = len(r.dishes)
    num_filtered_dishes = len(r.filtered_dishes)
    # TODO: Maybe add this information for front end?

    return Response(res, status=status.HTTP_200_OK)
