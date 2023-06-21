from django.urls import path
from .view import *
urlpatterns = [
    path('get_data/', getData),
    path('add/', addData)
]