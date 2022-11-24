from django.urls import path
from . import views

urlpatterns = [
    path('get_data', views.getData),
    path('user/register', views.register),
    path('user/check_card_id', views.check_card_id)
]
