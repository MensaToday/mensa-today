from django.urls import path
from . import views

urlpatterns = [
    path('course/recrawl', views.recrawl_courses),
    path('course/get_courses', views.get_courses),
]
