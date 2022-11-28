from django.urls import path
from . import views

urlpatterns = [
    path('get_data', views.getData),
    path('user/register', views.register),
    path('user/logout', views.logout),
    path('user/check_card_id', views.check_card_id),
    path('mensa/get_dishplan', views.get_dishplan),
    path('mensa/user_ratings', views.user_ratings)
]
