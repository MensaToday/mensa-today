from django.urls import path
from . import views

urlpatterns = [
    path('get_data', views.getData),
    path('user/register', views.register),
    path('user/logout', views.logout),
    path('user/login', views.login),
    path('user/check_card_id', views.check_card_id),
    path('user/get_balance', views.get_balance),
    path('mensa/get_dishplan', views.get_dishplan),
    path('mensa/user_ratings', views.user_ratings),
    path('mensa/get_recommendations', views.get_recommendations),
    path('mensa/get_week_recommendation', views.get_week_recommendation)
]
