from django.urls import path
from .views import *

urlpatterns = [
    path('', get_data, name='Home'),
    path('result', get_data, name="result")
]
