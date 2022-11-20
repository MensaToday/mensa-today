from django.urls import path
from . import views

urlpatterns = [
    path('learnweb_login', views.learnweb_login, name='learnweb_login'),
]
