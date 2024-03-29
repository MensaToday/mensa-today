from django.urls import path
from . import views

urlpatterns = [
    path('mensa/get_dishplan', views.get_dishplan),
    path('mensa/user_ratings', views.user_ratings),
    path('mensa/get_recommendations', views.get_recommendations),
    path('mensa/get_week_recommendation', views.get_week_recommendation),
    path('mensa/get_quiz_dishes', views.get_quiz_dishes),
    path('mensa/save_user_side_dishes', views.save_user_side_dishes),
    path('mensa/mensa_data', views.get_mensa_data),
]
