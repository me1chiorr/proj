# main/api_urls.py
from django.urls import path
from .views import RestaurantListAPI, ReservationListCreateAPI

urlpatterns = [
    path('restaurants/', RestaurantListAPI.as_view(), name='api_restaurants'),
    path('reservations/', ReservationListCreateAPI.as_view(), name='api_reservations'),
]
