import datetime
from datetime import datetime

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import random

from mensa.models import Dish, DishPlan, UserDishRating
from mensa_recommend.serializers import DishPlanSerializer, \
    UserDishRatingSerializer

from mensa.models import UserDishRating, Dish

import datetime
from datetime import datetime

from mensa.models import Dish, DishPlan, UserDishRating, Category, Allergy
from mensa_recommend.source.computations.date_computations import \
    get_last_monday
from mensa_recommend.source.computations.transformer import transform_rating
from mensa_recommend.source.recommendation import recommender

from mensa_recommend.serializers import DishPlanSerializer, UserDishRatingSerializer, DishSerializer


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

            200-OK if successful
        """
    r = recommender.DishRecommender(request.user, datetime.today(), True)
    res = r.predict(1, serialize=True)

    recommendations = [day[0][0] if len(day) > 0 else {} for day
                       in res.values()]
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


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_quiz_dishes(request):
    """Get random dishes for the initial quiz based on the user preferences

        Route: api/v1/mensa/get_quiz_dishes
        Authorization: Any
        Methods: Get


        Input
        ------
        {
            "categories": [str],
            "allergies": [str]
        }

        Output
        -------
        [
            {
                "id": 275,
                "categories": [
                    {
                        "category": {
                            "id": 4,
                            "name": "Beef"
                        }
                    }
                ],
                "additives": [],
                "allergies": [
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
                            "id": 23,
                            "name": "Celery"
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
                "name": "Nudeln mit Bolognese, Parmesankäse",
                "url": "https://live.staticflickr.com/5164/5242038276_ff3753e36a_n.jpg"
            },
        ]
    """

    if 'categories' in request.data and 'allergies' in request.data:

        # get request parameters
        categories = request.data['categories']
        allergies = request.data['allergies']

        category_objects = Category.objects.filter(name__in=categories)
        allergy_objects = Allergy.objects.exclude(name__in=allergies)

        dishes = list(Dish.objects.filter(
            categories__in=category_objects, allergies__in=allergy_objects, url__isnull=False))

        random_dishes = random.sample(dishes, 3)

        return Response(DishSerializer(random_dishes, many=True).data)
