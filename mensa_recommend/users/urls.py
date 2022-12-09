from django.urls import path
from . import views

urlpatterns = [
    path('user/register', views.register),
    path('user/logout', views.logout),
    path('user/login', views.login),
    path('user/check_card_id', views.check_card_id),
    path('user/get_balance', views.get_balance),
]
