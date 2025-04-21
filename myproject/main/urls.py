from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import ReservationListCreateAPI
from .views import ReservationListCreateAPI, RestaurantListAPI
from .views import my_reservations
from .views import cancel_reservation

from .views import restaurant_list

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('reserve/', views.make_reservation, name='reserve'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('api/restaurants/', RestaurantListAPI.as_view(), name='api_restaurants'),
    path('api/reservations/', ReservationListCreateAPI.as_view(), name='api_reservations'),
    path('my-reservations/', my_reservations, name='my_reservations'),
    path('cancel/<int:pk>/', cancel_reservation, name='cancel_reservation'),
]



urlpatterns += [
    path('api/reservations/', ReservationListCreateAPI.as_view(), name='api_reservations'),
]


