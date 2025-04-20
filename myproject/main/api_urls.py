from django.urls import path
from .views import ReservationListCreateAPI

urlpatterns = [
    path('reservations/', ReservationListCreateAPI.as_view(), name='api_reservations'),
]
